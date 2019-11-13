import logging
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Log, Base

class SQLAlchemyHandler(logging.Handler):
    def __init__(self, sqlalchemyUrl):
        super().__init__()
        engine = create_engine(sqlalchemyUrl)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    # A very basic logger that commits a LogRecord to the SQL Db
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
        self.session.commit()
