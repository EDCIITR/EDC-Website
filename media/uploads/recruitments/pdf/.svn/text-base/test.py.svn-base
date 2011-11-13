import ho.pisa as pisa

def helloWorld():
	filename = __file__ + ".pdf"
	pdf = pisa.CreatePDF("Hello <strong>World</strong>",file(filename, "wb"))

	if not pdf.err:
		pisa.startViewer(filename)

if __name__=="__main__":
	pisa.showLogging()

helloWorld()

