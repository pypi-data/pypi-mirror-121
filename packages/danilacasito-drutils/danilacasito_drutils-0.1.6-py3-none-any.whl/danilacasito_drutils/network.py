import requests
def checkInternet():
	try:
		requests.get("https://google.com")
		eplo = True
	except requests.exceptions.ConnectionError:
		eplo = False
	return eplo