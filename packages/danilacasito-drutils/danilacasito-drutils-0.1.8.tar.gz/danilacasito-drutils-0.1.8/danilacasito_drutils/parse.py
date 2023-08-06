def argparse(text):
	"""
	Parses all the arguments of the text that you pass in the first argument and returns a list with your arguments separated
	
	Example:
		parser.argparse('"Hello" "World" "How are you"')

	With the example, it should return:
		["Hello", "World", "How are you"]
	"""
	sho = False
	args = []
	e = []
	temparg = ""
	for i in text:
		if sho:
			if i == '"' or i == "'":
				sho = False
				args.append(temparg)
			if sho:
				temparg = temparg+i

		if not sho:
			temparg = ""
			if i == '"' or i == "'":
				sho = True
		
	for i in args:
		if i != ' ':
			e.append(i)
	return e