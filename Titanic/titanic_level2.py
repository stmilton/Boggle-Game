"""
File: titanic_level2.py
Name: 
----------------------------------
This file builds a machine learning algorithm by pandas and sklearn libraries.
We'll be using pandas to read in dataset, store data into a DataFrame,
standardize the data by sklearn, and finally train the model and
test it on kaggle. Hyperparameters are hidden by the library!
This abstraction makes it easy to use but less flexible.
You should find a good model that surpasses 77% test accuracy on kaggle.
"""

import math
import pandas as pd
from sklearn import preprocessing, linear_model
TRAIN_FILE = 'titanic_data/train.csv'
TEST_FILE = 'titanic_data/test.csv'


def data_preprocess(filename, mode='Train', training_data=None):
	"""
	:param filename: str, the filename to be read into pandas
	:param mode: str, indicating the mode we are using (either Train or Test)
	:param training_data: DataFrame, a 2D data structure that looks like an excel worksheet
						  (You will only use this when mode == 'Test')
	:return: Tuple(data, labels), if the mode is 'Train'
			 data, if the mode is 'Test'
	"""
	data = pd.read_csv(filename)
	labels = None

	data.loc[data.Sex == 'male', 'Sex'] = 1
	data.loc[data.Sex == 'female', 'Sex'] = 0
	data.loc[data.Embarked == 'S', 'Embarked'] = 0
	data.loc[data.Embarked == 'C', 'Embarked'] = 1
	data.loc[data.Embarked == 'Q', 'Embarked'] = 2

	if mode == 'Train':
		data = data.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1).dropna()
		labels = data.pop('Survived')
		return data, labels

	elif mode == 'Test':
		data = data.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)
		data['Age'] = data['Age'].fillna(round(training_data['Age'].mean(), 3))
		data['Fare'] = data['Fare'].fillna(round(training_data['Fare'].mean(), 3))

		return data


def one_hot_encoding(data, feature):
	"""
	:param data: DataFrame, key is the column name, value is its data
	:param feature: str, the column name of interest
	:return data: DataFrame, remove the feature column and add its one-hot encoding features
	"""
	if feature == 'Sex':
		data['Sex_0'] = 0
		data.loc[data.Sex == 0, 'Sex_0'] = 1
		data['Sex_1'] = 0
		data.loc[data.Sex == 1, 'Sex_1'] = 1
		data.pop('Sex')

	elif feature == 'Pclass':
		data['Pclass_0'] = 0
		data.loc[data.Pclass == 1, 'Pclass_0'] = 1
		data['Pclass_1'] = 0
		data.loc[data.Pclass == 2, 'Pclass_1'] = 1
		data['Pclass_2'] = 0
		data.loc[data.Pclass == 3, 'Pclass_2'] = 1
		data.pop('Pclass')

	elif feature == 'Embarked':
		data['Embarked_0'] = 0
		data.loc[data.Embarked == 0, 'Pclass_0'] = 1
		data['Embarked_1'] = 0
		data.loc[data.Embarked == 1, 'Pclass_1'] = 1
		data['Embarked_2'] = 0
		data.loc[data.Embarked == 2, 'Pclass_2'] = 1
		data.pop('Embarked')

	return data


def standardization(data, mode='Train'):
	"""
	:param data: DataFrame, key is the column name, value is its data
	:param mode: str, indicating the mode we are using (either Train or Test)
	:return data: DataFrame, standardized features
	"""
	standardizer = preprocessing.StandardScaler()
	data = standardizer.fit_transform(data)

	return data


def main():
	"""
	You should call data_preprocess(), one_hot_encoding(), and
	standardization() on your training data. You should see ~80% accuracy
	on degree1; ~83% on degree2; ~87% on degree3.
	Please write down the accuracy for degree1, 2, and 3 respectively below
	(rounding accuracies to 8 decimals)
	TODO: real accuracy on degree1 -> 0.79634831
	TODO: real accuracy on degree2 -> 0.82865168
	TODO: real accuracy on degree3 -> 0.84831460
	"""

	training_data, labels = data_preprocess(TRAIN_FILE)
	testing_data = data_preprocess(TEST_FILE, mode='Test', training_data=training_data)

	training_data = one_hot_encoding(training_data, 'Sex')
	training_data = one_hot_encoding(training_data, 'Pclass')
	training_data = one_hot_encoding(training_data, 'Embarked')
	testing_data = one_hot_encoding(testing_data, 'Sex')
	testing_data = one_hot_encoding(testing_data, 'Pclass')
	testing_data = one_hot_encoding(testing_data, 'Embarked')

	poly = preprocessing.PolynomialFeatures(degree=3)
	training_data = poly.fit_transform(training_data)
	testing_data = poly.transform(testing_data)

	standardizer = preprocessing.StandardScaler()
	training_data = standardizer.fit_transform(training_data)
	testing_data = standardizer.transform(testing_data)

	h = linear_model.LogisticRegression(max_iter=10000)
	classifier = h.fit(training_data, labels)
	print(classifier.score(training_data, labels))

	predictions = classifier.predict(testing_data)
	print(predictions)





if __name__ == '__main__':
	main()
