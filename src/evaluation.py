"""
１ヶ月のシフトを決めるにあたっての条件
~前提条件~
・従業員は4人
・従業員は休み希望を数日提出した後シフトを決める

~シフト制約~
出勤者数は2,3人
従業員内で土日祝日と重なる休み日数を揃えたい
従業員内で連休の回数を揃えたい
4人中2人のうち一方は出社しなければならない
"""
import numpy as np
import calendar_check as calendar

# それぞれの評価項目のWEIGHT
DESIRED_HOLIDAY_WEIGHT = 5
NUMBER_OF_HOLIDAYS_WEIGHT = 1
CONTINUOUS_WORK_WEIGHT = 1
PUBLIC_HOLIDAY_WEIGHT = 1
CONSECUTIVE_HOLIDAYS_WEIGHT = 1
TEAM_SHIFT_WEIGHT = 1


class Evaluation:
    def __init__(self,
                 all_shifts: list,
                 calendar_check: calendar,
                 employees: list,
                 number_of_people: int,
                 holiday_max: int,
                 continuous_work: int):

        self.all_shifts = all_shifts
        self.number_of_people = number_of_people
        self.month_days = calendar_check.check_number_of_day()
        self.employees = employees
        self.penalty_list = []
        self.slice_shift = self._slice()
        self.calendar_check = calendar_check
        self.holiday_max = holiday_max
        self.continuous_work = continuous_work

    def shift_evaluation(self):
        self.penalty_list = [self._check_desired_holiday(),
                             self._check_number_of_holidays(),
                             self._check_continuous_work(),
                             self._check_public_holiday(),
                             self._check_consecutive_holidays(),
                             self._check_team_shift(),
                             ]

        penalty = sum(self.penalty_list)
        return penalty

    def print_penalty(self) -> None:
        """
        penaltyの詳細を確認できます。
        """
        self.shift_evaluation()
        print('希望休/休日数/連勤数/土日祝/連休数/チーム制約')
        print(self.penalty_list)
        return

    def _slice(self):
        """
        要素数（従業員数*１ヶ月の日数）のデータを社員ごとのシフトに分解
        __init__で一度実行され、結果をクラス変数slice_shiftに格納
        """
        sliced = []
        start = 0
        days = self.month_days
        for num in range(self.number_of_people):
            sliced.append(self.all_shifts[start:start + days])
            start = start + days
        return tuple(sliced)

    def _check_continuous_work(self) -> int:
        """
        従業員の連続勤務日数を確認します
        :return:全従業員の基準日から超過した連続勤務日数の合計
        """
        penalty = 0
        for individual_shift in self.slice_shift:
            max_cnt = 0
            cnt = 0
            for day in individual_shift:
                # 一人づつ連続勤務数を計算する
                if day == 1:
                    cnt += 1
                else:
                    cnt = 0

                if max_cnt < cnt:
                    max_cnt = cnt

            # 指定された連続勤務数から超過した日数分をpenaltyに加算する
            if max_cnt > self.continuous_work:
                penalty = penalty + max_cnt - self.continuous_work

        return penalty * CONTINUOUS_WORK_WEIGHT

    def _check_desired_holiday(self) -> int:
        """
        従業員の休み希望日が勤務日となっていないかの確認をします
        :return:シフトが希望通りでない日数に重さを積算した合計
        """
        penalty = 0
        for number, individual_shift in enumerate(self.slice_shift):
            employee = self.employees[number]
            for status in employee.desired_holiday:
                if not individual_shift[status-1] == 0:
                    penalty += 1
        return penalty * DESIRED_HOLIDAY_WEIGHT

    def _check_number_of_holidays(self) -> int:
        """
        １ヶ月の休日数が指定通りか確認します。
        :return:指定した休日数との従業員ごとの差分の合計
        """
        penalty = 0
        for individual_shift in self.slice_shift:
            holiday_cnt = np.count_nonzero(individual_shift == 0)
            penalty += abs(holiday_cnt - self.holiday_max)
        return penalty * NUMBER_OF_HOLIDAYS_WEIGHT

    def _check_team_shift(self) -> int:
        """
        １日の出勤者数の制約の確認をします
        :return: ex) １日の出勤者数が3~4人以外の場合は差分をpenaltyとしてreturn
        """
        penalty = 0
        for day_index in range(self.month_days):
            employee_day_list = []
            for shift in self.slice_shift:
                employee_day_list.append(shift[day_index])
            employee_cnt = sum(employee_day_list)
            if not (employee_cnt == 4 or employee_cnt == 3):
                penalty += 1
            if (employee_day_list[0] + employee_day_list[1]) == 0:
                penalty += 1

        return penalty * TEAM_SHIFT_WEIGHT

    def _check_public_holiday(self) -> float:
        """
        暦の土日祝日と休みが重なる日数が従業員内で均等かの確認をします
        :return:暦の土日祝日と休みが重なる日数の従業員内平均との差分合計
        """
        penalty = 0
        cnt_list = []
        for number, individual_shift in enumerate(self.slice_shift):
            public_holiday_cnt = 0
            for day, status in enumerate(individual_shift):
                if status == 0:
                    if self.calendar_check.check_calendar_holiday(day + 1):
                        public_holiday_cnt += 1
            self.employees[number].public_holiday_cnt = public_holiday_cnt
            cnt_list.append(public_holiday_cnt)

        avg = sum(cnt_list) / len(cnt_list)
        for employee in self.employees:
            penalty += abs(employee.public_holiday_cnt - avg)
        return penalty * PUBLIC_HOLIDAY_WEIGHT

    def _check_consecutive_holidays(self) -> float:
        """
        連休の回数が従業員内で均等かを確認します
        :return:全従業員の連休回数を平均し、差分をpenaltyとしてreturn
        """
        penalty = 0
        cnt_list = []
        for individual_shift in self.slice_shift:
            cnt = 0
            consecutive_holidays_cnt = 0
            for day in individual_shift:
                if day == 0:
                    cnt += 1
                else:
                    if cnt >= 2:
                        consecutive_holidays_cnt += 1
                    cnt = 0
            cnt_list.append(consecutive_holidays_cnt)
        avg = sum(cnt_list) / len(cnt_list)
        for number, employee in enumerate(self.employees):
            penalty = penalty + abs(cnt_list[number] - avg)
        return penalty * CONSECUTIVE_HOLIDAYS_WEIGHT
