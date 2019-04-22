import json, settings


class JSONDatabase():

    def __init__(self, path):
        try:
            fl = open(path)
            self.path = path
            self.data = json.load(fl)
        except FileNotFoundError:
            fl = open(path, 'w+')
            dict = {}
            for table in settings.TABLES:
                dict.update({table: []})
            json.dump(dict, fl)
            self.data = dict
        except json.JSONDecodeError:
            self.data = []
        fl.close()

    def __getattr__(self, key):
        return self.data[key]

    def get(self, key):
        return self.data[key]

    def save(self):
        with open(self.path, 'w+') as fl:
            jdata = self.data
            json.dump(jdata, fl)