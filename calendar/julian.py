jdn = 0
year = -4712
month = 1
day = 1


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


def is_leap_year(year):
    if year % 4 == 0:
        return True
    else:
        return False


def get_month_length(month, year):
    if month == 2:
        if is_leap_year(year):
            return 29
        else:
            return 28
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 31


calendar = {}
for i in range(3000000):
    calendar[jdn] = "%d. %s %d" % (day, months[month], year + 753)
    jdn += 1
    day += 1
    if day > get_month_length(month, year):
        day = 1
        month += 1
        if month > 12:
            month = 1
            year += 1