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


def is_valentines_day(month, day):
    return month == 2 and day == 14


def is_easter(year, month, day):
    # see Astronomical Algorithms by Jean Meeus
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    n = (h + l - 7 * m + 114) // 31
    p = (h + l - 7 * m + 114) % 31
    return month == n and day == p + 1


def is_halloween(month, day):
    return month == 10 and day == 31


def is_christmas(month, day):
    return month == 12 and day == 25


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
message = "Guten Morgen."
if is_valentines_day(month, day):
    message += "💞"
elif is_easter(year, month, day):
    message += "🐰"
elif is_halloween(month, day):
    message += "🎃"
elif is_christmas(month, day):
    message += "🎅"
else:
    message += "🌞"
message += "\n\n"
message += "%s (greg.)\n" % gregorian_date
message += "%s (jul./a.u.c.)\n" % julian_date
message += "%s (jüd.)\n" % hebrew_date
message += "%s (isl.)¹\n" % islamic_date
message += "%s (frz.)²\n" % french_date
message += "%s (Maya)³" % mayan_date
result = api.PostUpdate(message)
id = result.id
message = "¹Kuwaitischer Algorithmus\n"
message += "²Romme-Schaltregel\n"
message += "³GMT-Korrelation"
api.PostUpdate(message, in_reply_to_status_id=id)