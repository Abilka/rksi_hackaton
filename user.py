import hashlib

import requests

import setting


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.host = "http://{0}:{1}".format(setting.SERVER_IP, setting.SERVER_PORT)
        self.auth = self.is_login

    @property
    def is_login(self):
        if requests.get('{0}/login'.format(self.host),
                        params={'login': self.login, 'password': self.coding_password(self.password)}).json()[
            'result'] is True:
            return True
        return False

    @property
    def role(self):
        if requests.get('{0}/login'.format(self.host),
                        params={'login': self.login, 'password': self.coding_password(self.password)}).json()[
            'result'] is True:
            return True
        return False

    def set_password(self, new_password: str) -> None:
        if self.auth is True:
            requests.get('{0}/new_password'.format(self.host),
                         params={'login': self.login, 'password': self.coding_password(new_password)}).json()

    @staticmethod
    def coding_password(password: str) -> str:
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    @staticmethod
    def get_user() -> dict:
        return requests.get('http://{0}:{1}/get_user'.format(setting.SERVER_IP, setting.SERVER_PORT)).json()

    @staticmethod
    def new_user(login: str, password: str, role: str) -> dict:
        return requests.get('http://{0}:{1}/new_user'.format(setting.SERVER_IP, setting.SERVER_PORT),
                            params={'login': login, "password": User.coding_password(password), 'role': role}).json()
