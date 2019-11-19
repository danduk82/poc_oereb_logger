import logging
import traceback
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import createLogClass, Base
from sqlalchemy.exc import OperationalError, InvalidRequestError
from sqlalchemy_utils import database_exists, create_database
import threading, time
from .filters import ContainsExpression, DoesNotContainExpression


module_logs = logging.getLogger(__name__)

class SQLAlchemyHandler(logging.Handler):
    
    MAX_NB_LOGS = 100
    MAX_TIMEOUT = 1

    def __init__(self, sqlalchemyUrl, 
              doesNotContainExpression = None,
              containsExpression = None):
        super().__init__()
        # initialize DB session
        self.engine = create_engine(sqlalchemyUrl['url'])
        self.Log = createLogClass(
                  tablename = sqlalchemyUrl.get('tablename', 'logs'),
                  tableargs = sqlalchemyUrl.get('tableargs', None))
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        # initialize log queue
        self.log_queue = []
        # initialize a thread to process the logs Asynchronously
        self.condition = threading.Condition()
        self.processor_thread = threading.Thread(target = self._processor, daemon = True)
        self.processor_thread.start()
        # initialize filters
        if doesNotContainExpression:
             self.addFilter(DoesNotContainExpression(doesNotContainExpression))
        if containsExpression:
             self.addFilter(ContainsExpression(containsExpression))


    def _processor(self):
        while True:
            with self.condition:
                while not self.log_queue:
                    self.condition.wait()
                queue = self.log_queue
                self.log_queue = []
            self._write_logs(queue)


    def _write_logs(self,logs):
       try:
           self.session.bulk_save_objects(logs)
           self.session.commit()
       except (OperationalError, InvalidRequestError):
           try: 
               self.create_db()
               self.session.rollback()
               self.session.bulk_save_objects(logs)
               self.session.commit()
           except Exception as e:
                # if we really cannot commit the log to DB, do not lock the
                # thread and do not crash the application
                module_logs.critical(e)
                pass
       finally:
           self.session.expunge_all()


    def create_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        #FIXME: we should not access directly the private __table_args__
        # variable, but add an accessor method in models.Log class
        if type(self.Log.__table_args__) is not type(None) and self.Log.__table_args__.get('schema', None):
            if not self.engine.dialect.has_schema(self.engine,self.Log.__table_args__['schema']):
                self.engine.execute(sqlalchemy.schema.CreateSchema(self.Log.__table_args__['schema']))
        Base.metadata.create_all(self.engine)


    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = self.Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        with self.condition:
            # put the log in an asynchronous queue
            self.log_queue.append(log)
            self.condition.notify()



