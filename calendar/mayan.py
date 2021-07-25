jdn = 584283
baktun = 0
katun = 0
year = 0
month = 0
day = 0
tzolkin_weekday = 19
tzolkin_day = 4
haab_month = 17
haab_day = 8


weekdays = [
    "Imix",
    "Ikʼ",
    "Akʼbʼal",
    "Kʼan",
    "Chikchan",
    "Kimi",
    "Manikʼ",
    "Lamat",
    "Muluk",
    "Ok",
    "Chuwen",
    "Ebʼ",
    "Bʼen",
    "Ix",
    "Men",
    "Kʼibʼ",
    "Kabʼan",
    "Etzʼnabʼ",
    "Kawak",
    "Ajaw"
]


months = [
    "Pop",
    "Woʼ",
    "Sip",
    "Sotzʼ",
    "Sek",
    "Xul",
    "Yaxkʼin",
    "Mol",
    "Chʼen",
    "Yax",
    "Sak",
    "Keh",
    "Mak",
    "Kʼankʼin",
    "Muwan",
    "Pax",
    "Kʼayab",
    "Kumkʼu",
    "Wayebʼ"
]


def get_month_length(month):
    if month == 18:
        return 5
    else:
        return 20


calendar = {}
for i in range(2880000):
    calendar[jdn] = "%d.%d.%d.%d.%d %d %s %d %s" % (
        baktun,
        katun,
        year,
        month,
        day,
        tzolkin_day,
        weekdays[tzolkin_weekday],
        haab_day,
        months[haab_month]
    )
    jdn += 1
    day += 1
    if day >= 20:
        day = 0
        month += 1
        if month >= 18:
            month = 0
            year += 1
            if year >= 20:
                year = 0
                katun += 1
                if katun >= 20:
                    katun = 0
                    baktun += 1
    tzolkin_day += 1
    if tzolkin_day > 13:
        tzolkin_day = 1
    tzolkin_weekday += 1
    if tzolkin_weekday >= 20:
        tzolkin_weekday = 0
    haab_day += 1
    if haab_day >= get_month_length(haab_month):
        haab_day = 0
        haab_month += 1
        if haab_month >= 19:
            haab_month = 0