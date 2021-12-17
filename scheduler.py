import json
import typing

import pandas

import database


class Calculate:
    def __init__(self):
        """Иницилиазтор, грузит из бд информацию о парах и отсутсвующих преподов"""
        self._db_data: pandas.DataFrame = pandas.read_sql('SELECT * FROM schedule', database.DbSchedule().connection)
        self._missed: pandas.DataFrame = pandas.read_excel('Отсутствующие.xlsx')

    def miss_teacher(self) -> pandas.DataFrame:
        """Возвращает DataFrame с расписание отсутсвующих преподователей"""
        teacher_apair: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 0]
        missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return teacher_apair.loc[teacher_apair['group_name'].isin(missed)]

    def miss_teacher_family(self) -> typing.List:
        """Возвращает фамилии преподов отсутсвующих"""
        teacher_apair: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 0]
        missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return list(teacher_apair.loc[teacher_apair['group_name'].isin(missed)]['group_name'].values)

    def get_apair_teacher(self, name: str) -> typing.Dict or None:
        """Возвращает пары препода по фамилии"""
        name = name.upper()
        df: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 0]
        result = df[df["group_name"].values == [name]]['json_data'].values
        if len(result) > 0:
            return json.loads(result[0])
        else:
            return None

    def get_apair_group(self, group_name: str) -> typing.Dict or None:
        """Возвращает пары группы по группе"""
        group_name = group_name.upper()
        df: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 1]
        result = df[df["group_name"].values == [group_name]]['json_data'].values
        if len(result) > 0:
            return json.loads(result[0])
        else:
            return None

    def replace_apair(self):
        need_replace: typing.List = []
        for teacher in self.miss_teacher_family():
            apair_teacher: typing.Dict = self.get_apair_teacher(teacher)
            for date in apair_teacher:
                for hour in apair_teacher[date]:
                    for apair in apair_teacher[date][hour]:
                        apair.update({"date": date, 'hour': hour})
                        need_replace.append(apair)
        return pandas.DataFrame(need_replace)

    def is_free(self, name, apair_day: str, apair_hour: str) -> bool:
        apair_teacher = self.get_apair_teacher(name)
        APAIR_NUMBER: typing.Dict = {
            '08:00  —  09:30': 1,
            '09:40  —  11:10': 2,
            '11:30  —  13:00': 3,
            '13:10  —  14:40': 4,
            '15:00  —  16:30': 5,
            '16:40  —  18:10': 6,
            '18:20  —  19:50': 7
        }
        if apair_teacher is not None and apair_teacher.get(apair_day) is not None and apair_teacher[apair_day].get(
                apair_hour) is not None:
            return False
        if APAIR_NUMBER.get(apair_hour) is not None:
            return True
        else:
            raise Exception('Такой пары не существует')

    def is_radius_apair(self, name, apair_day: str, apair_hour: str) -> typing.List:
        apair_teacher = self.get_apair_teacher(name)
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
        if apair_teacher is not None and apair_teacher.get(apair_day) is not None and apair_teacher[apair_day].get(
                apair_hour) is not None:
            if APAIR_HOUR[APAIR_NUMBER[apair_hour] - 1] in APAIR_HOUR:
                down_apair = self.is_free(name, apair_day, APAIR_HOUR[APAIR_NUMBER[apair_hour] - 2])
            else:
                down_apair = None
            if APAIR_HOUR[APAIR_NUMBER[apair_hour] + 1] in APAIR_HOUR:
                upper_apair = self.is_free(name, apair_day, APAIR_HOUR[APAIR_NUMBER[apair_hour]])
            else:
                upper_apair = None
            x = 1
            return [not down_apair, not upper_apair]
        else:
            return [False, False]



print(Calculate().is_radius_apair('Шашкин А.Г.', '18 декабря, суббота', '13:10  —  14:40'))
