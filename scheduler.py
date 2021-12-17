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
        missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return teacher_apair.loc[teacher_apair['group_name'].isin(missed)]

    def get_apair_teacher(self, name: str) -> typing.Dict:
        """Возвращает пары препода по фамилии"""
        df: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 0]
        return json.loads(df[df["group_name"].values == [name]]['json_data'].values[0])

    def get_apair_group(self, group_name: str) -> typing.Dict:
        df: pandas.DataFrame = self._db_data[self._db_data['is_group'] == 1]
        return json.loads(df[df["group_name"].values == [group_name]]['json_data'].values[0])

