from classes.BaseBlockchain import BaseBlockchain
import requests
import json
import time


class BlockchainEmercoin(BaseBlockchain):

    def __init__(self, url: str, port: int, login: str, password: str):
        """

        :param url:
        :param port:
        :param login:
        :param password:
        """
        self.url = url
        self.port = port
        self.login = login
        self.password = password
        return

    def get_info(self):
        return self.__method("getinfo", [])

    def check(self):
        try:
            self.get_info()
        except Exception:
            return False

        return True

    def post_resource(self, data, days):
        name = 'webtags:'+str(time.time())
        value = self.__pack_record(data)
        return self.__method("name_new", [name, value, days, '', ''])

    def show_resource(self, name):

        return self.__method("name_show", [name, '', 'base64'])

    def edit_resource(self, name, data, days):
        value = self.__pack_record(data)

        return self.__method("name_update", [name, value, days, '', ''])

    def delete_resource(self, name):
        return self.__method("name_delete", [name])

    def __method(self, method, params):
        url = self.__get_url()

        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "1.0",
            "id": 0,
        }

        response = requests.post(url, json=payload).json()
        return response

    def __parse_record(self, data_json_str):
        return json.loads(data_json_str)

    def __pack_record(self, data):
        return json.dumps(data)

    def __get_url(self):
        return "http://{}:{}@{}:{}/".format(self.login, self.password, self.url, self.port)

    def get_my(self):
        all_names = self.__method("name_list", ['', ''])['result']

        results = []

        for record in all_names:
            if record['name'].find('webtags:') == 0:
                results.append(record)

        return results

    def get_all(self):
        return self.__method("name_filter", ['^webtags:.+', 0, 0, 0, '', ''])
