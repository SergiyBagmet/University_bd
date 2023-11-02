from src.db import DBManager
import typing as t


class CRUDManager:
    def __init__(self, dbm: DBManager):
        self.dbm = dbm

    def create(self, obj: object):
        with self.dbm.connection() as session:
            session.add(obj)
        
    def create_many(self, objects: t.Iterable[object]):
        with self.dbm.connection() as session:
            session.add_all(objects)