import psycopg2

conn = psycopg2.connect("user="+input("username: ")+" password="+input("password: ")+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()

#cursor.execute("insert into test values (%s, %s)", (102, "abcdef"))
cursor.execute("select * from test;")
print(cursor.fetchone())

cursor.close()
conn.close()
