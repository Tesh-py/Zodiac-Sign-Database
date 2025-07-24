#document/step 2
import sqlite3

conn = sqlite3.connect('zodiac.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS combined_zodiac;')
#combines all format tables together
cursor.execute("""
    CREATE TABLE combined_zodiac AS
    SELECT 
        z1.sign AS name,
        z1.horoscope,
        z2.colour,
        z3.element,
        z3.start_date,
        z3.end_date,
        z3.quality,
        z3.planet
    FROM Zodiac1 z1
    LEFT JOIN Zodiac2 z2 ON LOWER(TRIM(z1.sign)) = LOWER(TRIM(z2.name))
    LEFT JOIN Zodiac3 z3 ON LOWER(TRIM(z1.sign)) = LOWER(TRIM(z3.name));
""")
#lower ensures all lower case
#trim removes whitespaces
#AS changes data info word into a linking word as needed
#left join merges all tables even if there is missing info from 1 of the tables
conn.commit()
conn.close()
#give the user the keys/words to use
zodiac_options = [
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
]
print(f"Zodiac sign options: {zodiac_options}")

element_options = [
    'fire', 'earth', 'air', 'water'
]
print(f"Element options: {element_options}")

quality_options = [
    'cardinal', 'fixed','mutable'
]
print(f"Cardinal options: {quality_options}")

#retrieves all zodiac/horoscope info from consolidated table
def get_zodiac_info(zodiac_name):
    conn = sqlite3.connect('zodiac.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM combined_zodiac
        WHERE LOWER(TRIM(name)) = LOWER(TRIM(?));
    """, (zodiac_name,))
    result = cursor.fetchone()
    conn.close()
    return result
#retrieves all zodiacs of the chosen element
def get_by_element(element):
    conn = sqlite3.connect('zodiac.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM combined_zodiac
        WHERE LOWER(TRIM(element)) = LOWER(TRIM(?));
    """, (element,))
    results = cursor.fetchall()
    conn.close()
    return results
#retrieves all zodiacs of the chosen quality
def get_by_quality(quality):
    conn = sqlite3.connect('zodiac.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM combined_zodiac
        WHERE LOWER(TRIM(quality)) = LOWER(TRIM(?));
    """, (quality,))
    results = cursor.fetchall()
    conn.close()
    return results

#loop for user to select data wanted
def zodiac_page():
    while True:
        print("""
Please select an option from 1 to 4:
1. Get today's horoscope for your chosen Zodiac Sign
2. List Zodiac Signs based on an Element
3. List Zodiac Signs based on a Quality
4. Exit
              """)
        option = input('Enter your option (1-4): ').strip()
#1 is full zodiac/horoscope info
        if option == '1':
            user_zodiac = input('Enter your Zodiac Sign: ').strip().lower()
            daily_horoscope = get_zodiac_info(user_zodiac)
            if daily_horoscope:
                (name, horoscope, colour, element, start_date, end_date, quality, planet) = daily_horoscope
                print(f"""
{name.capitalize()}'s Horoscope for Today:
{horoscope}

Lucky Colour: {colour.capitalize()}
Element: {element.capitalize()}
Date Range: {start_date.capitalize()} - {end_date.capitalize()}
Quality: {quality.capitalize()}
Ruling Planet: {planet.capitalize()}
                """)
            else:
                print('Zodiac sign not found.')
#2 will list all zodiacs within the chosen element
        elif option == '2':
            element = input('Enter Element (fire, earth, air, water): ').strip().lower()
            users_elements = get_by_element(element)
            if users_elements:
                print(f"Zodiac Signs with element '{element}': {[s[0].capitalize() for s in users_elements]}")
            else:
                print('No Zodiac Signs found for that element.')
#3 will list all zodaiacs within the chosen quality
        elif option == '3':
            quality = input('Enter Quality (cardinal, fixed, mutable): ').strip().lower()
            users_qualities = get_by_quality(quality)
            if users_qualities:
                print(f"Zodiac Signs with quality '{quality}': {[s[0].capitalize() for s in users_qualities]}")
            else:
                print('No Zodiac Signs found for that quality.')
#4 allows the user to exit the loop
        elif option == '4':
            print('You will exit now.')
            break

        else:
            print('Invalid choice. Please enter a number between 1 and 4.')

if __name__ == '__main__':
    zodiac_page()
