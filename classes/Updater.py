from classes.BaseBlockchain import BaseBlockchain
from classes.BaseRepository import BaseRepository
import json


class Updater:

    def __init__(self, repository: BaseRepository, blockchain: BaseBlockchain):
        """

        :param blockchain:
        """

        self.repository = repository
        self.blockchain = blockchain
        return

    def check(self):
        if not self.repository.check():
            self.sync()

    def sync(self):
        self.repository.init()
        records = self.blockchain.get_all()['result']

        decoded_records = []

        for record in records:
            resource = self.blockchain.show_resource(record['name'])['result']
            resource_decoded = json.loads(resource['value'])
            resource_decoded['name'] = resource['name']
            decoded_records.append(resource_decoded)

        self.sync_local(decoded_records)
        return

    def sync_local(self, records):
        self.repository.eraise()

        networks = []
        types = []
        langs = []
        tags = []

        names_data = {}

        valid_records = []
        valid_records_names = []
        url_descriptions = {}

        for record in records:
            if 'url' in record and 'network' in record and 'type' in record and 'lang' in record and 'lang' in record and 'tags' in record and 'description' in record:
                valid_records_names.append(record['name'])

                if record['url'] not in url_descriptions:
                    url_descriptions[record['url']] = []

                    valid_records.append(record)

                    if networks.count(record['network']) == 0:
                        networks.append(record['network'])

                    if types.count(record['type']) == 0:
                        types.append(record['type'])

                    if langs.count(record['lang']) == 0:
                        langs.append(record['lang'])

                    record_tags = record['tags'].split(',')
                    for tag in record_tags:
                        tag = tag.strip()
                        if tags.count(tag) == 0:
                            tags.append(tag)

                    names_data[record['name']] = {
                        'network': record['network'],
                        'type': record['type'],
                        'lang': record['lang'],
                        'description': record['description'],
                        'tags': record_tags
                    }

                url_descriptions[record['url']].append(record['description'])

        for record in records:
            if record['name'] not in valid_records_names:
                if 'url' in record and 'description' in record:
                    if record['url'] in url_descriptions:
                        url_descriptions[record['url']].append(record['description'])

        self.repository.write_resources(valid_records)
        self.repository.write_networks(networks)
        self.repository.write_types(types)
        self.repository.write_langs(langs)
        self.repository.write_tags(tags)

        for name, data in names_data.items():
            resources_id = self.repository.get_resources_id_by_name(name)
            # self.repository.write_description(resources_id, data['description'])
            network_id = self.repository.get_network_id_by_name(data['network'])
            lang_id = self.repository.get_lang_id_by_name(data['lang'])
            type_id = self.repository.get_type_id_by_name(data['type'])
            self.repository.update_resources(resources_id, network_id, lang_id, type_id)
            self.repository.write_resources_tags(resources_id, names_data[name]['tags'])

        self.repository.write_descriptions(url_descriptions)
        # print(self.repository.get_resources())
        # print(self.repository.get_resources_tags())

        self.repository.commit()

        return

