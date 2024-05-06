from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Hiljem tuleb päris andmebaas
engine = create_engine('sqlite:///test.db')

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
