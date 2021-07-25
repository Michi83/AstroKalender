jdn = 2375840
year = 1
month = 1
day = 1


months = [
    None,
    "Vendémiaire",
    "Brumaire",
    "Frimaire",
    "Nivôse",
    "Pluviôse",
    "Ventôse",
    "Germinal",
    "Floréal",
    "Prairial",
    "Messidor",
    "Thermidor",
    "Fructidor",
    "Sansculottides"
]


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                if year % 4000 == 0:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return True
    else:
        return False


def get_month_length(month, year):
    if month == 13:
        if is_leap_year(year):
            return 6
        else:
            return 5
    else:
        return 30


calendar = {}
for i in range(1460969):
    calendar[jdn] = "%d. %s %d" % (day, months[month], year)
    jdn += 1
    day += 1
    if day > get_month_length(month, year):
        day = 1
        month += 1
        if month > 13:
            month = 1
            year += 1