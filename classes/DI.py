import os
from classes.BlockchainEmercoin import BlockchainEmercoin
from classes.RepositorySQLITE import RepositorySQLITE
from classes.Config import Config


class DI:

    @staticmethod
    def get_blockchain():
        conf = Config.get_config()
        return BlockchainEmercoin(
            conf['host'],
            conf['port'],
            conf['user'],
            conf['password']
        )

    @staticmethod
    def get_repository():
        filename = os.path.dirname(__file__) + \
                   os.path.sep + \
                   os.path.pardir + \
                   os.path.sep + \
                   'database.db'
        return RepositorySQLITE(db=filename)
