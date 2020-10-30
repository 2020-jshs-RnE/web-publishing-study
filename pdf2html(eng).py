import camelot
file = "C:/Users/sjshb/Desktop/js/테스트.pdf"
tables = camelot.read_pdf(file)
#print(tables[0].df)
tables.export("C:/Users/sjshb/Desktop/js/테스트.html", f = "html")