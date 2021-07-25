jdn = 347998
year = 1
hours = 5
parts = 204


months = [
    None,
    "Nisan",
    "Ijjar",
    "Siwan",
    "Tammus",
    "Aw",
    "Elul",
    "Tischri",
    "Cheschwan",
    "Kislew",
    "Tevet",
    "Schevat",
    "Adar",
    "We-Adar"
]


def is_leap_year(year):
    if year % 19 in {0, 3, 6, 8, 11, 14, 17}:
        return True
    else:
        return False


def get_month_length(month, year):
    year_length = new_years[year + 1] - new_years[year]
    if month in {1, 3, 5, 7, 11}:
        return 30
    elif month in {2, 4, 6, 10, 13}:
        return 29
    elif month == 8:
        if year_length in {355, 385}:
            return 30
        else:
            return 29
    elif month == 9:
        if year_length in {353, 383}:
            return 29
        else:
            return 30
    elif month == 12:
        if year_length in {383, 384, 385}:
            return 30
        else:
            return 29


new_years = [None]
for i in range(7001):
    postponement = 0
    if hours >= 18:
        postponement = 1
    elif (jdn % 7 == 1 and 10000 * hours + parts >= 90204
            and not is_leap_year(year)):
        postponement = 1
    elif (jdn % 7 == 0 and 10000 * hours + parts >= 150589
            and is_leap_year(year - 1)):
        postponement = 1
    if (jdn + postponement) % 7 in {2, 4, 6}:
        postponement += 1
    new_years.append(jdn + postponement)
    if is_leap_year(year):
        parts += 589
        hours += 21
        jdn += 383
    else:
        parts += 876
        hours += 8
        jdn += 354
    if parts >= 1080:
        parts -= 1080
        hours += 1
    if hours >= 24:
        hours -= 24
        jdn += 1
    year += 1


jdn = 347998
year = 1
month = 7
day = 1
calendar = {}
for i in range(2556729):
    calendar[jdn] = "%d. %s %d" % (day, months[month], year)
    jdn += 1
    day += 1
    if day > get_month_length(month, year):
        day = 1
        month += 1
        if month == 7:
            year += 1
        elif not is_leap_year(year) and month > 12 or month > 13:
            month = 1