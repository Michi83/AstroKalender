from sys import path
path.append("..")
from config import mastodon_access_token, mastodon_api_base_url
from datetime import date, datetime, timedelta
from math import asin, atan2, cos, floor, pi, radians as rad, sin, tan
from pytz import timezone, utc
from mastodon import Mastodon

# Horizons settings:
# Time Specification: Start=2000-01-01 UT , Stop=2099-12-31, Step=1 (days)
# Apparent RA & DEC
# Local apparent hour angle
# calendar and Julian Day Number

# Symbols:
# jdn = Julian day number
# h = hour angle
# delta = declination
# A = azimuth
# a = altitude


data = None


class Datum:
    def __init__(self, date, jdn, h, delta):
        self.date = date
        self.jdn = jdn
        self.h = h
        self.delta = delta


def load_data(filename):
    global data
    data = {}
    with open(filename, "r") as file:
        for line in file:
            if line == "$$SOE\n":
                break
        for line in file:
            if line == "$$EOE\n":
                break
            date = line[1:12]
            jdn = float(line[19:36])
            delta = rad(float(line[51:60]))
            h = rad(15 * float(line[62:75]))
            datum = Datum(date, jdn, h, delta)
            data[date] = datum
            data[jdn] = datum


def interpolate(x, x1, x2, y1, y2):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


def hour_angle_declination(jdn):
    x = jdn
    datum1 = data[floor(jdn - 0.5) + 0.5]
    datum2 = data[floor(jdn - 0.5) + 1.5]
    x1 = datum1.jdn
    x2 = datum2.jdn
    y1 = datum1.h
    y2 = datum2.h + 2 * pi  # accounts for earth's rotation
    h = interpolate(x, x1, x2, y1, y2)
    y1 = datum1.delta
    y2 = datum2.delta
    delta = interpolate(x, x1, x2, y1, y2)
    return h, delta


def azimuth_altitude(jdn, phi):
    h, delta = hour_angle_declination(jdn)
    A = atan2(sin(h), cos(h) * sin(phi) - tan(delta) * cos(phi))
    a = asin(sin(phi) * sin(delta) + cos(phi) * cos(delta) * cos(h))
    return A, a


def toot(city, phi, tz, filename):
    load_data(filename)
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    months_en = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"]
    months_de = [None, "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"]
    if city == "Wien":
        months_de[1] = "Jänner"
    date_en = "%4i-%s-%02i" % (year, months_en[month], day)
    date_de = "%i. %s %i" % (day, months_de[month], year)
    jdn = data[date_en].jdn
    message = "#GutenMorgen.🌞\n\n"
    message += "Der Sonnenlauf am %s in #%s:\n" % (date_de, city)
    for h in range(-2, 23):
        for m in range(60):
            if h < 0:
                dt_utc = datetime(year, month, day, h + 24, m, tzinfo=utc)
                dt_utc -= timedelta(days=1)
            else:
                dt_utc = datetime(year, month, day, h, m, tzinfo=utc)
            dt_local = dt_utc.astimezone(tz)
            if dt_local.day != day:
                continue
            A1, a1 = azimuth_altitude(jdn + h / 24 + (m - 0.5) / 1440, phi)
            A2, a2 = azimuth_altitude(jdn + h / 24 + (m + 0.5) / 1440, phi)
            if a1 < rad(-18) and a2 >= rad(-18):
                message += ("%02i:%02i Beginn der astronomischen Dämmerung\n" %
                    (dt_local.hour, dt_local.minute))
            if a1 < rad(-12) and a2 >= rad(-12):
                message += ("%02i:%02i Beginn der nautischen Dämmerung\n" %
                    (dt_local.hour, dt_local.minute))
            if a1 < rad(-6) and a2 >= rad(-6):
                message += ("%02i:%02i Beginn der bürgerlichen Dämmerung\n" %
                    (dt_local.hour, dt_local.minute))
            if a1 < rad(-50 / 60) and a2 >= rad(-50 / 60):
                message += ("%02i:%02i Sonnenaufgang\n" %
                    (dt_local.hour, dt_local.minute))
            if A1 < 0 and A2 >= 0:
                message += ("%02i:%02i Wahrer Mittag\n" %
                    (dt_local.hour, dt_local.minute))
            if a1 >= rad(-50 / 60) and a2 < rad(-50 / 60):
                message += ("%02i:%02i Sonnenuntergang\n" %
                    (dt_local.hour, dt_local.minute))
            if a1 >= rad(-6) and a2 < rad(-6):
                message += ("%02i:%02i Ende der bürgerlichen Dämmerung\n" %
                    (dt_local.hour, dt_local.minute))
            if a1 >= rad(-12) and a2 < rad(-12):
                message += ("%02i:%02i Ende der nautischen Dämmerung\n" %
                    (dt_local.hour, dt_local.minute))
            if a1 >= rad(-18) and a2 < rad(-18):
                message += ("%02i:%02i Ende der astronomischen Dämmerung\n" %
                    (dt_local.hour, dt_local.minute))
    message += "\n#Astronomie #AstroKalender #Astrodon"
    mastodon = Mastodon(
        access_token=mastodon_access_token,
        api_base_url=mastodon_api_base_url
    )
    mastodon.toot(message)


toot(
    "Berlin",
    rad(52 + 31 / 60),
    timezone("Europe/Berlin"),
    "berlin.txt"
)
toot(
    "Hamburg",
    rad(53 + 34 / 60),
    timezone("Europe/Berlin"),
    "hamburg.txt"
)
toot(
    "München",
    rad(48 + 8 / 60),
    timezone("Europe/Berlin"),
    "muenchen.txt"
)
toot(
    "Köln",
    rad(50 + 56 / 60),
    timezone("Europe/Berlin"),
    "koeln.txt"
)
toot(
    "Frankfurt",
    rad(50 + 2 / 60),
    timezone("Europe/Berlin"),
    "frankfurt.txt"
)
toot(
    "Stuttgart",
    rad(48 + 48 / 60),
    timezone("Europe/Berlin"),
    "stuttgart.txt"
)
toot(
    "Wien",
    rad(48 + 13 / 60),
    timezone("Europe/Vienna"),
    "wien.txt"
)
toot(
    "Zürich",
    rad(47 + 22 / 60),
    timezone("Europe/Zurich"),
    "zuerich.txt"
)