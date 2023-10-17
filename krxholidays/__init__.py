from datetime import datetime, timedelta
from krxholidays.data import holidays

weeknames = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

def is_holiday_str(date_str: str, pattern: str = "%Y-%m-%d") -> bool:
    """
    주어진 날짜가 공휴일인지 확인합니다.
    """
    date = datetime.strptime(date_str, pattern)
    return is_holiday(date)


def is_holiday(date: datetime) -> bool:
    """
    주어진 날짜가 공휴일인지 확인합니다.
    """
    return get_day_info(date)["is_holiday"]

def add_business_days(date: datetime, days: int) -> datetime:
    not_holiday_count = 1
    compare_date = date

    while not_holiday_count <= days:
        compare_date = compare_date + timedelta(days=1)

        if not is_holiday(compare_date):
            not_holiday_count += 1
    return compare_date

def get_day_info(date: datetime) -> dict:
    """
    주어진 날짜가 공휴일인지 확인합니다.
    """

    matched_list = list(filter(lambda x: x["date"] == date.strftime("%Y-%m-%d"), holidays))
    if len(matched_list) > 0:
        return matched_list[0]

    weekday = date.weekday()
    weekname = weeknames[weekday]

    if weekday == 5 or weekday == 6:
        return {"date": date.strftime("%Y-%m-%d"), "week_name": weekname, "desc": "주말", "is_holiday": True}

    return {"date": date.strftime("%Y-%m-%d"), "week_name": weekname, "desc": "평일", "is_holiday": False}