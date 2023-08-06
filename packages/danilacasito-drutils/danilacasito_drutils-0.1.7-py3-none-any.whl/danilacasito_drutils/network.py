import requests
def checkInternet():
	"""
	Checks if you have internet, if yes, returns True, otherwise, it returns False
	"""
	try:
		requests.get("https://google.com")
		eplo = True
	except requests.exceptions.ConnectionError:
		eplo = False
	return eplo