import datetime
import jpholiday
import calendar


class CalendarCheck:

    # 対象の年月を初期設定します
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month

    # 引数の日付が土日祝日かを確認します
    def check_calendar_holiday(self, day: int) -> bool:
        target_date = datetime.date(self.year, self.month, day)
        if target_date.weekday() >= 5 or jpholiday.is_holiday(target_date):
            return True
        else:
            return False

    # 引数の日付が土曜日か確認します
    def check_saturday(self, day: int) -> bool:
        target_date = datetime.date(self.year, self.month, day)
        if target_date.weekday() == 5:
            return True
        else:
            return False

    # 月の日数を確認します
    def check_number_of_day(self) -> int:
        return calendar.monthrange(self.year, self.month)[1]
