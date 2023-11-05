import argparse


from src.models import Student, Teacher, Subject, Group, Base
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
        self.args = None
        

    def _get_model(self):
        cls_name = self.args.model
        model_cls = globals().get(cls_name)
        if model_cls is not None and issubclass(model_cls, Base):
            return model_cls
  
        raise ValueError(f"Invalid model name: {cls_name} is not a valid model.")
        

    def run(self):
        self.args = self.parser.parse_args()
        model_cls = self._get_model()
        
        match self.args.action:
            case "create":
                if (name:=self.args.name) is None:
                    raise ValueError("name [--name/-n] is required for 'create' action.")
                model_obj = model_cls(name=name) # TODO
                self.crud.create(model_obj)
            case "read":
                if (id:=self.args.id) is None:
                    raise ValueError("id [--id/-i] is required for 'read' action.")
                res = self.crud.read(model_cls, id)
                print(res)
            case "list":
                models = self.crud.read_all(model_cls)
                print("\n".join(map(str,models)))
            case "update":
                pass
            case "delete":
                pass
            case _:
                print("[ERROR]: uncknowon aaction ")

def main():
    dbm = DBManager(url)
    crud_m = CRUDManager(dbm)
    DB_cli = DatabaseCLI(crud_m)
    DB_cli.run()

if __name__ == "__main__":
    main()
    
  