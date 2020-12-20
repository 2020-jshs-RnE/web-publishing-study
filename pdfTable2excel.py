import tabula
df = tabula.read_pdf('C:/Users/sjshb/Desktop/제곽/정보 관련/web-publishing-study-main/테스트용 표.pdf', pages = 1, lattice = True)[0] #절대경로써야됨

df.columns = df.columns.str.replace('\r', ' ')
data = df
data.to_excel('C:/Users/sjshb/Desktop/제곽/정보 관련/web-publishing-study-main/테스트용 표.xlsx')   #절대경로써야됨