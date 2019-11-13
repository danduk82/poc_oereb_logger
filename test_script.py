
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging 
import datetime
from sqlalchemylogger.handlers import SQLAlchemyHandler

from sqlalchemylogger.models import Base, Log


if __name__ == '__main__':
    # simple logging config
    logging.basicConfig(
         format='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger_db_engine = 'sqlite:///logger_db.sqlite3'
    
    mylogger = SQLAlchemyHandler(logger_db_engine)
    logger.addHandler(mylogger)
    logger.info('bla')
#
#    oereb_logger = OEREBHttpLogger(session)
#
#    oereb_logger.setLevel = logging.DEBUG
#    logger.addHandler(oereb_logger)
#    log_adapter = logging.LoggerAdapter(logger,
#                                        {'status':302,
#                                         'flavour':'blabla',
#                                         'requested_format': 'xml'})
#    log_adapter.debug('marche pas')
#    
#
#    log_adapter = logging.LoggerAdapter(logger,
#                                        {'status':404,
#                                         'flavour':'blabla',
#                                         'requested_format': 'json',
#                                         'service_type': 'GetCapabilities'})
#    import pdb; pdb.set_trace()
#    log_adapter.info('marche pas de nouveau')
