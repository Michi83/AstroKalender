from sys import path
path.append("..")
from config import mastodon_access_token, mastodon_api_base_url
from datetime import date, datetime, timedelta
from math import asin, atan2, cos, radians as rad, sin, tan, tau
from pytz import timezone, utc
from mastodon import Mastodon

# Horizons settings:
# Time Specification: Start=2000-01-01 UT , Stop=2099-12-31, Step=1 (days)
# Apparent RA & DEC
# Local apparent sidereal time
# calendar and Julian Day Number

# Symbols:
# jdn = Julian day number
# alpha = right ascension
# delta = declination
# theta = local sidereal time
# A = azimuth
# a = altitude


data = None


class Datum:
    def __init__(self, date, jdn, alpha, delta, theta):
        self.date = date
        self.jdn = jdn
        self.alpha = alpha
        self.delta = delta
        self.theta = theta


def load_data(filename):
    global data
    data = []
    with open(filename, "r") as file:
        for line in file:
            if line == "$$SOE\n":
                break
        for line in file:
            if line == "$$EOE\n":
                break
            date = line[1:12]
            jdn = float(line[19:36])
            alpha = rad(float(line[41:50]))
            delta = rad(float(line[51:60]))
            theta = rad(15 * float(line[62:75]))
            datum = Datum(date, jdn, alpha, delta, theta)
            data.append(datum)


def interpolate(x, x1, x2, y1, y2):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


def right_ascension_declination_sidereal_time(jdn):
    x = jdn
    for i in range(len(data)):
        if data[i].jdn < x and data[i + 1].jdn >= x:
            x1 = data[i].jdn
            x2 = data[i + 1].jdn
            y1 = data[i].alpha
            y2 = data[i + 1].alpha
            if y2 < y1:
                y2 += tau
            alpha = interpolate(x, x1, x2, y1, y2)
            y1 = data[i].delta
            y2 = data[i + 1].delta
            delta = interpolate(x, x1, x2, y1, y2)
            y1 = data[i].theta
            y2 = data[i + 1].theta
            if y2 < y1:
                y2 += tau
            y2 += tau
            theta = interpolate(x, x1, x2, y1, y2)
            return alpha, delta, theta


def azimuth_altitude(jdn, phi):
    alpha, delta, theta = right_ascension_declination_sidereal_time(jdn)
    h = theta - alpha
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
    for datum in data:
        if datum.date == date_en:
            jdn = datum.jdn
            break
    message = "#GutenMorgen.🌞\n\n"
    message += "Der Sonnenlauf am %s in %s:\n" % (date_de, city)
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
    message += "\n"
    message += "#Astronomie #Astrokalender #Astrodon"
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