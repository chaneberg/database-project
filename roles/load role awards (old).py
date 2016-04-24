import xml.etree.ElementTree
import psycopg2
import sys

casts = xml.etree.ElementTree.parse('casts.xml').getroot()

username = input("username: ")
password = input("password: ")
conn = psycopg2.connect("user="+username+" password="+password+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from role_awards;')

for dirfilms in casts:
    for filmc in dirfilms:
        if filmc.tag == 'filmc':
            for m in filmc:
    
                film_id = None
                person_id = None

                for field in m:
                    if field.tag == 'f': film_id = field.text
                    if field.tag == 'a': person_id = field.text

                    if field.tag == 'awards':
                        for award in field:
                            award_code = award.text
                
                            try:
                                cursor.execute("insert into role_awards values (%s, %s, %s)", (film_id, person_id, award_code))
                            except:
                                print(sys.exc_info()[1])

cursor.close()
conn.close()
