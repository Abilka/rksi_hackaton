import json
import typing

import pandas

import database


class Schedule:
    def __init__(self):
        """Иницилиазтор, грузит из бд информацию о парах и отсутсвующих преподов"""
        self._db_data: pandas.DataFrame = pandas.read_sql('SELECT * FROM schedule', database.DbSchedule().connection)
        self._missed: pandas.DataFrame = pandas.read_excel('Отсутствующие.xlsx')
        self._db_data = self.convert_db_data()

    def miss_teacher(self) -> pandas.DataFrame:
        """Возвращает DataFrame с расписание отсутсвующих преподователей"""
        teacher_apair: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 0]
        missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return teacher_apair.loc[teacher_apair['group_name'].isin(missed)]

    def convert_db_data(self):
        json_data: typing.List = []

        array_apair = []
        for i in self._db_data['json_data']:
            array_apair.append(json.loads(i))

        for data in array_apair:
            for day in data:
                for hour in data[day]:
                    for apair in data[day][hour]:
                        apair.update({'day': day, 'hour': hour})
                        json_data.append(apair)

        return pandas.DataFrame(json_data)

    def miss_teacher_family(self) -> typing.List:
        """Возвращает фамилии преподов отсутсвующих"""
        teacher_apair: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 0]
        missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return list(teacher_apair.loc[teacher_apair['group_name'].isin(missed)]['group_name'].values)

    def get_apair(self, name: str) -> typing.Dict or None:
        """Возвращает пары препода по фамилии"""
        name: str = name.title()
        result = self._db_data[self._db_data["teacher"].values == [name]]
        if len(result) > 0:
            return result
        else:
            return None

    def need_replace(self) -> pandas.DataFrame:
        """Возвращает dataframe пар необходимых заменить"""
        need_replace: typing.List = []
        for teacher in self.miss_teacher_family():
            apair_teacher: typing.Dict = self.get_apair(teacher)
            for date in apair_teacher:
                for hour in apair_teacher[date]:
                    for apair in apair_teacher[date][hour]:
                        apair.update({"date": date, 'hour': hour})
                        need_replace.append(apair)
        return pandas.DataFrame(need_replace)

    def is_free(self, name, apair_day: str, apair_hour: str) -> bool:
        """Проверка, свободна ли пара"""

        apair_teacher: pandas.DataFrame = self.get_apair(name)
        query = apair_teacher.query("day=='{}'".format(apair_day)).query("hour=='{}'".format(apair_hour))
        if len(list(query.values)) > 0:
            return False
        return True

    def is_radius_apair(self, name, apair_day: str, apair_hour: str) -> typing.Dict:
        """Выясняет, свободны ли пары в радиусе (выше/ниже) одной пары от отправленной
        :param name: ФИО препода
        :param apair_day: день пары
        :param apair_hour: часы пары
        """
        APAIR_HOUR: typing.List = [
            '08:00  —  09:30',
            '09:40  —  11:10',
            '11:30  —  13:00',
            '13:10  —  14:40',
            '15:00  —  16:30',
            '16:40  —  18:10',
            '18:20  —  19:50'
        ]
        APAIR_NUMBER: typing.Dict = {
            '08:00  —  09:30': 1,
            '09:40  —  11:10': 2,
            '11:30  —  13:00': 3,
            '13:10  —  14:40': 4,
            '15:00  —  16:30': 5,
            '16:40  —  18:10': 6,
            '18:20  —  19:50': 7
        }
        is_upper, is_down = False, False

        if APAIR_NUMBER[apair_hour] + 1 > 7:
            is_upper = None
        if APAIR_NUMBER[apair_hour] - 1 < 1:
            is_down = None
        down_hour = APAIR_HOUR[APAIR_NUMBER[apair_hour] - 2]
        upper_hour = APAIR_HOUR[APAIR_NUMBER[apair_hour] - 1]
        if self.is_free(name, apair_day, down_hour) is True and is_down is not None:
            is_down = True
        if self.is_free(name, apair_day, upper_hour) is True and is_upper is not None:
            is_upper = True

        return {'down': {"status": is_down, 'hour': down_hour}, 'upper': {"status": is_upper, 'hour': upper_hour}}

    def changed_needed(self) -> pandas.DataFrame:

        bad_perpods = self.miss_teacher_family()
        need_replace = self.need_replace()
        for i in self.need_replace()['teacher'].drop_duplicates():
            group_apair = self.get_apair_group(i[1])
            for day in group_apair:
                for hour in group_apair[day]:
                    for apair in group_apair[day][hour]:
                        print(apair)


print(Schedule().is_radius_apair('Шашкин А.Г.', '18 декабря, суббота', '18:20  —  19:50'))
