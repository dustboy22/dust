def interpret(text):
	text = text.split("\n")
	text.insert(0, "<br></br>")
	for line in text:
		line += "<br></br>"

	print(text)

	text = "".join(text)

	print(text)

	return text[0]