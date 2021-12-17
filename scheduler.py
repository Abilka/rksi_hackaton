import json
import typing

import pandas

import database


class Calculate:
    def __init__(self):
        self._db_data: pandas.DataFrame = pandas.read_sql('SELECT * FROM schedule', database.DbSchedule().connection)
        self._missed: pandas.DataFrame = pandas.read_excel('Отсутствующие.xlsx')

    def miss_teacher(self) -> pandas.DataFrame:
        """Возвращает DataFrame с расписание отсутсвующих преподователей"""
        teacher_apair: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 0]
        self._missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return teacher_apair.loc[teacher_apair['group_name'].isin(self._missed)]

    def need_change(self):
        """Возвращает пары которые надо заменить"""
        json_data = self.miss_teacher()

        json.loads(json_data.iloc[0]['json_data'])
        print(json_data)

Calculate().need_change()