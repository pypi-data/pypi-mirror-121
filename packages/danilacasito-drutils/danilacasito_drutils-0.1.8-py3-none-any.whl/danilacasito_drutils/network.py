import requests
def checkInternet():
	"""
	Checks if you have internet, if yes, returns True, otherwise, it returns False
	usage:
		network.checkInternet()

	"""
	try:
		requests.get("https://google.com")
		eplo = True
	except requests.exceptions.ConnectionError:
		eplo = False
	return eplo
def getReturnCode(url):
	"""
	Makes a request to the specified url and returns you the code
	usage:
		network.getReturnCode("https://google.es")

	it returns a string with the return code
	"""
	r = requests.get(url)
	return str(r.code)
