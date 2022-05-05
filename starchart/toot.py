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


today = date.today()
year = today.year
month = today.month
day = today.day
filename = "img/%04d-%02d-%02d.png" % (year, month, day)
message = "Der Sternenhimmel am %d. %s.\n" % (day, months[month])
message += "(50° N, 10° O, 22 Uhr MEZ)\n"
message += "Clear Skies! #Astrodon"
mastodon = Mastodon(
    access_token=mastodon_access_token,
    api_base_url=mastodon_api_base_url
)
media_id = mastodon.media_post(filename).id
mastodon.status_post(message, media_ids=[media_id])
