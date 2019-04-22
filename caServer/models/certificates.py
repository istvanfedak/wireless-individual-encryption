from ..db.db import Database
from datetime import datetime


class Certificates(Database):

    def __init__(self):
        super().__init__('Certificates')