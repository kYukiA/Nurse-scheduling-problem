class ShiftPrint:

    def __init__(self, employees, shifts):
        self.employees = employees
        self.shift_all_list = shifts

    def __str__(self):
        result = f"\n"
        number_of_days = int(len(self.shift_all_list) / len(self.employees))
        list_ = list(range(1, number_of_days+1))
        list_ = list(map(self.space_format, list_))
        result += "day\t\t\t:{}\n".format(list_)

        for key, employee in enumerate(self.employees):
            result += f"{employee.name}\t:{list(map(self.space_format, self.split_list(number_of_days)[key]))}\n"

        return result

    def split_list(self, n: int) -> list:
        """
        引数で指定した数字でself.shift_all_listを分割します。
        :param n: 分割数を指定します
        :return: 分割後のlist ex)[[1, 2],[3, 4]]
        """
        result = [self.shift_all_list[idx:idx + n] for idx in range(0, len(self.shift_all_list), n)]
        return result

    @staticmethod
    def space_format(s: str) -> str:
        """
        日付を表示した時に縦が揃うように、2文字分のスペースを確保し、右詰めに調整します
        :param s: "2", "20"
        :return: " 2", "20"
        """
        return "{:>2}".format(s)
