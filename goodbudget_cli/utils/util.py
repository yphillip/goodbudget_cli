import datetime


def format_date(input_date: str) -> str:
    """Goodbudget's input date must be formatted as mm/dd/yyyy"""

    if input_date.lower() == "today":
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")
    elif input_date.lower() == "yesterday":
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        formatted_date = datetime.date.strftime(yesterday, "%m/%d/%Y")
    else:
        assert input_date.count("/") == 2, "Format must be mm/dd/yyyy!"
        month, day, year = input_date.split("/")

        assert len(month) in [1, 2]
        if len(month) == 1:
            month = "0" + month
        assert len(day) in [1, 2]
        if len(day) == 1:
            day = "0" + day
        assert len(year) in [2, 4]
        if len(year) == 4:
            assert year.startswith("20")  # assuming it's 20XX
        if len(year) == 2:
            year = "20" + year

        formatted_date = "/".join([month, day, year])

    return formatted_date
