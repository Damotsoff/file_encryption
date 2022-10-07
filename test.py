import psycopg2
conn = psycopg2.connect(dbname='testdb',user='postgres',password='12345',host='localhost')
cursor =conn.cursor()
lg = 'alex'
pas= '12313ssd'
# cursor.execute("INSERT INTO users(login,password) VALUES(%s,%s)",(lg,pas))
cursor.execute('select  login from users where login=%s;',(lg,))
result = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()
print(result)