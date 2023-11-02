from contextlib import contextmanager

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import create_engine


class DBManager:
    def __init__(self, db_url: str):
        engine = create_engine(db_url, echo=True, pool_size=5, max_overflow=0)
        DBsession = sessionmaker(bind=engine)
        self.session :Session = DBsession()

    @contextmanager
    def connection(self):
        try:
            yield self.session
            self.session.commit()
        except (IntegrityError, SQLAlchemyError) as e:
            self.session.rollback()
            print(f"[Error]: {e}")