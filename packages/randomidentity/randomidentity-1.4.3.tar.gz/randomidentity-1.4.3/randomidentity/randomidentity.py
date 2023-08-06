import random

from .data import *

names_count = len(names) - 1
surnames_count = len(surnames) - 1
streets_num_count = len(streets_num) - 1
streets_count = len(streets) - 1
city_count = len(city) - 1
postcode_count = len(postcode) - 1
num_code_count = len(num_code) - 1


def identity(count: int = 1):
	"""This function returns random data of people that you can use in your projects."""
	if count > 0:
		while count > 0:
			return '\n' + names[random.randint(0, names_count)] + ' ' + surnames[random.randint(0, surnames_count)] + '\n' + streets_num[random.randint(0, streets_num_count)] + ' ' + streets[random.randint(0, surnames_count)] + '\n' + city[random.randint(0, city_count)] + ', ' + postcode[random.randint(0, postcode_count)] + '\n' +  f'({num_code[random.randint(0,num_code_count)]}) xxx-xxxx'
			count = count - 1
	if count < 0:
		print('[ERR] Please write a number greater than 0')
	if count == 0:
		pass
