"""
File: titanic_level1.py
Name: 
----------------------------------
This file builds a machine learning algorithm from scratch 
by Python codes. We'll be using 'with open' to read in dataset,
store data into a Python dict, and finally train the model and 
test it on kaggle. This model is the most flexible one among all
levels. You should do hyperparameter tuning and find the best model.
"""
import util
import math
TRAIN_FILE = 'titanic_data/train.csv'
TEST_FILE = 'titanic_data/test.csv'


def data_preprocess(filename: str, data: dict, mode='Train', training_data=None):
	"""
	:param filename: str, the filename to be processed
	:param data: dict[str: list], key is the column name, value is its data
	:param mode: str, indicating the mode we are using
	:param training_data: dict[str: list], key is the column name, value is its data
						  (You will only use this when mode == 'Test')
	:return data: dict[str: list], key is the column name, value is its data
	"""

	with open(filename, 'r') as f:
		is_first_line = True
		for line in f:
			data_lst = line.strip().split(',')

			if mode == 'Train':
				start = 1
				if is_first_line:
					keys = [data_lst[1], data_lst[2], data_lst[4], data_lst[5], data_lst[6], data_lst[7], data_lst[9],
							data_lst[11]]
					for key in keys:
						data[key] = []
					is_first_line = False
					continue
				else:
					# Train [Survived, Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]
					data_lst = [data_lst[1], data_lst[2], data_lst[5], data_lst[6], data_lst[7], data_lst[8], data_lst[10],
							data_lst[12]]
			elif mode == 'Test':
				start = 0
				if is_first_line:
					keys = [data_lst[1], data_lst[3], data_lst[4], data_lst[5], data_lst[6], data_lst[8], data_lst[10]]
					for key in keys:
						data[key] = []
					is_first_line = False
					continue
				else:
					# Test [Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]
					data_lst = [data_lst[1], data_lst[4], data_lst[5], data_lst[6], data_lst[7], data_lst[9], data_lst[11]]
					if '' in data_lst:
						for i in range(len(data_lst)):
							if data_lst[i] == '':
								data_lst[i] = round(sum(training_data[keys[i]])/len(training_data[keys[i]]), 3)
			if '' not in data_lst:
				for i in range(len(data_lst)):
					# Train [Survived, Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]
					# Test [Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]
					if i == start-1 and start-1 >= 0:
						# Survived
						data[keys[i]].append(int(data_lst[i]))
					elif i == start:
						# Pclass
						data[keys[i]].append(int(data_lst[i]))
					elif i == start+1:
						# Sex
						if data_lst[i] == 'male':
							data[keys[i]].append(1)
						else:
							data[keys[i]].append(0)
					elif i == start+2:
						# Age
						data[keys[i]].append(float(data_lst[i]))
					elif i == start+3:
						# SibSp
						data[keys[i]].append(int(data_lst[i]))
					elif i == start+4:
						# Parch
						data[keys[i]].append(int(data_lst[i]))
					elif i == start+5:
						# Fare
						data[keys[i]].append(float(data_lst[i]))
					elif i == start+6:
						# Embarked
						if data_lst[i] == 'S':
							data[keys[i]].append(0)
						elif data_lst[i] == 'C':
							data[keys[i]].append(1)
						else:
							data[keys[i]].append(2)

	return data


def one_hot_encoding(data: dict, feature: str):
	"""
	:param data: dict[str, list], key is the column name, value is its data
	:param feature: str, the column name of interest
	:return data: dict[str, list], remove the feature column and add its one-hot encoding features
	"""
	if feature == 'Sex':
		Sex_0 = []
		Sex_1 = []
		for i in data['Sex']:
			if i == 0:
				Sex_0.append(1)
				Sex_1.append(0)
			else:
				Sex_0.append(0)
				Sex_1.append(1)
		data['Sex_0'] = Sex_0
		data['Sex_1'] = Sex_1
		data.pop('Sex')
	elif feature == 'Pclass':
		Pclass_0 = []
		Pclass_1 = []
		Pclass_2 = []
		for i in data['Pclass']:
			if i == 1:
				Pclass_0.append(1)
				Pclass_1.append(0)
				Pclass_2.append(0)
			elif i == 2:
				Pclass_0.append(0)
				Pclass_1.append(1)
				Pclass_2.append(0)
			else:
				Pclass_0.append(0)
				Pclass_1.append(0)
				Pclass_2.append(1)
		data['Pclass_0'] = Pclass_0
		data['Pclass_1'] = Pclass_1
		data['Pclass_2'] = Pclass_2
		data.pop('Pclass')

	elif feature == 'Embarked':
		Embarked_0 = []
		Embarked_1 = []
		Embarked_2 = []
		for i in data['Embarked']:
			if i == 0:
				Embarked_0.append(1)
				Embarked_1.append(0)
				Embarked_2.append(0)
			elif i == 1:
				Embarked_0.append(0)
				Embarked_1.append(1)
				Embarked_2.append(0)
			else:
				Embarked_0.append(0)
				Embarked_1.append(0)
				Embarked_2.append(1)
		data['Embarked_0'] = Embarked_0
		data['Embarked_1'] = Embarked_1
		data['Embarked_2'] = Embarked_2
		data.pop('Embarked')

	return data


def normalize(data: dict):
	"""
	:param data: dict[str, list], key is the column name, value is its data
	:return data: dict[str, list], key is the column name, value is its normalized data
	"""
	for key, lst in data.items():
		new_lst = []
		for x in lst:
			new_x = (x-min(lst))/(max(lst)-min(lst))
			new_lst.append(new_x)
		data[key] = new_lst

	return data


def learnPredictor(inputs: dict, labels: list, degree: int, num_epochs: int, alpha: float):
	"""
	:param inputs: dict[str, list], key is the column name, value is its data
	:param labels: list[int], indicating the true label for each data
	:param degree: int, degree of polynomial features
	:param num_epochs: int, the number of epochs for training
	:param alpha: float, known as step size or learning rate
	:return weights: dict[str, float], feature name and its weight
	"""
	# Step 1 : Initialize weights
	weights = {}  # feature => weight
	keys = list(inputs.keys())

	if degree == 1:
		for i in range(len(keys)):
			weights[keys[i]] = 0
	elif degree == 2:
		for i in range(len(keys)):
			weights[keys[i]] = 0
		for i in range(len(keys)):
			for j in range(i, len(keys)):
				weights[keys[i] + keys[j]] = 0

	# Step 2 : Start training

	# Step 3 : Feature Extract
	if degree == 1:
		new_inputs = {}
		for num in range(len(labels)):
			inputs_d1 = {}
			for j in range(len(keys)):
				inputs_d1[keys[j]] = inputs[keys[j]][num]
			new_inputs[num] = inputs_d1

	elif degree == 2:
		new_inputs = {}
		for num in range(len(labels)): #712
			inputs_d2 = {}
			for i in range(len(keys)):
				for j in range(i, len(keys)):
					inputs_d2[keys[i] + keys[j]] = inputs[keys[i]][num]*inputs[keys[j]][num]
				inputs_d2[keys[i]] = inputs[keys[i]][num]
			new_inputs[num] = inputs_d2

	# Step 4 : Update weights

	for epoch in range(num_epochs):
		for num in range(len(labels)):
			k = util.dotProduct(weights, new_inputs[num])
			h = 1 / (1 + math.exp(-k))
			scale = - alpha * (h - labels[num])
			util.increment(weights, scale, new_inputs[num])

	return weights
