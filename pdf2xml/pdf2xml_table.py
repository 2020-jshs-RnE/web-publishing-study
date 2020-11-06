import pdftables_api
import os

c = pdftables_api.Client('API_KEYS')

file_path = "D:/RnE/xmltable/"

for file in os.listdir(file_path):
    if file.endswith(".pdf"):
        c.xml(os.path.join(file_path,file), file+'.xml')