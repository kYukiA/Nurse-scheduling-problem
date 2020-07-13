from evaluation import Evaluation
from employee import Employee
import calendar_check
from vcopt import vcopt
from shift_print import ShiftPrint

# 従業員情報、希望休の定義　
emp1 = Employee(1, name='employee1', desired_holiday=[6, 7, 20])
emp2 = Employee(2, name='employee2', desired_holiday=[1, 19, 25])
emp3 = Employee(3, name='employee3', desired_holiday=[12, 26, 27])
emp4 = Employee(4, name='employee4', desired_holiday=[5, 14, 28])
emp5 = Employee(5, name='employee5', desired_holiday=[3, 22, 23])
employees = [emp1, emp2, emp3, emp4, emp5]


# 評価関数
def eval_shift(individual):
    s = Evaluation(all_shifts=individual,
                   calendar_check=calendar_check.CalendarCheck(2020, 6),
                   employees=employees,
                   number_of_people=len(employees),
                   holiday_max=9,
                   continuous_work=4)
    return s.shift_evaluation()


def main():
    # カレンダ情報
    calendar = calendar_check.CalendarCheck(2020, 6)
    # 要素のフォーマットを定義
    para_range = [[0, 1] for _ in range(calendar.check_number_of_day()*len(employees))]

    # GAで最適化
    para, score = vcopt().dcGA(para_range,         # パラメータ範囲
                               eval_shift,         # 評価関数
                               0)                  # 目標値

    # 結果の表示
    print(para)
    print(score)
    return para, score


if __name__ == "__main__":
    expected, _ = main()

    shift_print = ShiftPrint(employees, expected)
    print(shift_print)

