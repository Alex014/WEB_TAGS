from classes.BaseRepository import BaseRepository
import sqlite3

class RepositorySQLITE(BaseRepository):

    def __init__(self, db: str):
        self.connection = sqlite3.connect(db)
        self.connection.row_factory = sqlite3.Row

    def init(self):
        # self.connection.execute('CREATE DATABASE IF NOT EXISTS web_tags DEFAULT CHARACTER SET utf8')
        # self.connection.execute('USE web_tags"')

        self.connection.execute('CREATE TABLE IF NOT EXISTS descriptions ('
                                'id INTEGER NOT NULL NOT NULL PRIMARY KEY AUTOINCREMENT,'
                                'resources_id INTEGER KEY,'
                                'description text NOT NULL'
                                ');')

        self.connection.execute('CREATE TABLE IF NOT EXISTS langs ('
                                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                                'name TEXT KEY'
                                ');')

        self.connection.execute('CREATE TABLE IF NOT EXISTS networks ('
                                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                                'name TEXT KEY'
                                ');')

        self.connection.execute('CREATE TABLE IF NOT EXISTS types ('
                                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                                'name TEXT KEY'
                                ');')

        self.connection.execute('CREATE TABLE IF NOT EXISTS resources ('
                                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                                'network_id INTEGER KEY,'
                                'lang_id INTEGER KEY,'
                                'type_id INTEGER KEY,'
                                'url TEXT UNIQUE,'
                                'name TEXT KEY,'
                                'FOREIGN KEY  (lang_id) REFERENCES langs  (id),'
                                'FOREIGN KEY  (network_id) REFERENCES networks  (id),'
                                'FOREIGN KEY  (type_id) REFERENCES types  (id),'
                                'FOREIGN KEY  (id) REFERENCES resources_tags  (resources_id) ON DELETE CASCADE,'
                                'FOREIGN KEY  (id) REFERENCES resources_types  (resources_id) ON DELETE CASCADE'
                                ');')

        self.connection.execute('CREATE TABLE IF NOT EXISTS resources_tags ('
                                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                                'resources_id INTEGER KEY,'
                                'tags_id INTEGER KEY'
                                ');')

        self.connection.execute('CREATE TABLE IF NOT EXISTS tags ('
                                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                                'name TEXT KEY,'
                                'FOREIGN KEY  (id) REFERENCES resources_tags  (tags_id) ON DELETE CASCADE'
                                ');')
        return

    def eraise(self):
        self.connection.execute('DELETE FROM resources_tags')
        self.connection.execute('DELETE FROM tags')
        self.connection.execute('DELETE FROM types')
        self.connection.execute('DELETE FROM descriptions')
        self.connection.execute('DELETE FROM langs')
        self.connection.execute('DELETE FROM networks')
        self.connection.execute('DELETE FROM resources')
        return

    def commit(self):
        return self.connection.commit()

    def write_tags(self, tags: list):
        tags_brackets = []
        values = []
        for tag in tags:
            tags_brackets.append('(?)')
            values.append(tag)

        sql = ', '.join(tags_brackets)
        res = self.connection.execute('INSERT INTO tags (name) VALUES ' + sql, values)
        # print(res.rowcount)
        return

    def write_types(self, types: list):
        types_brackets = []
        values = []
        for type in types:
            types_brackets.append('(?)')
            values.append(type)

        sql = ', '.join(types_brackets)
        res = self.connection.execute('INSERT INTO types (name) VALUES ' + sql, values)
        # print(res.rowcount)
        return

    def write_langs(self, langs: list):
        langs_brackets = []
        values = []
        for lang in langs:
            langs_brackets.append('(?)')
            values.append(lang)

        sql = ', '.join(langs_brackets)
        res = self.connection.execute('INSERT INTO langs (name) VALUES ' + sql, values)
        # print(res.rowcount)
        return

    def write_networks(self, networks: list):
        networks_brackets = []
        values = []
        for network in networks:
            networks_brackets.append('(?)')
            values.append(network)

        sql = ', '.join(networks_brackets)
        res = self.connection.execute('INSERT INTO networks (name) VALUES ' + sql, values)
        # print(res.rowcount)
        return

    def write_resources(self, resources: list):
        networks_brackets = []
        values = []
        for resource in resources:
            networks_brackets.append('(?, ?)')
            values.append(resource['name'])
            values.append(resource['url'])

        sql = ', '.join(networks_brackets)
        res = self.connection.execute('INSERT INTO resources (name, url) VALUES ' + sql, values)
        # print(res.rowcount)
        return

    def write_descriptions(self, descriptions: dict):
        descriptions_brackets = []
        values = []
        for url in descriptions:
            for description in descriptions[url]:
                descriptions_brackets.append('( (SELECT id FROM resources WHERE url = ?) , ?)')
                values.append(url)
                values.append(description)

        sql = ', '.join(descriptions_brackets)
        self.connection.execute('INSERT INTO descriptions (resources_id, description) VALUES ' + sql, values)
        return

    def write_description(self, resources_id: int, description: str):
        self.connection.execute('INSERT INTO descriptions (resources_id, description) VALUES(?, ?)',
                                [resources_id, description])
        return

    def write_resources_tags(self, resources_id: int, tags: list):
        params = []
        for i in range(len(tags)):
            params.append('?')

        self.connection.execute('INSERT INTO resources_tags SELECT NULL, ' + str(
            resources_id) + ' , id FROM tags WHERE name in (' + ', '.join(params) + ')', tags)
        return

    def read_networks(self):
        cur = self.connection.cursor()
        res = cur.execute('SELECT N.*, '
                          '(SELECT COUNT(R.id)  FROM resources R WHERE R.network_id = N.id) AS cnt '
                          'FROM networks N')
        return res.fetchall()

    def read_langs(self, network_id: int):
        cur = self.connection.cursor()
        res = cur.execute('SELECT L.*,'
                          ' (SELECT COUNT(R.id)  FROM resources R WHERE R.lang_id = L.id AND R.network_id = ?) AS cnt '
                          'FROM langs L '
                          'WHERE id IN (SELECT lang_id FROM resources WHERE network_id = ?)',
                          [network_id, network_id])
        return res.fetchall()

    def read_types(self, network_id: int, lang_id: int):
        cur = self.connection.cursor()
        res = cur.execute('SELECT T.*,'
                          ' (SELECT COUNT(DISTINCT R.id)  FROM resources R WHERE R.type_id = T.id AND R.network_id = ? AND R.lang_id = ?) AS cnt '
                          'FROM types T '
                          'WHERE '
                          ' id IN (SELECT type_id FROM resources WHERE network_id = ? AND lang_id = ?)',
                          [network_id, lang_id, network_id, lang_id])
        return res.fetchall()

    def read_tags(self, network_id: int, lang_id: int, type_id: int):
        cur = self.connection.cursor()
        res = cur.execute('SELECT T.*, '
                          ' (SELECT COUNT(DISTINCT R.id)  '
                          '  FROM resources R '
                          '  INNER JOIN resources_tags RT ON (RT.resources_id = R.id) '
                          '  WHERE RT.tags_id = T.id AND R.network_id = ? AND R.lang_id = ? AND R.type_id = ?'
                          ' ) AS cnt '
                          'FROM tags T '
                          'INNER JOIN resources_tags RT ON (RT.tags_id = T.id) '
                          'INNER JOIN resources R ON (RT.resources_id = R.id) '
                          'WHERE '
                          ' R.network_id = ? AND R.lang_id = ? AND R.type_id = ?'
                          ' ORDER BY T.name ',
                          [network_id, lang_id, type_id, network_id, lang_id, type_id])
        return res.fetchall()

    def read_resources(self, network_id=0, lang_id=0, type_id=0, tags_id=0):
        cur = self.connection.cursor()
        res = cur.execute('SELECT R.*,'
                          ' (SELECT COUNT(DRC.id)  FROM descriptions DRC WHERE DRC.resources_id = R.id) AS cnt, '
                          ' (SELECT D.description FROM descriptions D WHERE D.resources_id = R.id ORDER BY D.id LIMIT 1 ) AS description '
                          'FROM resources R '
                          'INNER JOIN resources_tags RT ON (RT.resources_id = R.id) '
                          'WHERE '
                          ' R.network_id = ? AND R.lang_id = ? AND R.type_id = ? '
                          ' AND RT.tags_id = ? '
                          'ORDER BY cnt DESC',
                          [network_id, lang_id, type_id, tags_id])
        return res.fetchall()

    def read_resource(self, resources_id: int):
        cur = self.connection.cursor()
        res = cur.execute('SELECT * FROM resources WHERE id = ?', [resources_id])
        return res.fetchone()

    def read_descriptions(self, resources_id: int):
        cur = self.connection.cursor()
        res = cur.execute('SELECT * FROM descriptions WHERE resources_id = ?', [resources_id])
        return res.fetchall()

    def get_resources_id_by_name(self, name: str):
        res = self.connection.execute('SELECT * FROM resources WHERE name = ?', [name])
        resource = res.fetchone()
        return resource[0]

    def get_network_id_by_name(self, name: str):
        res = self.connection.execute('SELECT * FROM networks WHERE name = ?', [name])
        return res.fetchone()[0]

    def get_network_name_by_id(self, network_id: int):
        res = self.connection.execute('SELECT * FROM networks WHERE id = ?', [network_id])
        return res.fetchone()[1]

    def get_lang_id_by_name(self, name: str):
        res = self.connection.execute('SELECT * FROM langs WHERE name = ?', [name])
        return res.fetchone()[0]

    def get_lang_name_by_id(self, lang_id: int):
        res = self.connection.execute('SELECT * FROM langs WHERE id = ?', [lang_id])
        return res.fetchone()[1]

    def get_type_id_by_name(self, name: str):
        res = self.connection.execute('SELECT * FROM types WHERE name = ?', [name])
        return res.fetchone()[0]

    def get_type_name_by_id(self, type_id: int):
        res = self.connection.execute('SELECT * FROM types WHERE id = ?', [type_id])
        return res.fetchone()[1]

    def get_tag_name_by_id(self, tags_id: int):
        res = self.connection.execute('SELECT * FROM tags WHERE id = ?', [tags_id])
        return res.fetchone()[1]

    def get_resources(self):
        res = self.connection.execute('SELECT * FROM resources')
        return res.fetchall()

    def get_resources_tags(self):
        res = self.connection.execute('SELECT * FROM resources_tags')
        return res.fetchall()

    def update_resources(self, resources_id: int, network_id: int, lang_id: int, type_id: int):
        return self.connection.execute('UPDATE resources SET network_id = ?, lang_id = ?, type_id = ? WHERE id = ?',
                                    [network_id, lang_id, type_id, resources_id])

    def search_resources_by_url(self, url: str):
        cur = self.connection.cursor()
        res = cur.execute('SELECT R.*,'
                          ' (SELECT RT.tags_id FROM resources_tags RT WHERE RT.resources_id = R.id LIMIT 1) AS tags_id, '
                          ' (SELECT COUNT(DRC.id)  FROM descriptions DRC WHERE DRC.resources_id = R.id) AS cnt, '
                          ' (SELECT D.description FROM descriptions D WHERE D.resources_id = R.id ORDER BY D.id LIMIT 1 ) AS description '
                          'FROM resources R '
                          'WHERE R.url LIKE  ? '
                          'ORDER BY cnt DESC',
                          ['%'+url+'%'])
        return res.fetchall()

    def search_resources_by_description(self, description: str):
        cur = self.connection.cursor()
        res = cur.execute('SELECT * '
                          'FROM '
                          ' (   SELECT R.*,'
                          '     (SELECT RT.tags_id FROM resources_tags RT WHERE RT.resources_id = R.id LIMIT 1) AS tags_id, '
                          '     (SELECT COUNT(DRC.id)  FROM descriptions DRC WHERE DRC.resources_id = R.id) AS cnt, '
                          '     (SELECT D.description FROM descriptions D WHERE D.resources_id = R.id ORDER BY D.id LIMIT 1 ) AS description '
                          '     FROM resources R'
                          ' ) RRR '
                          'WHERE description LIKE  ? '
                          'ORDER BY cnt DESC',
                          ['%'+description+'%'])
        return res.fetchall()

    def check(self):
        cur = self.connection.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND  name NOT LIKE 'sqlite_%';")
        return len(res.fetchall()) > 0
