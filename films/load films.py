import xml.etree.ElementTree
import psycopg2
import sys

valid_category_codes = ['Susp', 'CnR', 'Dram', 'West', 'Myst', 'S.F.', 'Advt', 'Horr', 'Romt', 'Comd', 'Musc', 'Docu',
                        'Porn', 'Noir', 'BioP', 'TV', 'TVs', 'TVm']
valid_country_codes = {"USA": "Am", "America": "Am", "United States": "Am", "US": "Am", "United States of America": "Am",
                       "Britain": "Br", "GB": "Br", "Great Britain": "Br", "France": "Fr", "Germany": "Ge", "Italy": "It",
                       "Japan": "Ja", "Argentinia": "Ar", "Australia": "Au", "Belgium": "Be", "Brazil": "Bz", "Canada": "Ca",
                       "China": "Ch", "People's Republic of China": "Ch", "PRC": "Ch", "Czechoslovakia": "Cz",
                       "Denmark": "Da", "Greece": "Gr", "Holland": "Du", "Hungary": "Hu", "India": "In", "Ireland": "Ir",
                       "Mexico": "Me", "Austria": "Os", "Peru": "Pe", "USSR": "Ru", "Russia": "Ru", "Spain": "Sp",
                       "South-Africa": "SA", "South Africa": "SA", "Yugoslavia": "Yu", "Switzerland": "Zw"}

movies = xml.etree.ElementTree.parse('movies.xml').getroot()

conn = psycopg2.connect("user="+input("username: ")+" password="+input("password: ")+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from films;')

#directorfilms = movies[0]
#films = directorfilms[1]
#film = films[0]

for directorfilms in movies:
    films = directorfilms[1]
    for film in films:
        
        film_id = None
        title = None
        year = None
        category_code = None
        country_code = None

        for field in film:
            #print(field.tag,'=',field.text)
            
            if field.tag == 'fid':
                film_id = field.text
            if field.tag == 't' and field.text:
                title = field.text[:256]
            if field.tag == 'year' and field.text.isdigit():
                year = field.text
            if field.tag == 'cats':
                for cat in field:
                    if cat.tag == 'cat' and cat.text in valid_category_codes:
                        category_code = cat.text
            if field.tag == 'loc':
                for site in field:
                    if site.tag == 'site':
                        for siteplace in site:
                            if siteplace.tag == 'siteplace':
                                if siteplace.text in valid_country_codes.values():
                                    country_code = siteplace.text
                                elif siteplace.text in valid_country_codes:
                                    country_code = valid_country_codes[siteplace.text]

        #print("insert into films values ("+film_id+", "+title+", "+year+", "+category_code+", "+country_code+");")
        try:
            cursor.execute("insert into films values (%s, %s, %s, %s, %s)", (film_id, title, year, category_code, country_code))
            #conn.commit()
        except:
            print(sys.exc_info()[1])

cursor.close()
conn.close()
