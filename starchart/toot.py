from sys import path
path.append("..")
from config import mastodon_access_token, mastodon_api_base_url
from datetime import date
from mastodon import Mastodon


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


def get_alt_text(date_string):
    with open("alttexts.txt", "r") as file:
        for line in file:
            if line[:10] == date_string:
                return line[11:].strip()
    return ""


today = date.today()
year = today.year
month = today.month
day = today.day
date_string = "%04d-%02d-%02d" % (year, month, day)
filename = "img/%s.png" % date_string
alt_text = get_alt_text(date_string)
message = "Der Sternenhimmel am %d. %s %d.\n" % (day, months[month], year)
message += "(50° N, 10° O, 22 Uhr MEZ)\n"
message += "#ClearSkies! #Astronomie #Astrodon"
mastodon = Mastodon(
    access_token=mastodon_access_token,
    api_base_url=mastodon_api_base_url
)
media_id = mastodon.media_post(filename, description=alt_text).id
mastodon.status_post(message, media_ids=[media_id])
