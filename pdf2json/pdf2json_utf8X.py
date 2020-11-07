from tabula import read_pdf, convert_into


files = ["D:/RnE/xmltable/qew.pdf","D:/RnE/xmltable/d.pdf"]

# for i in files:

#     print(read_pdf(i,output_format="json"))
#     convert_into(i,"D:/RnE/jsontable/testcase.json",output_format="json")

for i in files:

    # f = open("test.json","w",encoding="utf8")
    # rorkxsp = read_pdf(i,output_format="json")
    
    
    # rorkxsp = str(rorkxsp).replace("\'","\"")

    # print(rorkxsp)
    # tjfak = []
    # tjfak.append(rorkxsp)
    convert_into(i,"D:/RnE/jsontable/testcase{}.json".format(files.index(i)),output_format="json")
    # print(tjfak, type(tjfak))

    # f.close()
