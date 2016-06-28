import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(os.environ.get('DB_CONNECT_STRING', 'sqlite:///users.db'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from models import *

# noinspection PyUnresolvedReferences
def init_db():
    Base.metadata.create_all(bind=engine)


init_db()

