import abc


class BaseRepository:

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def check(self):
        pass

    @abc.abstractmethod
    def eraise(self):
        pass

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def write_tags(self, tags: list):
        pass

    @abc.abstractmethod
    def write_types(self, types: list):
        pass

    @abc.abstractmethod
    def write_langs(self, langs: list):
        pass

    @abc.abstractmethod
    def write_networks(self, networks: list):
        pass

    @abc.abstractmethod
    def write_resources(self, resources: list):
        pass

    @abc.abstractmethod
    def write_descriptions(self, resources_id: int, descriptions: list):
        pass

    @abc.abstractmethod
    def write_description(self, resources_id: int, description: str):
        pass

    @abc.abstractmethod
    def write_resources_tags(self, resources_id: int, tags: list):
        pass

    @abc.abstractmethod
    def read_networks(self):
        pass

    @abc.abstractmethod
    def read_langs(self, network_id: int):
        pass

    @abc.abstractmethod
    def read_types(self, network_id: int, lang_id: int):
        pass

    @abc.abstractmethod
    def read_tags(self, network_id: int, lang_id: int, type_id: int):
        pass

    @abc.abstractmethod
    def read_resources(self, network_id=0, lang_id=0, type_id=0, tags_id=0):
        pass

    @abc.abstractmethod
    def read_resource(self, resource_id: int):
        pass

    @abc.abstractmethod
    def get_resources_id_by_name(self, name: str):
        pass

    @abc.abstractmethod
    def read_descriptions(self, resources_id: int):
        pass

    @abc.abstractmethod
    def get_network_id_by_name(self, name: str):
        pass

    @abc.abstractmethod
    def get_lang_id_by_name(self, name: str):
        pass

    @abc.abstractmethod
    def get_type_id_by_name(self, name: str):
        pass

    @abc.abstractmethod
    def get_resources(self):
        pass

    @abc.abstractmethod
    def get_resources_tags(self):
        pass

    @abc.abstractmethod
    def get_network_name_by_id(self, network_id: int):
        pass

    @abc.abstractmethod
    def get_lang_name_by_id(self, lang_id: int):
        pass

    @abc.abstractmethod
    def get_type_name_by_id(self, type_id: int):
        pass

    @abc.abstractmethod
    def get_tag_name_by_id(self, tags_id: int):
        pass

    @abc.abstractmethod
    def update_resources(self, resources_id: int, network_id: int, lang_id: int, type_id: int):
        pass

    @abc.abstractmethod
    def search_resources_by_url(self, url: str):
        pass

    @abc.abstractmethod
    def search_resources_by_description(self, description: str):
        pass
