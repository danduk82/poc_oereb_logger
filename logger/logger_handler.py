from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging 
import datetime

from models import Base, HttpLogs

class OEREBHttpLogger(logging.Handler):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.setLevel(logging.DEBUG)

    def emit(self, record): 

        self.format(record)

        log_time = datetime.datetime.strptime(record.__dict__['asctime'], "%Y-%m-%d %H:%M:%S,%f")
        http_status = int(record.__dict__.get('status',100))
        service_type=record.__dict__.get('service_type', None)
        requested_format=record.__dict__.get('requested_format', None)
        location_requested=record.__dict__.get('location_requested', None)
        flavour=record.__dict__.get('flavour', None)
        
        #import pdb; pdb.set_trace()
        log_record = HttpLogs(log_time,
                              http_status,
                              service_type=service_type,
                              requested_format=requested_format,
                              location_requested=location_requested,
                              flavour=flavour)

        self.session.add(log_record)
        self.session.commit()



