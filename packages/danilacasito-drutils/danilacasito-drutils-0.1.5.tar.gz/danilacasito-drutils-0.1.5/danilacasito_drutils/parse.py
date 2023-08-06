def argparse(text):
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