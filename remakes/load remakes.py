import xml.etree.ElementTree
import psycopg2
import sys

remakes = xml.etree.ElementTree.parse('remakes.xml').getroot()

username = input("username: ")
password = input("password: ")
conn = psycopg2.connect("user="+username+" password="+password+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from remakes;')

for remake in remakes:

    original_film_id = None
    remake_film_id = None
    similarity = None

    for field in remake:
        if field.tag == 'sid': original_film_id = field.text
        if field.tag == 'rid': remake_film_id = field.text
        if field.tag == 'frac': similarity = field.text.replace(' ','')
    
    try:
        cursor.execute("insert into remakes values (%s, %s, %s)",
            (original_film_id, remake_film_id, similarity))
    except:
        print(sys.exc_info()[1])

cursor.close()
conn.close()
