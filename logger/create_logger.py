from .models import HttpLogs, Base
from sqlalchemy import create_engine

def main():
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///logger_db.sqlite3')
     
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

if __name__ == '__main__':
     main()
