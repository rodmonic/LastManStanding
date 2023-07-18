import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.skysports.com/football/fixtures-results/{}'

csv_file = 'data.csv'

df = pd.read_csv(csv_file)

# get all dates

# Get the unique values in a specific column
unique_dates = df['Date'].unique()

column_names = ['date', 'team_1', 'team_2', 'score_1', 'score_2']

df_matches = pd.DataFrame(columns=column_names)

# loop through dates
for matchday in unique_dates:
    # get the response for that day from SkyNews
    url_date = format(datetime.strptime(matchday, "%d/%m/%Y"), "%d-%B-%Y")

    url_with_date = url.format(url_date)

    response = requests.get(url_with_date)

    if response.status_code == 200:
        content = response.text

        # Get the value from a specific column
        soup = BeautifulSoup(content, 'html.parser')

        matches = soup.find_all(class_="matches__item matches__link")
        matches_dict = []
        for match in matches:
            match_dict ={}
            team_1 = match.find(class_="matches__item-col matches__participant matches__participant--side1").text.strip(' \n\t')
            team_2 = match.find(class_="matches__item-col matches__participant matches__participant--side2").text.strip(' \n\t')
            score_1 = match.find_all(class_="matches__teamscores-side")[0].text.strip(' \n\t')
            score_2 = match.find_all(class_="matches__teamscores-side")[1].text.strip(' \n\t')

            df_matches = df_matches.append({
                "date": matchday,
                "team_1": team_1,
                "team_2": team_2,
                "score_1": score_1,
                "score_2": score_2
            },
                ignore_index=True
            )

    else:
        print("Error:", response.status_code)

df_matches.to_csv('matches.csv')






