from sys import path
path.append("..")
from config import (access_token_key, access_token_secret, consumer_key,
                    consumer_secret)
from datetime import date
from twitter import Api

api = Api(
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret
)

today = date.today()
today_year = today.year
today_month = today.month
today_day = today.day
with open("events.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line == "" or line[0] == "#":
            continue
        year = int(line[0:4])
        month = int(line[5:7])
        day = int(line[8:10])
        if year == today_year and month == today_month and day == today_day:
            message = line[11:]
            api.PostUpdate(message)
