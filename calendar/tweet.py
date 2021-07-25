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
todays_date = "%d. %s %d" % (day, months[month], year)
with open("/home/astrokalender/goodmorning/calendar_data.txt", "r") as file:
    for line in file:
        fields = line.strip().split(",")
        jdn = fields[0]
        gregorian_date = fields[1]
        julian_date = fields[2]
        hebrew_date = fields[3]
        islamic_date = fields[4]
        french_date = fields[5]
        mayan_date = fields[6]
        if gregorian_date == todays_date:
            break
tweet = "Guten Morgen.🌞\n\n"
tweet += "%s (greg.)\n" % gregorian_date
tweet += "%s (jul.)\n" % julian_date
tweet += "%s (jüd.)\n" % hebrew_date
tweet += "%s (isl.)\n" % islamic_date
tweet += "%s (frz.)\n" % french_date
tweet += "%s (maya.)" % mayan_date
api = Api(
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret
)
api.PostUpdate(tweet)
