

mf = open('merged_file.json','w',encoding='utf8')

i = 0

while 1:
    try:
        tf = open('test{}.json'.format(i),'r',encoding='utf8')
    except:
        print('Finished exploring Files')
        break

    print(tf.read(), file=mf)
    i += 1

mf.close()

