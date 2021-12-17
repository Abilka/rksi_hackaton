from typing import Union

import requests
from bs4 import BeautifulSoup

APAIR_NUMBER = {
    '08:00  —  09:30': 1,
    '09:40  —  11:10': 2,
    '11:30  —  13:00': 3,
    '13:10  —  14:40': 4,
    '15:00  —  16:30': 5,
    '16:40  —  18:10': 6,
    '18:20  —  19:50': 7
}


class Take:
    def __init__(self, domain='su') -> None:
        self.domain = domain
        self.prepodi_list = []
        self.group_list = []

    def take_group_list(self) -> list:
        """Лист групп с выпадающего списка на сайте, если уже есть возвращает его который в памяти обьекта
        :rtype: list групп
        """

        if len(self.group_list) == 0:
            reas = requests.post('https://www.rksi.su/')
            soup = BeautifulSoup(reas.content, "html.parser")
            prepodi_select = soup.findAll(['select'])[1]
            group_select = soup.findAll(['select'])[0]
            for i in group_select.findAll(['option']):
                self.group_list.append(i.text.upper())
            for i in prepodi_select.findAll(['option']):
                i = i.text
                # if '  ' in i:
                #     i = i.replace('  ', ' ')
                self.prepodi_list.append(i.upper())

        return self.group_list

    def take_perpod_list(self) -> list:
        """Лист прпеподов с выподающего списка, если уже есть возвращает его который в памяти обьекта
        :rtype: list преподов
        """

        if len(self.prepodi_list) == 0:
            reas = requests.post('https://www.rksi.su/')
            soup = BeautifulSoup(reas.content, "html.parser")
            prepodi_select = soup.findAll(['select'])[1]
            group_select = soup.findAll(['select'])[0]
            for i in group_select.findAll(['option']):
                self.group_list.append(i.text.upper())
            for i in prepodi_select.findAll(['option']):
                i = i.text
                # if '  ' in i:
                #     i = i.replace('  ', ' ')
                self.prepodi_list.append(i.upper())
        return self.prepodi_list

    def schedule(self, cmd: str) -> Union[list, None]:
        """
        Запрос расписания с сайта
        :param cmd: группа/препод
        :return: лист пар, если пар нет или не существует группы - None
        """

        if len(self.group_list) == 0:
            self.take_group_list()
        if cmd in self.group_list:
            is_group = True
        else:
            cmd = cmd.title()
            is_group = False

        if self.domain == 'ru':
            cmd = cmd.encode('cp1251')
            cmd = str(cmd).replace('\\x', '%')
            cmd = str(cmd).replace('\'', '')
            cmd = str(cmd).replace(' ', '+')

            self.cmd = str(cmd).replace('b', '', 1)

            self.headers = {"Host": "www.rksi.ru",
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip,deflate",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Content-Length": "47",
                            "Origin": "http://www.rksi.ru",
                            "Connection": "keep-alive",
                            "Referer": "http://www.rksi.ru/schedule",
                            "Upgrade-Insecure-Requests": "1",
                            "Pragma": "no-cache",
                            "Cache-Control": "no-cache"}
            if is_group:
                self.reas = requests.post('https://www.rksi.ru/schedule/',
                                          data=f'group={self.cmd}&stt=%CF%EE%EA%E0%E7%E0%F2%FC%21',
                                          headers=self.headers)
            else:
                self.reas = requests.post('https://www.rksi.ru/schedule/',
                                          data=f'teacher={self.cmd}&stp=%CF%EE%EA%E0%E7%E0%F2%FC%21',
                                          headers=self.headers)
        else:
            if is_group:
                self.headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                                "Accept-Encoding": "gzip, deflate",
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Content-Length": "77",
                                "Connection": "keep-alive"}
                data = {
                    "group": cmd,
                    'stt': "Показать!"
                }
            else:
                self.headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                                "Accept-Encoding": "gzip, deflate",
                                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                                "Content-Length": "140",
                                "Connection": "keep-alive"}
                data = {
                    "teacher": cmd,
                    'stp': "Показать!"
                }

            self.reas = requests.post('http://rksi.su',
                                      data=data,
                                      headers=self.headers)

        soup = BeautifulSoup(self.reas.content, "html.parser")
        soup = soup.findAll(['p', 'b', 'hr'])

        if len(soup) == 0:
            return None
        schedule = [[]]
        acum = 0

        if self.domain == 'ru':
            soup.pop(0)
        else:
            pass

        for i in soup:

            if i.contents:
                schedule[acum].append(i)
            else:
                acum += 1
                schedule.append([])

        for i in range(len(schedule)):
            for j in range(len(schedule[i])):
                if '<br/><b>' not in str(schedule[i][j]) and j != 0:
                    schedule[i][j] = None
        dictonary = {}

        for days in schedule:
            main_day = days[0].text
            dictonary[main_day] = {}
            for pari in days:
                if pari:
                    if '<br/>' in str(pari):
                        pari = str(pari).split('<br/>')
                    if len(pari) > 2:
                        pari[0] = pari[0].replace('<p>', '')
                        pari[1] = pari[1].replace('</b>', '').replace('<b>', '')
                        pari[2] = pari[2].replace('</p>', '').split(', ауд. ')
                        audit_info = pari[2][1].split('-')
                        apair_time = pari[0].split('  —  ')
                        if len(audit_info) < 2:
                            while len(audit_info) != 2:
                                audit_info.append('')
                        data_apait = {'doctrine': pari[1], 'teacher': pari[2][0],
                                      'auditoria': audit_info[0], 'corpus': audit_info[1],
                                      'number': APAIR_NUMBER[pari[0]], 'start': apair_time[0],
                                      'end': apair_time[1], 'warn': None
                                      }
                        if dictonary[main_day].get(pari[0]):
                            dictonary[main_day][pari[0]].append(data_apait)
                        else:
                            dictonary[main_day][pari[0]] = [data_apait]

        if dictonary.get('Многоканальный телефон: +7 (863) 206-88-88') == {}:
            return None
        else:
            return dictonary
