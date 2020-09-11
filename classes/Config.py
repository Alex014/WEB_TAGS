import os
import json


class Config:

    config = {}
    filename = os.path.dirname(__file__)+os.path.sep+os.path.pardir+os.path.sep+'config.json'

    @staticmethod
    def get_config():
        if len(Config.config) == 0:
            if os.path.exists(Config.filename):
                f = os.open(Config.filename, os.O_RDONLY)
                dt = os.read(f, os.path.getsize(Config.filename))
                Config.config = json.loads(dt)
                os.close(f)
            else:
                Config.config = {
                    'host': 'localhost',
                    'port': 8332,
                    'user': 'user',
                    'password': 'user'
                }
            return Config.config
        else:
            return Config.config

    @staticmethod
    def save_config(config):
        if not os.path.exists(Config.filename):
            os.mknod(Config.filename)

        file = open(Config.filename, 'w')
        data = json.dumps(config)
        file.write(data)
        file.close()

        Config.config = config

