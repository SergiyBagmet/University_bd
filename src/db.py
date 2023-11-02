import configparser
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


file_config = Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "USER")
password = config.get("DB", "PASSWORD")
db_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMEIN")
port = config.get("DB", "PORT")
url = f"postgresql://{username}:{password}@{domain}:{port}/{db_name}"

engine = create_engine(url, echo=True)
DBsession = sessionmaker(bind=engine)
session = DBsession()