import xml.etree.ElementTree
import psycopg2
import sys

movies = xml.etree.ElementTree.parse('movies.xml').getroot()

conn = psycopg2.connect("user="+input("username: ")+" password="+input("password: ")+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from sponsored;')

for directorfilms in movies:
    films = directorfilms[1]
    for film in films:
        
        film_id = None

        for field in film:
            
            if field.tag == 'fid':
                film_id = field.text

            if field.tag == 'studios':
                for studio in field:
                    if studio.tag == 'studio':
                        
                        studio_name = studio.text

                        try:
                            cursor.execute("insert into sponsored values (%s, %s)", (film_id, studio_name))
                        except:
                            print(sys.exc_info()[1])

cursor.close()
conn.close()
