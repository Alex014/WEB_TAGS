from classes.BaseRepository import BaseRepository


class Searcher:

    def __init__(self, repository: BaseRepository):
        self.repository = repository
        return

    def get_networks(self):
        # .....
        return

    def get_langs(self, network_id):
        # .....
        return

    def get_types(self, network_id, lang_id):
        # .....
        return

    def get_tags(self, network_id, lang_id, type_id):
        # .....
        return

    def get_resources(self, network_id=0, lang_id=0, type_id=0, tags_id_list=()):
        # .....
        return

    def get_resource(self, resource_id):
        # .....
        return