class Employee:
    def __init__(self, number: int, name: str, desired_holiday: list):
        self.number = number
        self.name = name
        self.desired_holiday = desired_holiday
        self.public_holiday_cnt = 0
