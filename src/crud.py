import typing as t

from src.db import DBManager
from src.models import BaseModel

class CRUDManager:
    def __init__(self, dbm: DBManager):
        self.dbm = dbm
        
    def create(self, model: BaseModel):
        with self.dbm.connection() as session:
            session.add(model)
        
    def create_many(self, models: t.Iterable[BaseModel]):
        with self.dbm.connection() as session:
            session.add_all(models)
    
    def read(self, model: t.Type[BaseModel], primary_key: int) -> BaseModel | None:
        # Метод для чтения объекта по первичному ключу
        with self.dbm.connection() as session:
            return session.query(model).get(primary_key)
    
    def read_all(self, model: t.Type[BaseModel]):
        with self.dbm.connection() as session:
            return session.query(model).all()    

    def update(self, model: BaseModel):
        # Метод для обновления объекта
        with self.dbm.connection() as session:
            session.merge(model)

    def delete(self, model: BaseModel):
        # Метод для удаления объекта
        with self.dbm.connection() as session:
            session.delete(model)
        return True
            
    def custom_query(self, query):
        # Выполняет произвольный SQL-запрос и возвращает результат
        with self.dbm.connection() as session:
            result = session.execute(query).all()
        return result