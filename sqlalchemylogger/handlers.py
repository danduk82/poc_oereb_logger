import logging
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Log, Base
from sqlalchemy.exc import OperationalError, InvalidRequestError
import threading, queue, time


class SQLAlchemyHandler(logging.Handler):
    
    MAX_NB_LOGS = 100
    MAX_TIMEOUT = 5

    def __init__(self, sqlalchemyUrl):
        super().__init__()
        # initialize DB session
        self.engine = create_engine(sqlalchemyUrl)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        # initialize log queue
        self.log_queue = queue.Queue()
        # initialize a thread to process the logs Asynchronously
        self.processor_thread = threading.Thread(target = self._processor)
        self.processor_thread.start()


    def _processor(self):
        _terminated = False
        while not _terminated:
            logs = []
            time_since_last = time.time()
            while True:
                try:
                    log = self.log_queue.get(timeout=self.MAX_TIMEOUT)
                    if log is None:
                        # one way of killing a thread
                        _terminated = True
                    logs.append(log)
                except queue.Empty:
                     pass
                if len(logs) > 0:
                    if (len(logs) >= self.MAX_NB_LOGS) or (time_since_last + self.MAX_TIMEOUT <= time.time()) :
                        self._writeLogs(logs)
                        self.log_queue.task_done()
                        break


    def _writeLogs(self,logs):
       self.session.bulk_save_objects(logs)
       try:
           self.session.commit()
       except (OperationalError, InvalidRequestError):
           try: 
               self.create_db()
               self.session.rollback()
               self.session.bulk_save_objects(logs)
               self.session.commit()
           except:
                # if we really cannot commit the log to DB, do not lock the
                # thread and do not crash the application
                pass
       finally:
            self.session.expunge_all()


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
        # put the log in an asynchronous queue
        self.log_queue.put(log)



