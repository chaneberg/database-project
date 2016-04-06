import xml.etree.ElementTree
import psycopg2
import sys

movies = xml.etree.ElementTree.parse('movies.xml').getroot()

conn = psycopg2.connect("user="+input("username: ")+" password="+input("password: ")+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from directed;')

for directorfilms in movies:
    films = directorfilms[1]
    for film in films:
        
        film_id = None

        for field in film:
            
            if field.tag == 'fid':
                film_id = field.text

            if field.tag == 'dirs':
                for dir_ in field:
                    if dir_.tag == 'dir':
                        
                        person_id = None
                        
                        for dirn in dir_:
                            if dirn.tag == 'dirn':
                                person_id = dirn.text

                        try:
                            cursor.execute("insert into directed values (%s, %s)", (film_id, person_id))
                        except:
                            print(sys.exc_info()[1])

cursor.close()
conn.close()
