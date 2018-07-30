from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine('sqlite+pysqlite:///db/blockchaindb.sqlite')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

