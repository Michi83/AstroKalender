from sys import path
path.append("..")
from config import (access_token_key, access_token_secret, consumer_key,
                    consumer_secret)
from datetime import date
from twitter import Api


months = [
    None,
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember"
]


today = date.today()
year = today.year
month = today.month
day = today.day
filename = "img/%04d-%02d-%02d.png" % (year, month, day)
with open(filename, "rb") as file:
    message = "Der Sternenhimmel am %d. %s.\n" % (day, months[month])
    message += "(50° N, 10° O, 22 Uhr MEZ)\n"
    message += "Clear Skies!"
    api = Api(
        access_token_key=access_token_key,
        access_token_secret=access_token_secret,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret
    )
    api.PostUpdate(message, file)