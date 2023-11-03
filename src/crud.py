import typing as t

from src.db import DBManager

class CRUDManager:
    def __init__(self, dbm: DBManager):
        self.dbm = dbm
        self.session = dbm.connection()

    def create(self, obj: object):
        with self.dbm.connection() as session:
            session.add(obj)
        
    def create_many(self, objects: t.Iterable[object]):
        with self.dbm.connection() as session:
            session.add_all(objects)
    
    def read(self, model, primary_key):
        # Метод для чтения объекта по первичному ключу
        with self.dbm.connection() as session:
            return session.query(model).get(primary_key)

    def update(self, obj):
        # Метод для обновления объекта
        with self.dbm.connection() as session:
            session.merge(obj)

    def delete(self, obj):
        # Метод для удаления объекта
        with self.dbm.connection() as session:
            session.delete(obj)
            
    def custom_query(self, query):
        # Выполняет произвольный SQL-запрос и возвращает результат
        with self.dbm.connection() as session:
            result = session.execute(query).all()
        return result