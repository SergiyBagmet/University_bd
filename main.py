import argparse
import typing as t

from src.models import BaseModel
from src.crud import CRUDManager
from src.config import url
from src.db import DBManager


class DatabaseCLI:
    def __init__(self, crud: CRUDManager):
        self.crud = crud
        
        self.parser = argparse.ArgumentParser(description="Database CRUD Operations")
        self.parser.add_argument("--action", "-a", help="Action (create, list, update, remove)", required=True)
        self.parser.add_argument("--model", "-m", help="Model name (Student, Teacher, Subject, Group)", required=True)
        self.parser.add_argument("--name", "-n", help="'Fullname' for (Student, Teacher) or name for (Subject, Group)")
        self.parser.add_argument("--id", "-i", type=int, help="ID for update or remove actions")
        self.parser.add_argument("--group_id", "-g", type=int, help="Group ID")
        self.parser.add_argument("--sub_id", "-s", type=int, help="Subject ID")
        self.parser.add_argument("--teacher_id", "-t", type=int, help="Teacher ID")
        self.parser.add_argument("--student_id", "-st", type=int, help="Student ID")
        
        self.cli_args = vars(self.parser.parse_args())
    
    def _get_model_cls(self):
        cls_name = self.cli_args.get('model')
        model = globals().get(cls_name)
        if model is not None and issubclass(model, BaseModel):
            return model
  
        raise ValueError(f"Invalid model name: {cls_name} is not a valid model.")
    
    def _set_model(self, model: t.Type[BaseModel]):
        column_names = model.get_column_names()[1:] # column names with out id(primary_key)
        model_obj = model()
        for column_name in column_names:
            if (val:=self.cli_args.get(column_name)) is not None:
                setattr(model_obj, column_name, val)     
        return model_obj

    def run(self):
        model = self._get_model_cls()
        
        match self.cli_args.get('action'):
            
            case "create":
                if self.cli_args.get('name') is None:
                    raise ValueError("name [--name/-n] is required for 'create' action.")
                model_obj = self._set_model(model)
                self.crud.create(model_obj)
                
            case "read":
                if (id:=self.cli_args.get('id')) is None:
                    raise ValueError("id [--id/-i] is required for 'read' action.")
                model_obj= self.crud.read(model, id)
                if model_obj is not None:
                    print(model_obj)
                else:
                    print(f"[ERROR]: No record found '{model.__name__}' with id '{id}' to read.")    
                
            case "list":
                data = self.crud.read_all(model)
                print("\n".join(map(str, data)))
                
            case "update":
                if (id := self.cli_args.get('id')) is None:
                    raise ValueError("id [--id/-i] is required for 'update' action.")
                
                existing_obj = self.crud.read(model, id)
                if existing_obj is None:
                    print(f"[ERROR]: No record found with id {id} to update.")
                
                model_obj = self._set_model(model)
                model_obj.id = id
        
                self.crud.update(model_obj)
                print(f"[UPDATE] {model_obj} ")
                
            case "delete":
                if (id:=self.cli_args.get('id')) is None:
                    raise ValueError("id [--id/-i] is required for 'delete' action.")

                if (model_obj:= self.crud.read(model, id)) is None:
                    print(f"[ERROR]: No {model.__name__} found with id {id} to delete or error occurred.")
                else:
                    self.crud.delete(model_obj)
                    print(f"[DELETE] {model_obj} with id {id} has been deleted.")  
            case _:
                print("[ERROR]: Unknown action ")

def main():
    dbm = DBManager(url)
    crud_m = CRUDManager(dbm)
    DB_cli = DatabaseCLI(crud_m)
    DB_cli.run()

if __name__ == "__main__":
    main()
    
    

    
    
    

    