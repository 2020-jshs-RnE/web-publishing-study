# xml files mergine code

mf = open("D:/rne/mergingxml/wxxxmlf.xml",'w',encoding='utf8')

i = 0

while 1:
    try:
        tf = open('D:/RnE/mergingxml/txml{}.xml'.format(i),'r',encoding='utf8')
    except:
        print('Finished exploring Files')
        break

    print(tf.read(), file=mf)
    i += 1

mf.close()
