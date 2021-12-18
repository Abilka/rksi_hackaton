import json
import typing

import pandas

import database


class Schedule:
    def __init__(self):
        """Иницилиазтор, грузит из бд информацию о парах и отсутсвующих преподов"""
        self._db_data: pandas.DataFrame = pandas.read_sql('SELECT * FROM schedule', database.DbSchedule().connection)
        self._missed: pandas.DataFrame = pandas.read_excel('Отсутствующие.xlsx')
        self._db_data_nochange = self._db_data.copy()
        self._db_data = self.convert_db_data()

    def miss_teacher(self) -> pandas.DataFrame:
        """Возвращает DataFrame с расписание отсутсвующих преподователей"""
        teacher_apair: pandas.DataFrame = self._db_data_nochange[self._db_data_nochange['is_group'] == 0]
        missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return teacher_apair.loc[teacher_apair['group_name'].isin(missed)]

    def convert_db_data(self):
        json_data: typing.List = []
        array_apair: typing.Dict = {}
        for i in self._db_data[['group_name', 'json_data']].values:
            array_apair.update({i[0]: json.loads(i[1])})

        for group in array_apair:
            for day in array_apair[group]:
                for hour in array_apair[group][day]:
                    for apair in array_apair[group][day][hour]:
                        apair.update({'group': group, 'day': day, 'hour': hour})
                        json_data.append(apair)

        return pandas.DataFrame(json_data)

    def miss_teacher_family(self) -> typing.List:
        """Возвращает фамилии преподов отсутсвующих"""
        teacher_apair: pandas.DataFrame = self._db_data_nochange[self._db_data_nochange['is_group'] == 0]
        missed: typing.List = list(map(lambda x: x.upper(), list(self._missed['ФИО'].values)))
        return list(teacher_apair.loc[teacher_apair['group_name'].isin(missed)]['group_name'].values)

    def get_apair(self, name: str) -> typing.Dict or None:
        """Возвращает пары препода по фамилии"""
        name: str = name.upper()
        result: pandas.DataFrame = self._db_data[self._db_data["group"].values == [name]]
        if len(result) > 0:
            return result
        else:
            return None

    def get_current_apair(self, name, apair_day: str, apair_hour: str):
        apair_teacher: pandas.DataFrame = self.get_apair(name)
        query: pandas.DataFrame = apair_teacher.query("day=='{}'".format(apair_day)).query(
            "hour=='{}'".format(apair_hour))
        return query

    def get_teacher_group(self, group: str) -> typing.List:
        return list(self._db_data[self._db_data['group'] == group]['teacher'].drop_duplicates().values)

    def get_subject_training(self, name: str):
        """Берет учебные предметы препода"""
        return list(self._db_data[self._db_data['teacher'] == name]['doctrine'].drop_duplicates().values)

    def set_apair(self, day: str, hour: str, family_replaced: str, family_new: str, lesson_subject: str):
        apair_teacher: pandas.DataFrame = self.get_apair(family_replaced)
        query: pandas.DataFrame = apair_teacher.query("day=='{}'".format(day)).query(
            "hour=='{}'".format(hour))
        query['doctrine'] = lesson_subject
        query['group'] = family_new
        query['weight'] = 0
        return query

    def insert_apair(self):
        ...

    def need_replace(self) -> pandas.DataFrame:
        """Возвращает dataframe пар необходимых заменить"""
        return self._db_data.loc[self._db_data['group'].isin(self.miss_teacher_family())]

    def is_free(self, name, apair_day: str, apair_hour: str) -> bool:
        """Проверка, свободна ли пара"""

        apair_teacher: pandas.DataFrame = self.get_apair(name)
        if apair_teacher is not None:
            query: pandas.DataFrame = apair_teacher.query("day=='{}'".format(apair_day)).query(
                "hour=='{}'".format(apair_hour))
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
        is_upper: bool or None = False
        is_down: bool or None = False

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
        changed: pandas.DataFrame = pandas.DataFrame()
        for row in need_replace.iterrows():
            day = row[1]['day']
            hour = row[1]['hour']
            for teacher in self.get_teacher_group(row[1]['teacher']):
                if teacher.upper() not in bad_perpods:
                    if not self.is_free(teacher, day, hour):

                        radius: typing.Dict = self.is_radius_apair(teacher, day, hour)
                        if radius['down']['status'] is True:
                            apair: pandas.DataFrame = self.set_apair(day, radius['down']['hour'], row[1]['group'],
                                                                     teacher, self.get_subject_training(teacher)[0])
                            apair['changled'] = row[1]['group']
                            apair['weight'] = 1.0
                            changed: pandas.DataFrame = changed.append(apair)
                        elif radius['upper']['status'] is True:
                            apair: pandas.DataFrame = self.set_apair(day, radius['upper']['hour'], row[1]['group'],
                                                                     teacher, self.get_subject_training(teacher)[0])
                            apair['changled'] = row[1]['group']
                            apair['weight'] = 1.0
                            changed: pandas.DataFrame = changed.append(apair)
                    else:
                        apair: pandas.DataFrame = self.set_apair(day, hour, row[1]['group'], teacher,
                                                                 self.get_subject_training(teacher)[0])
                        apair['changled'] = row[1]['group']
                        apair['weight'] = 0.5
                        changed: pandas.DataFrame = changed.append(apair)

        return pandas.DataFrame(changed.sort_values('weight',ascending=False).drop_duplicates())


x = Schedule().changed_needed()
x.to_excel('Лист замен.xlsx', 'Замены', index=False, engine='openpyxl')
