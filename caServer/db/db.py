#from .. import settings
import settings
from .json import JSONDatabase


class DBObject:

    data = None

    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.data[key]

    def __setattr__(self, key, value):
        self.data[key] = value


class Database:

    def __init__(self):
        if settings.DB_TYPE == 'json':
            self.db = JSONDatabase(settings.DB_FILE)
        else:
            raise ValueError(settings.DB_TYPE + " is not a valid database option, see documentation for help")

    def save(self):
        self.db.save()