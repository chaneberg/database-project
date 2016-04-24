import xml.etree.ElementTree
import psycopg2
import sys

casts = xml.etree.ElementTree.parse('casts.xml').getroot()

username = input("username: ")
password = input("password: ")
conn = psycopg2.connect("user="+username+" password="+password+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from roles;')
cursor.execute('delete from role_awards;')

errorCount = 0

for dirfilms in casts:
    for filmc in dirfilms:
        if filmc.tag == 'filmc':
            role_id = 0
            for m in filmc:
    
                film_id = None
                person_id = None
                role_type_code = None
                role_description = None
                character_name = None

                for field in m:
                    if field.tag == 'f': film_id = field.text
                    if field.tag == 'a': person_id = field.text
                    if field.tag == 'p' and field.text != 'Und': role_type_code = field.text
                    if field.tag == 'r': role_description = field.text
                    if field.tag == 'n': character_name = field.text
                
                try:
                    cursor.execute("insert into roles values (%s, %s, %s, %s, %s, %s)",
                        (film_id, person_id, role_id + 1, role_type_code, role_description, character_name))
                    role_id += 1
                except:
                    print(sys.exc_info()[1])
                    errorCount += 1

                for field in m:
                    if field.tag == 'awards':
                        for award in field:
                            award_code = award.text
                
                            try:
                                cursor.execute("insert into role_awards values (%s, %s, %s, %s)", (film_id, person_id, role_id, award_code))
                            except:
                                print(sys.exc_info()[1])

cursor.close()
conn.close()

print(errorCount,'errors')
