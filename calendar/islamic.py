jdn = 1948439
year = 1
month = 1
day = 1


months = [
    None,
    "Muharram",
    "Safar",
    "Rabīʿ al-awwal",
    "Rabīʿ ath-thānī",
    "Dschumādā l-ūlā",
    "Dschumādā th-thāniya",
    "Radschab",
    "Schaʿbān",
    "Ramadan",
    "Schawwāl",
    "Dhū l-Qaʿda",
    "Dhū l-Hiddscha"
]


def is_leap_year(year):
    if year % 30 in {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}:
        return True
    else:
        return False


def get_month_length(month, year):
    if month in {1, 3, 5, 7, 9, 11}:
        return 30
    elif month in {2, 4, 6, 8, 10}:
        return 29
    elif month == 12:
        if is_leap_year(year):
            return 30
        else:
            return 29


calendar = {}
for i in range(1000000):
    calendar[jdn] = "%d. %s %d" % (day, months[month], year)
    jdn += 1
    day += 1
    if day > get_month_length(month, year):
        day = 1
        month += 1
        if month > 12:
            month = 1
            year += 1