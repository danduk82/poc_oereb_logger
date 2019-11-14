import logging
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Log, Base
from sqlalchemy.exc import OperationalError, InvalidRequestError

class SQLAlchemyHandler(logging.Handler):
    def __init__(self, sqlalchemyUrl):
        super().__init__()
        self.engine = create_engine(sqlalchemyUrl)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        self.session.add(log)
        try:
            self.session.commit()
        except (OperationalError, InvalidRequestError):
            try: 
                self.create_db()
                self.session.rollback()
                self.session.add(log)
                self.session.commit()
            except:
                 # if we really cannot commit the change to DB, do not lock the
                 # wsgi application
                 pass

