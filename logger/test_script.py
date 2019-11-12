
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging 
import datetime
from logger_handler import OEREBHttpLogger

from models import Base, HttpLogs


if __name__ == '__main__':
    # simple logging config
    logging.basicConfig(
         format='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger_db_engine = 'sqlite:///logger_db.sqlite3'
    
    engine = create_engine(logger_db_engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    oereb_logger = OEREBHttpLogger(session)

    oereb_logger.setLevel = logging.DEBUG
    logger.addHandler(oereb_logger)
    log_adapter = logging.LoggerAdapter(logger,
                                        {'status':302,
                                         'flavour':'blabla',
                                         'requested_format': 'xml'})
    log_adapter.debug('marche pas')
    

    log_adapter = logging.LoggerAdapter(logger,
                                        {'status':404,
                                         'flavour':'blabla',
                                         'requested_format': 'json',
                                         'service_type': 'GetCapabilities'})
    log_adapter.info('marche pas de nouveau')
