import json
import sqlite3
from typing import List


class DbSchedule:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('schedule.db')
        self.cursor = self.connection.cursor()

    """with as"""

    def __enter__(self):
        self.connection = sqlite3.connect('schedule.db')
        self.cursor = self.connection.cursor()
        return self

    def cleare_base(self):
        self.cursor.execute('DELETE FROM schedule')

    def append_json_data(self, group: str, json_data: str, is_group: bool) -> None:
        self.cursor.execute('INSERT INTO schedule (group_name, json_data, is_group) VALUES (?, ?, ?)',
                            (group, json_data, is_group))

    def select_shcedule(self, command: str) -> dict:
        """Отправка расписания
        :param need_day: количество дней в расписание для возврата
        :param command: группа или препод по которому надо расписание
        :rtype: json с группами
        """
        result = self.cursor.execute('SELECT * FROM schedule WHERE group_name LIKE ?',
                                     ("{}%".format(command),)).fetchone()

        if result and len(result) > 0 and result[1] != 'null':
            json_string_with_base = dict(json.loads(result[1]))
            return {'name': result[0].upper(), 'schedule': json_string_with_base}
        else:
            return {'name': None, 'schedule': None}

    def take_group(self) -> List[str]:
        resutl = self.cursor.execute('SELECT group_name FROM schedule WHERE is_group=1').fetchall()
        return list(map(lambda x: x[0], resutl))

    def take_prepods(self) -> List[str]:
        resutl = self.cursor.execute('SELECT group_name FROM schedule WHERE is_group=1').fetchall()
        return list(map(lambda x: x[0], resutl))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
