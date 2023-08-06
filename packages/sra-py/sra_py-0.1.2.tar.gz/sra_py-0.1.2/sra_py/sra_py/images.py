from .errors import *

import requests

SR = "https://some-random-api.ml"

def image(endpoint: str):
	try:
		r = requests.request("GET", f"{SR}/img/{endpoint}").json()
		return r["link"]
	except:
		raise NotFound(f"Endpoint \"{endpoint}\" not found")

def dog():
	return image('dog')

def cat():
	return image('cat')

def fox():
	return image('fox')

def panda():
	return image('panda')

def red_panda():
	return image('red_panda')

def bird():
	return image('birb')

def koala():
	return image('koala')

def pikachu():
	return image('pikachu')

def kangaroo():
	return image('kangaroo')

def racoon():
	return image('racoon')

def whale():
	return image('whale')