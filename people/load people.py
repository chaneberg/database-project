import xml.etree.ElementTree
import psycopg2
import sys
import re

def extractDate(date):
    if not date: return None
    match = re.search('[0-9][0-9][0-9][0-9]', date)
    if not match: return None
    return match.group()

valid_country_codes = {"USA": "Am", "America": "Am", "United States": "Am", "US": "Am", "United States of America": "Am",
                       "Britain": "Br", "GB": "Br", "Great Britain": "Br", "France": "Fr", "Germany": "Ge", "Italy": "It",
                       "Japan": "Ja", "Argentinia": "Ar", "Australia": "Au", "Belgium": "Be", "Brazil": "Bz", "Canada": "Ca",
                       "China": "Ch", "People's Republic of China": "Ch", "PRC": "Ch", "Czechoslovakia": "Cz",
                       "Denmark": "Da", "Greece": "Gr", "Holland": "Du", "Hungary": "Hu", "India": "In", "Ireland": "Ir",
                       "Mexico": "Me", "Austria": "Os", "Peru": "Pe", "USSR": "Ru", "Russia": "Ru", "Spain": "Sp",
                       "South-Africa": "SA", "South Africa": "SA", "Yugoslavia": "Yu", "Switzerland": "Zw"}

people = xml.etree.ElementTree.parse('people.xml').getroot()
actors = xml.etree.ElementTree.parse('actors.xml').getroot()

username = 'chaneberg13'#input("username: ")
password = 'xdch456'#input("password: ")
conn = psycopg2.connect("user="+username+" password="+password+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from people;')

for person in people:
    
    person_id = None
    first_name = None
    last_name = None
    stage_name = None
    birth_date = None
    death_date = None
    work_start_date = None
    work_end_date = None
    gender = None
    typical_role = None
    country_code = None

    for field in person:
        if field.tag == 'pname': person_id = field.text
        if field.tag == 'givennm': first_name = field.text
        if field.tag == 'familynm': last_name = field.text

        if field.tag == 'dob': birth_date = extractDate(field.text)
        if field.tag == 'dod': death_date = extractDate(field.text)
        if (field.tag == 'yeardirstart' or field.tag == 'yearstart') and extractDate(field.text): work_start_date = extractDate(field.text)
        if field.tag == 'yearend': work_end_date = extractDate(field.text)

        if field.tag == 'background' and field.text and field.text[1:] in valid_country_codes.values(): country_code = field.text[1:]
        
    
    try:
        cursor.execute("insert into people values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (person_id, first_name, last_name, stage_name, birth_date, death_date, work_start_date, work_end_date, gender, typical_role, country_code))
    except:
        print(sys.exc_info()[1])

for actor in actors:
    
    person_id = None
    first_name = None
    last_name = None
    stage_name = None
    birth_date = None
    death_date = None
    work_start_date = None
    work_end_date = None
    gender = None
    typical_role = None
    country_code = None

    for field in actor:
        if field.tag == 'stagename': person_id = field.text
        if field.tag == 'firstname': first_name = field.text
        if field.tag == 'familyname': last_name = field.text
        #if field.tag == 'stagename': stage_name = field.text

        if field.tag == 'dob': birth_date = extractDate(field.text)
        if field.tag == 'dod': death_date = extractDate(field.text)
        if field.tag == 'dowstart': work_start_date = extractDate(field.text)
        if field.tag == 'dowend': work_end_date = extractDate(field.text)

        if field.tag == 'gender' and field.text in ['M','F']: gender = field.text
        if field.tag == 'roletype' and field.text != 'unknown': typical_role = field.text
        if field.tag == 'origin' and field.text and field.text[1:] in valid_country_codes.values(): country_code = field.text[1:]
    
    name = person_id.split(' ')
    if not first_name and name:
        first_name = name[0]
    if not last_name and name and len(name) >= 2:
        last_name = name[1]

    if first_name and last_name and person_id != first_name+' '+last_name:
        stage_name = person_id
    
    try:
        cursor.execute("insert into people values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (person_id, first_name, last_name, stage_name, birth_date, death_date, work_start_date, work_end_date, gender, typical_role, country_code))
    except:
        print(sys.exc_info()[1])

cursor.close()
conn.close()
