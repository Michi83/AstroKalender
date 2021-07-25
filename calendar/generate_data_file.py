from gregorian import calendar as gregorian_calendar
from julian import calendar as julian_calendar
from hebrew import calendar as hebrew_calendar
from islamic import calendar as islamic_calendar
from french import calendar as french_calendar
from mayan import calendar as mayan_calendar


with open("calendar_data.txt", "w") as file:
    for jdn in range(2451545, 2488070):
        file.write("%s,%s,%s,%s,%s,%s,%s\n" % (
            jdn,
            gregorian_calendar[jdn],
            julian_calendar[jdn],
            hebrew_calendar[jdn],
            islamic_calendar[jdn],
            french_calendar[jdn],
            mayan_calendar[jdn]
        ))