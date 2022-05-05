from sys import path
path.append("..")
from config import mastodon_access_token, mastodon_api_base_url
from datetime import date
from mastodon import Mastodon

# Ephemerides generated with NASA's HORIZONS web interface.
# Settings:
# Ephemeris Type [change] :     OBSERVER
# Observer Location [change] :   Geocentric [500]
# Time Span [change] :      Start=2000-01-01, Stop=2099-12-31, Step=1 d
# Table Settings [change] :     defaults
# Display/Output [change] :     download/save (plain text file)

SUN = 0
MOON = 1
MERCURY = 2
VENUS = 3
MARS = 4
JUPITER = 5
SATURN = 6
URANUS = 7
NEPTUNE = 8

filenames = (
    "sun.txt",
    "moon.txt",
    "mercury.txt",
    "venus.txt",
    "mars.txt",
    "jupiter.txt",
    "saturn.txt",
    "uranus.txt",
    "neptune.txt"
)

names = (
    "Sonne🌞",
    "Mond",
    "Merkur",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn🪐",
    "Uranus",
    "Neptun"
)

months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

months_german = (None, "Januar", "Februar", "März", "April", "Mai", "Juni",
                 "Juli", "August", "September", "Oktober", "November",
                 "Dezember")

mastodon = Mastodon(
    access_token=mastodon_access_token,
    api_base_url=mastodon_api_base_url
)

today = date.today()
today_year = today.year
today_month = today.month
today_day = today.day
message = "Ephemeriden für den %d. %s %d, 00:00 UT. #Astrodon" % (
    today_day,
    months_german[today_month],
    today_year
)
result = mastodon.status_post(message)
last_id = result.id
for i in range(9):
    filename = filenames[i]
    name = names[i]
    with open(filename, "r") as file:
        start_of_ephemeris_found = False
        for line in file:
            if line.startswith("$$SOE"):
                start_of_ephemeris_found = True
            elif start_of_ephemeris_found:
                year = int(line[1:5])
                month = months[line[6:9]]
                day = int(line[10:12])
                if (year == today_year and month == today_month
                        and day == today_day):
                    ra_hours = int(line[23:25])
                    ra_minutes = int(line[26:28])
                    ra_seconds = float(line[29:34])
                    dec_degrees = int(line[35:38])
                    dec_minutes = int(line[39:41])
                    dec_seconds = float(line[42:46])
                    magnitude = float(line[47:54])
                    distance = float(line[63:79])
                    elongation = float(line[92:100])
                    elongation_type = line[101:103]
                    phase_angle = float(line[104:112])
                    
                    # indicate the moon's phase with emojis
                    if i == MOON:
                        if elongation < 22.5:
                            name += "🌑"
                        elif elongation < 67.5 and elongation_type == "/T":
                            name += "🌒"
                        elif elongation < 112.5 and elongation_type == "/T":
                            name += "🌓"
                        elif elongation < 157.5 and elongation_type == "/T":
                            name += "🌔"
                        elif elongation >= 157.5:
                            name += "🌕"
                        elif elongation >= 112.5:
                            name += "🌖"
                        elif elongation >= 67.5:
                            name += "🌗"
                        else:
                            name += "🌘"
                    
                    # construct and tweet message
                    message = "%s\n" % name
                    message += "Rektaszension: %dʰ %dᵐ %.2fˢ\n" % (
                        ra_hours,
                        ra_minutes,
                        ra_seconds
                    )
                    message += "Deklination: %+d° %d′ %.1f″\n" % (
                        dec_degrees,
                        dec_minutes,
                        dec_seconds
                    )
                    message += "Helligkeit: %.3f mag\n" % magnitude
                    if i == MOON:
                        # km for the moon, au for everything else
                        distance = round(149597870.7 * distance)
                        message += "Entfernung: %d km" % distance
                    else:
                        message += "Entfernung: %f AU" % distance
                    if i != SUN:
                        message += "\n"
                        message += "Elongation: %.4f°" % elongation
                        if elongation_type == "/L":
                            message += " (führend)"
                        elif elongation_type == "/T":
                            message += " (folgend)"
                        message += "\n"
                        message += "Phasenwinkel: %.4f°" % phase_angle
                    result = mastodon.status_post(
                        message,
                        in_reply_to_id=last_id
                    )
                    last_id = result.id
                    break