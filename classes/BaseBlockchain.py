import abc


class BaseBlockchain:

    @abc.abstractmethod
    def get_info(self):
        pass

    @abc.abstractmethod
    def check(self):
        pass

    @abc.abstractmethod
    def post_resource(self, data, days):
        pass

    @abc.abstractmethod
    def edit_resource(self, name, data, days):
        pass

    @abc.abstractmethod
    def delete_resource(self, name):
        pass

    @abc.abstractmethod
    def get_my(self):
        pass

    @abc.abstractmethod
    def get_all(self):
        pass
