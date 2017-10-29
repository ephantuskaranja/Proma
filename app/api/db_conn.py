from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, sys
from ..models import Customer



Base = declarative_base()

def get_db_session():
    try:
        
        # engine = create_engine(os.environ.get('mssql+pyodbc://sa:max2017@#@192.168.1.185:1433/coffee'), echo=False)
        # engine = create_engine("mssql+pymssql://sa:tiger@hostname:port/dbname'))
        engine = create_engine("mssql+pymssql://sa:'max2017@#'@192.168.1.185:1433/coffee")
        
        print("CONNECTED TO THE DB SUCCESSFULLY");
    except OperationalError:
        sys.stderr.write("PROBLEM IN CONNECTING TO THE DATABASE\n")
        sys.exit(1)

    Base = declarative_base()
    Session = sessionmaker(bind = engine, autoflush=False)
    session = Session()
    return session

# class Customers(Base):
#     __table__ = Base.metadata.tables['customers']

# class Buildings(db.Model):
#     __table__ = db.Model.metadata.tables['test']
#     __bind_key__ = 'chet'
#     def __repr__(self):
#         return self.test1

# class Customers(Base):
#     __table__ = Base.metadata.tables['customers']
#     __bind_key__ = 'customers'


def get_customers():
    session = get_db_session
    customers = session.query(Customer).all()
    return customers

if __name__ == '__main__':
   customers = get_customers()
   print(len(customers))