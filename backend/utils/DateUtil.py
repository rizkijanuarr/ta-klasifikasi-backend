class DateUtil:

    DATE_PATTERN_1 = "dd-MM-yyyy"; # 05-09-2024
    DATE_PATTERN_2 = "yyyy-MM-dd"; # 2024-09-05
    DATE_PATTERN_3 = "yyyy-MM"; # 2024-09
    DATE_PATTERN_4 = "dd MMMM"; # 05 September
    DATE_PATTERN_5 = "dd MMM yyyy"; # 05 Sep 2024
    DATE_PATTERN_6 = "EEEE, dd MMMM yyyy"; # Kamis, 05 September 2024
    DATE_PATTERN_7 = "EEE, dd MMM yyyy"; # Kam, 05 Sep 2024
    DATE_PATTERN_8 = "dd/MM/yyyy"; # 05/09/2024
    DATE_PATTERN_9 = "MMMM yyyy"; # September 2024
    DATE_PATTERN_10 = "yyyy"; # 2024

    TIME_PATTERN_1 = "HH:mm"; # 14:30
    TIME_PATTERN_2 = "HH:mm:ss"; # 14:30:45
    TIME_PATTERN_3 = "hh:mm a"; # 02:30 PM
    TIME_PATTERN_4 = "HH:mm:ss z"; # 14:30:45 WIB
    TIME_PATTERN_5 = "HH:mm:ss Z"; # 14:30:45 +0700
    TIME_PATTERN_6 = "HH:mm:ss.SSS"; # 14:30:45.123

    UTC_IDN = "+7"; # (WIB)
    UTC = "UTC"; # (Waktu Universal)

    # main!
    def convertDateToString(date, pattern):
        if date is None:
            return None
        SimpleDateFormat p = SimpleDateFormat(pattern, Locale("id", "ID"))
        return p.format(date)

    # "05-09-2024"
    def formatShortDate(date):
        return convertDateToString(date, DATE_PATTERN_1)

    # "Kamis, 05 September 2024"
    def formatLongDateTime(date):
        return convertDateToString(date, DATE_PATTERN_6)

    # "2024-09-05 14:30"
    def formatWithTime(date):
        return convertDateToString(date, DATE_PATTERN_2 + " " + TIME_PATTERN_1)

    def convertStringToDate(dateString, pattern):
        SimpleDateFormat p = SimpleDateFormat(pattern, Locale("id", "ID"))
        return p.parse(dateString)

    def convertStringToDateTime(dateString, pattern):
        SimpleDateFormat p = SimpleDateFormat(pattern, Locale("id", "ID"))
        return p.parse(dateString)

