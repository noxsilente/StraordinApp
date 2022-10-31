import sqlite3

conn = sqlite3.connect('Straordinari.db')
curs = conn.cursor()
#curs.execute('DELETE FROM straordinari WHERE mm=\'2\n\'')
#curs.execute('UPDATE straordinari SET ora=\'.5\n\'WHERE gg=\'20\' AND mm=\'01\'')
curs.execute('SELECT * FROM straordinari ORDER BY CAST(gg AS INTEGER)')
conn.commit()
##lista = []
##for row in curs.execute('SELECT * FROM straordinari WHERE mm=10 ORDER BY CAST(gg AS INTEGER)'):
##        data=(row[0],row[1],row[2])
##        print(type(data))
##        lista.append(data)
##print(lista)
##print('******************')
#for row in curs.execute('UPDATE straordinari SET ):
#for row in curs.execute('SELECT gg,mm,ora FROM straordinari '):
#        print (row)
#print('----------------------------------------------------')
#curs.execute('DELETE FROM straordinari WHERE mm=10')
#for row in curs.execute('SELECT gg,mm,ora FROM straordinari '):
#        print (row)
##print('----------------------------------------------------')
##for i in lista:
##        curs.execute('INSERT INTO straordinari VALUES (?,?,?)', i)
##conn.commit()
for row in curs.execute('SELECT gg,mm,ora FROM straordinari '):
        print (row)
