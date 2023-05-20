##############################################
#   Formatting datetime and getting needed   #
#            datetime information            #
##############################################

from datetime import datetime


class DateTime:
    @classmethod
    def get_date_today(cls) -> str:
        date = datetime.now()
        return date.strftime(r"%Y/%m/%d")

    @classmethod
    def get_time_now(cls) -> str:
        time = datetime.now()
        return time.strftime(r"%I:%M %p")

    @classmethod
    def get_datetime_now(cls) -> str:
        dt = datetime.now()
        return dt.strftime(r"%Y/%m/%d %H:%M")

    @classmethod
    def change_format(cls, dt: str) -> str:
        dl = datetime.strptime(dt, r"%Y/%B/%d %H:%M")
        return dl.strftime(r"%Y/%m/%d %H:%M")

    @classmethod
    def get_date_from_fulldate(cls, fulldate: str) -> str:
        fulldate = datetime.strptime(fulldate, r"%Y/%m/%d %H:%M")
        return fulldate.strftime(r"%Y/%m/%d")

    @classmethod
    def get_time_from_fulldate(cls, fulldate: str) -> str:
        fulldate = datetime.strptime(fulldate, r"%Y/%m/%d %H:%M")
        return fulldate.strftime(r"%H:%M")
