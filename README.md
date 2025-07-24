# Zodiac-Sign-Database
Data Aggregation Tool.
This application allows the user to retrieve data from multiple sources, capture all information into a database and then a consolidated database. From there the user can select prompts to pull information from the database.
The information pertains to Zodiac Signs.

API key is included in the python files to retrieve url information.

URL used: https://api.api-ninjas.com/v1/horoscope?zodiac={sign}&day=today

The following third party libraries require installation.

```pip install requests```

All other imports are standard Python Libraries.

As the User you will need to run the Python files in sequence:
1. zodiac_step_1
2. zodiac_step_2
   
Ensure the following documents are saved in the same folder as the Python files:
1. zodiac_csv
2. zodiac_xml

**Comments/Notes on the python code:**

<ins>_import libraries_</ins>
* `csv`: reading data from a CSV file
* `json`: data transfer on the web
* `xml.etree.ElementTree as ET`: parsing and navigating a XML file
* `sqlite3`: provide a SQL like interface to read. query and write to a SQL database
* `requests`: allows HTTP requests
  

<ins>Part 1:</ins> The user will need to run zodiac_step_1.py to start the process. In this file the following will happen:
- the url website is used to retrieve daily horoscope information, with an API key already provided.
- daily horoscope per a zodiac sign will be saved into a dictionary, based on all the listed zodiac signs.
- the retrieved daily horoscope information will be saved to a JSON file. This file will save in the same folder as your python file.

<ins>Part 2:</ins> The SQLite tables/databases will be created:
- specific database for the JSON/html data (document : all_horoscopes)
- specific database for the CSV data (document : zodiac_csv)
- specific database for the xml data (document: zodiac_xml)

<ins>Part 3:</ins> The user will need to run zodiac_step_2.py after the above has finished. In this file the following will happen:
- all three databases created will be consolidated into one database, that will be used to retrieve information.
- due to the JSON data reflecting "sign" instead of name for the Zodiac sign, the "sign AS name" is used to ensure the tables align with the Zodiac sign as their main linking point.

<ins>Part 4:</ins> The user will be prompted to input information. This will result in data output that is retrieved from the consolidated SQlite table.
- the prompts will loop until the user decides to "exit"
 
