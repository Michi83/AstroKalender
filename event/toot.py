from sys import path
path.append("..")
from config import mastodon_access_token, mastodon_api_base_url
from datetime import date
from mastodon import Mastodon

mastodon = Mastodon(
    access_token=mastodon_access_token,
    api_base_url=mastodon_api_base_url
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
            mastodon.toot(message + " #Astrodon")
