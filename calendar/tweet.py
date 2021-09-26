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
todays_date = "%d. %s %d" % (day, months[month], year)
with open("calendar_data.txt", "r") as file:
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
api = Api(
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret
)
message = "Guten Morgen.🌞\n\n"
message += "%s (greg.)\n" % gregorian_date
message += "%s (jul./a.u.c.)\n" % julian_date
message += "%s (jüd.)\n" % hebrew_date
message += "%s (isl.)¹\n" % islamic_date
message += "%s (frz.)²\n" % french_date
message += "%s (Maya)³" % mayan_date
result = api.PostUpdate(message)
id = result.id
message = "¹Microsofts kuwaitischer Algorithmus, "
message += "kann vom astronomisch bestimmten Datum abweichen.\n"
message += "²Romme-Schaltregel\n"
message += "³GMT-Korrelation"
api.PostUpdate(message, in_reply_to_status_id=id)