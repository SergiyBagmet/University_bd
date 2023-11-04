from src.db import DBManager

class CRUDManager:
    def __init__(self, dbm: DBManager):
        self.dbm = dbm
        
    def create(self, model):
        with self.dbm.connection() as session:
            session.add(model)
        
    def create_many(self, models):
        with self.dbm.connection() as session:
            session.add_all(models)
    
    def read(self, model, primary_key):
        # Метод для чтения объекта по первичному ключу
        with self.dbm.connection() as session:
            return session.query(model).get(primary_key)
    
    def read_all(self, model):
        with self.dbm.connection() as session:
            return session.query(model).all()    

    def update(self, model):
        # Метод для обновления объекта
        with self.dbm.connection() as session:
            session.merge(model)

    def delete(self, model):
        # Метод для удаления объекта
        with self.dbm.connection() as session:
            session.delete(model)
            
    def custom_query(self, query):
        # Выполняет произвольный SQL-запрос и возвращает результат
        with self.dbm.connection() as session:
            result = session.execute(query).all()
        return result