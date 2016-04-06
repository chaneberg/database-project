import xml.etree.ElementTree
import psycopg2
import sys

movies = xml.etree.ElementTree.parse('movies.xml').getroot()

conn = psycopg2.connect("user="+input("username: ")+" password="+input("password: ")+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from produced;')

for directorfilms in movies:
    films = directorfilms[1]
    for film in films:
        
        film_id = None

        for field in film:
            
            if field.tag == 'fid':
                film_id = field.text

            if field.tag == 'prods':
                for prod in field:
                    if prod.tag == 'prod':
                        
                        person_id = None
                        
                        for pname in prod:
                            if pname.tag == 'pname':
                                person_id = pname.text

                        try:
                            cursor.execute("insert into produced values (%s, %s)", (film_id, person_id))
                        except:
                            print(sys.exc_info()[1])

cursor.close()
conn.close()
