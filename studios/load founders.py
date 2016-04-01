import psycopg2
import sys

founders = [('20th Cent.', 'Darryl Zanuck'), ('35mm Film Camera', 'Thomas Edison'), ('AFM', 'Alan Dwan'), 
('Ambrosio', 'Arturo Ambrosio'), ('ARC', 'Samuel Z. Arkoff'), ('ARC', 'James Nicholson'), 
('ATP', 'Basil Dean'), ('Carosse', 'Truffaut'), ('CastleRock', 'Rob Reiner'), ('Chaplin', 'Chaplin'), 
('Cineromans', 'Gaston Leroux'), ('Cineromans', 'Rene Navarre'), ('Cinetone', 'Rudolf Meyer'), 
('Dimension', 'Disney'), ('Edison', 'Thomas Edison'), ('ENSA', 'Basil Dean'), ('Essanay', 'G.M. Anderson'), 
('Essexe', 'Frank Sinatra'), ('Famous', 'Adolph Zukor'), ('Fantasy', 'Saul Saentz'), 
('Feature Play', 'Lasky'), ('Feature Play', 'DeMille'), ('Feature Play', 'Goldwyn'), 
('Film Camera', 'W. Friese-Greene'), ('Film House', 'Schepisi'), ('FilmMakers', 'Ida Lupino'), 
('FilmMakers', 'Collier Young'), ('First National', 'J.D. Williams'), ('Gainsborough', 'Balcon'), 
('Gainsborough', 'Saville'), ('Goldwyn', 'Sam Goldwyn'), ('Gracie', 'J.L. Brooks'), 
('Granada', 'Sid Bernstein'), ('Graniet', 'van Warmerdam'), ('Gregory', 'Ian Courts'), 
('IMP', 'Carl Laemmle'), ('Jagged', 'Mick Jagger'), ('Kinetoscope', 'Thomas Edison'), ('Korda', 'Korda'), 
('L\'anorthoscope', 'Plateau'), ('Lee Rich', 'Lee Rich'), ('Life Projection Wheel?', 'E. Muybridge'), 
('LionsGate', 'Mark Urman'), ('London Films', 'Alex Korda'), ('Lorimar', 'Lee Rich'), 
('Lubitsch', 'Ernst Lubitsch'), ('Malpaso', 'Clint Eastwood'), ('MGM', 'Bought Loews'), 
('MGM-U.A', 'Kirk Kerkorian'), ('Miramax', 'Weinstein'), ('NEF', 'J. Renoir'), ('NEF', 'Andre Zwobada'), 
('NEF', 'Camille Froancois'), ('NEF', 'Olivier Billiou'), ('NEF', 'C. Renoir'), ('NWP', 'Corman'), 
('Paramount', 'William Wadworth Hodkinson'), ('Pathe 2', 'Pathe'), ('Paulist', 'Ellwood Bud Kieser'), 
('Ph\`enakistiscope', 'Plateau'), ('Phakinescope', 'Abadie Dutemps'), 
('Phenakistiscope', 'Charles Chevalier'), ('Photobioscope', 'Bonnelliot'), 
('Photobioscope', 'Henry Cook'), ('Pickford', 'Mary Pickford'), ('Pixar', 'Steve Jobs'), 
('Pocket Kinematograph', 'J.B. Linnett'), ('Practical Projectors', 'Louis Lumiere'), 
('Practical Projectors', 'August Lumiere'), ('Praxinoscope', 'Emile Reynaud'), 
('Projection-Praxinoscope', 'Ch-E. Reynaud'), ('RealArt', 'James Nicholson'), 
('Regency', 'Arnon Milchan'), ('Republic', 'Herbert J. Yates'), ('Roach', 'Hal Roach'), 
('Schnellseher', 'O. Anschutz'), ('Selig Polyscope', 'William N. Selig'), 
('Skladanowsky', 'M. Skladanowsky'), ('Skladanowsky', 'E. Skladanowsky'), 
('Stereo-Praxinoscope', 'Emile Reynaud'), ('Thaumatrope', 'Docteur Pan'), ('Transatlantic', 'Bernstein'), 
('Transatlantic', 'Hitchcock'), ('Triangle', 'Harry Aitkins'), ('Triangle', 'Griffith'), 
('Triangle', 'Ince'), ('Triangle', 'Mark Sennett'), ('TriStar', 'Columbia'), ('Turner', 'Ted Turner'), 
('U.A.', 'Chaplin'), ('U.A.', 'Pickford'), ('U.A.', 'Fairbanks'), ('U.A.', 'Griffith'), 
('Universal', 'Carl Laemmle'), ('Victory', 'Balcon'), ('Victory', 'Saville'), 
('Vitascope? Projectors', 'W. Latham'), ('Vivid', 'Steven Hirsch'), ('Woodfall', 'Saltzman'), 
('Woodfall', 'Tony Richardson'), ('Woodfall', 'John Osborne'), ('Zoetrope', 'Francis Ford Coppola'), 
('Zoetrope', 'George Lucas')]

username = input("username: ")
password = input("password: ")
conn = psycopg2.connect("user="+username+" password="+password+" host=dhansen.cs.georgefox.edu dbname=fmdb")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('delete from founded;')

for pair in founders:

    studio_name = pair[0]
    personName = pair[1]
    personNameSplit = personName.split(' ')
    first_name = personNameSplit[0] if len(personNameSplit) > 1 else None
    last_name = personNameSplit[len(personNameSplit) - 1]

    print(personName)
    print(first_name, last_name)
    sql = "select * from people where person_id like '%"+last_name[:5]+"%' or last_name like '"+last_name[:5]+"%'"
    print(sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for record in result:
            print(record)
    except:
        print(sys.exc_info()[1])
    inp = input("enter id to use: ")
    person_id = result[int(inp)-1][0] if inp.isdigit() else inp

    try:
        print(cursor.mogrify("insert into people values (%s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (person_id, first_name, last_name)))
        cursor.execute("insert into people values (%s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (person_id, first_name, last_name))
    except:
        print(sys.exc_info()[1])
    
    try:
        print(cursor.mogrify("insert into founded values (%s, %s)", (studio_name, person_id)))
        cursor.execute("insert into founded values (%s, %s)", (studio_name, person_id))
    except:
        print(sys.exc_info()[1])

    print()

cursor.close()
conn.close()
