import random

from .data import *

names_count = len(names) - 1
surnames_count = len(surnames) - 1
streets_num_count = len(streets_num) - 1
streets_count = len(streets) - 1
cities_count = len(cities) - 1
postal_codes_count = len(postal_codes) - 1
num_code_count = len(num_code) - 1


def identity():
	"""This function returns random data of people that you can use in your projects."""
	return '\n' + names[random.randint(0, names_count)] + ' ' + surnames[random.randint(0, surnames_count)] + '\n' + streets_num[random.randint(0, streets_num_count)] + ' ' + streets[random.randint(0, surnames_count)] + '\n' + cities[random.randint(0, cities_count)] + ', ' + postal_codes[random.randint(0, postal_codes_count)] + '\n' +  f'({num_code[random.randint(0,num_code_count)]}) xxx-xxxx'


def name():
	"""This function returns random name that you can use in your projects."""
	return names[random.randint(0, names_count)]


def surname():
	"""This function returns random surname that you can use in your projects."""
	return surnames[random.randint(0, surnames_count)]


def street():
	"""This function returns random street that you can use in your projects."""
	return streets[random.randint(0, streets_count)]


def city():
	"""This function returns random city that you can use in your projects."""
	return cities[random.randint(0, cities_count)]


def postcode():
	"""This function returns random postcode that you can use in your projects."""
	return postal_codes[random.randint(0, postal_codes_count)]