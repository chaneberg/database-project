import xml.etree.ElementTree
import psycopg2
import sys
import re

movies = xml.etree.ElementTree.parse('movies.xml').getroot()

conn = psycopg2.connect("user="+input("username: ")+" password="+input("password: ")+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from film_awards;')

for directorfilms in movies:
    films = directorfilms[1]
    for film in films:
        
        film_id = None

        for field in film:
            
            if field.tag == 'fid':
                film_id = field.text

            if field.tag == 'awards':
                for aw in field:
                    if aw.tag == 'aw':
                        
                        awtype = None
                        awattr = None
                        award_code = None
                        
                        for aw_field in aw:
                            if aw_field.tag == 'awtype':
                                awtype = aw_field.text
                            if aw_field.tag == 'awattr':
                                awattr = aw_field.text

                        award_code = awtype
                        if (awtype == 'H' or awtype == 'Z') and awattr and re.search(r'^\*+$', awattr): award_code += awattr

                        try:
                            cursor.execute("insert into film_awards values (%s, %s)", (film_id, award_code))
                        except:
                            print(sys.exc_info()[1])

cursor.close()
conn.close()
