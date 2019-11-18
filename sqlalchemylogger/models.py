from sqlalchemy import MetaData, Table, Column
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register

#class Base(object):
#    @declared_attr
#    def __tablename__(cls):
#        return cls.__name__.lower()


DBSession = scoped_session(sessionmaker())
register(DBSession)
#Base = declarative_base(cls=Base)
Base = declarative_base()



class Log(Base):
#    __table_args__ = {'schema': 'logs'}
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True) # auto incrementing
    logger = Column(String) # the name of the logger. (e.g. myapp.views)
    level = Column(String) # info, debug, or error?
    trace = Column(String) # the full traceback printout
    msg = Column(String) # any custom log you may have included
    created_at = Column(DateTime, default=func.now()) # the current timestamp

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])
