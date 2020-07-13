import pytest
from calendar_check import CalendarCheck


@pytest.fixture()
def calendar_init():
    return CalendarCheck(2020, 7)


@pytest.mark.parametrize("day, expected", [
    (10, False),
    (24, True),
    (25, True)
])
@pytest.mark.usefixtures("calendar_init")
def test_check_calendar_holiday(calendar_init, day, expected):
    assert calendar_init.check_calendar_holiday(day) == expected


@pytest.mark.parametrize("day, expected", [
    (10, False),
    (24, False),
    (25, True)
])
@pytest.mark.usefixtures("calendar_init")
def test_check_saturday(calendar_init, day, expected):
    assert calendar_init.check_saturday(day) == expected


@pytest.mark.parametrize("year, month, expected", [
    (2020, 2, 29),
    (2020, 4, 30),
    (2020, 6, 30)
])
def test_check_number_of_day(year, month, expected):
    calendar_check = CalendarCheck(year, month)
    assert calendar_check.check_number_of_day() == expected

