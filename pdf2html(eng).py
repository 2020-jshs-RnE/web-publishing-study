import camelot
file = "경로.pdf"
tables = camelot.read_pdf(file)
#print(tables[0].df)
tables.export("경로.html", f = "html")
