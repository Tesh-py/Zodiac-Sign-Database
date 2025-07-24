#document/step one
import csv
import json
import xml.etree.ElementTree as ET
import sqlite3
import requests

#running through the api takes a while
print('Please wait while the code is running. This may take a moment.')

api_key = 'hG8W4rt2KxooBrzd2EwgCQ==0WWaQLwXJTjHwDed'
headers = {'X-Api-Key': api_key}

signs = [
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
]

all_horoscopes = {}
#suggested code from API Ninja to get daily horoscope
for sign in signs:
    url = f'https://api.api-ninjas.com/v1/horoscope?zodiac={sign}&day=today'
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        all_horoscopes[sign] = data['horoscope']
    else:
        print(f"Failed to get horoscope for {sign}: {response.status_code}")
#save url data into json document
with open('all_horoscopes.json', 'w', encoding='utf-8') as f:
    json.dump(all_horoscopes, f, indent=4)
print('all_horoscopes JSON file has been created')
#create dictionary from json data
with open('all_horoscopes.json', 'r',encoding='utf-8') as f:
    horoscopes = json.load(f)
#parse html to get the data
tree = ET.parse('zodiac_xml.xml')
root = tree.getroot()
#connect & create sqlite tables/database
conn = sqlite3.connect('zodiac.db')
cursor = conn.cursor()
#table created from html/json data
cursor.execute('''
CREATE TABLE IF NOT EXISTS Zodiac1 (
    sign TEXT PRIMARY KEY,
    horoscope TEXT
)
''')

for sign, text in horoscopes.items():
    cursor.execute('''
    INSERT OR REPLACE INTO Zodiac1 (sign, horoscope) VALUES (?, ?)
    ''', (sign, text))
print('html/JSON table created successfully')

#table created from csv data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Zodiac2 (
        name TEXT PRIMARY KEY,
        colour TEXT,
        element TEXT
    )
''')

with open('zodiac_csv.csv', 'r', newline='', encoding='utf-8-sig') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        cursor.execute('''
            INSERT OR REPLACE INTO Zodiac2 (name, colour, element) VALUES (?, ?, ?)
        ''', (row['name'], row['colour'], row['element']))
print('CSV table created successfully')

#table creates from xml data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Zodiac3 (
        name TEXT PRIMARY KEY,
        start_date TEXT,
        end_date TEXT,
        element TEXT,
        quality TEXT,
        planet TEXT
    )
''')

for sign in root.findall('zodiac_sign'):
    name = sign.attrib['name']
    start_date = sign.attrib['start_date']
    end_date = sign.attrib['end_date']
    element = sign.find('element').text
    quality = sign.find('quality').text
    planet = sign.find('planet').text

    cursor.execute('''
        INSERT OR REPLACE INTO Zodiac3 (name, start_date, end_date, element, quality, planet)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, start_date, end_date, element, quality, planet))
print('XML table created successfully')

conn.commit()
conn.close()
