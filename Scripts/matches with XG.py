from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

url = 'https://fbref.com/en/matches/{}'

csv_file = '..\\Data\\game_data.csv'

df = pd.read_csv(csv_file)

# get all dates

# Get the unique values in a specific column
unique_dates = df['Date'].unique()

column_names = ['date', 'home', 'home_xg', 'home_score', 'away', 'away_xg', 'away_score']

df_matches = pd.DataFrame(columns=column_names)

# loop through dates
for matchday in unique_dates:
    sleep(20)
    # get the response for that day from SkyNews
    url_date = format(datetime.strptime(matchday, "%d/%m/%Y"), "%Y-%m-%d")

    url_with_date = url.format(url_date)

    response = requests.get(url_with_date)

    if response.status_code == 200:
        content = response.text

        # Get the value from a specific column
        soup = BeautifulSoup(content, 'html.parser')

        sections = soup.find_all(class_="table_wrapper")

        for section in sections:
            title = section.find(class_="section_anchor").text.replace('"', '').replace("'","").replace(">",'')
            if title in ['Championship', 'Premier League']:
                table_section = section.find(class_="stats_table")
                table = table_section.find('tbody')
                rows = table.find_all('tr')
                for row in rows:
                    match ={}
                    columns = row.find_all('td')
                    match = {
                        'date': matchday,
                        'home': columns[2].text,
                        'home_xg': columns[3].text,
                        'home_score': columns[4].text.split("–")[0],
                        'away': columns[6].text,
                        'away_xg': columns[5].text,
                        'away_score': columns[4].text.split("–")[1]
                    }
                    df_matches = df_matches.append(match, ignore_index=True)


    else:
        print("Error:", response.status_code)

df_matches.to_csv('matches_with_xg.csv')






