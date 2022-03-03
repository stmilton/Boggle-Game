"""
File: boggle.py

"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
from typing import List

FILE = 'dictionary.txt'
ABC = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x','y', 'z']
dict = {}
dict_lst = []


def main():
	"""
	TODO:
	"""
	read_dictionary()
	lst = []
	word_lst = []
	for i in range(4):
		word = input(str(i+1) + ' row of letters: ')
		word = word.lower()
		w = word.split()
		word_lst.append(w)
		if len(w) == 4 and len(w[0]) == 1 and len(w[1]) == 1 and len(w[2]) == 1 and len(w[3]) == 1:
			lst.append(w[0])
			lst.append(w[1])
			lst.append(w[2])
			lst.append(w[3])

		else:
			print('Illegal input')
			break

	if len(lst) == 16:
		find_boggle(word_lst)


def find_boggle(word_lst):
	all_lst = []
	for i in range(4):
		for j in range(4):
			helper(all_lst, word_lst, '', i, j)
	print('There are', len(all_lst), 'words in total.')


def helper(all_lst, word_lst, current, next_x, next_y):
	if len(current) >= 4 and current in dict_lst and current not in all_lst:
		all_lst.append(current)
		print('Found:', current)
		for x in range(-1, 2, 1):
			for y in range(-1, 2, 1):
				if 0 <= next_x + x < 4:
					if 0 <= next_y + y < 4:
						if x != 0 or y != 0:
							if word_lst[next_y + y][next_x + x] != '':
								k = word_lst[next_y][next_x]
								word_lst[next_y][next_x] = ''
								helper(all_lst, word_lst, current + k, next_x + x, next_y + y)
								word_lst[next_y][next_x] = k

	else:
		if has_prefix(current + word_lst[next_y][next_x]):
			for x in range(-1, 2, 1):
				for y in range(-1, 2, 1):
					if 0 <= next_x+x < 4:
						if 0 <= next_y+y < 4:
							if x != 0 or y != 0:
								if word_lst[next_y+y][next_x+x] != '':
									k = word_lst[next_y][next_x]
									word_lst[next_y][next_x] = ''
									helper(all_lst, word_lst, current+k, next_x+x, next_y+y)
									word_lst[next_y][next_x] = k


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	for letter in ABC:
		locals()['dict_lst_' + letter] = []
		dict[letter] = locals()['dict_lst_' + letter]
	with open(FILE, 'r') as f:
		for line in f:
			word = ''
			for i in range(len(line) - 1):
				word += line[i]
			locals()['dict_lst_' + word[0]].append(word)
			dict_lst.append(word)


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	# print(sub_s)
	x = dict[sub_s[0]]
	for i in x:
		if i.startswith(sub_s):
			return True
	return False


if __name__ == '__main__':
	main()
