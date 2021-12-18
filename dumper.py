import datetime
import json
import logging

import time

import requests

import database
import takeschedule

DEBUG = False

logging.basicConfig(format='%(asctime)s (%(levelname)s) -  %(message)s', level=logging.INFO, filename='dump.log',
                    filemode='a')


def wait_until_day(need_day: int, today: datetime.datetime = datetime.datetime.now(), hour: int = 23,
                   minute: int = 0) -> float:
    end_of_day_datetime = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
    wait_time = (end_of_day_datetime.timestamp() - datetime.datetime.now().timestamp()) + (3600 * 24 * need_day)
    return wait_time+1

def start():
    try:
        requests.get('https://rksi.ru/schedule')
    except:
        logging.info('Ошибка запроса на сайт')
        time.sleep(600 * 3)
        start()
        pass
    else:
        logging.info('Запускаю дамп расписания с сайта')
        with database.DbSchedule() as db:
            db.cleare_base()
            x = takeschedule.Take()
            for group in x.take_group_list():
                sch = x.schedule(group)
                db.append_json_data(group, json.dumps(sch), True)
            logging.info('Закончил дамп групп')
            for group in x.take_perpod_list():
                sch = x.schedule(group)
                db.append_json_data(group.replace('  ', ' '), json.dumps(sch), False)
        logging.info('Дамп закончен')


if __name__ == '__main__':
    while True:
        day_number = datetime.datetime.today().weekday()
        day_activate = [0, 2, 4, 6]
        if day_number in day_activate or DEBUG:
            logging.info("Сегодня день дампа")
            start()
            now_datetime = datetime.datetime.now()
            wait_time = wait_until_day(2, now_datetime, 3)
            logging.info("Жду {}".format(wait_time))
            time.sleep(wait_time)
        else:
            logging.info("Сегодня не день дампа")
            now_datetime = datetime.datetime.now()
            wait_time = wait_until_day(2, now_datetime, 3)
            logging.info("Жду {}".format(wait_time))
            time.sleep(wait_time)


