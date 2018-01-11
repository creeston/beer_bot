from db import Db
from sqlalchemy import Table, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
	__tablename__ = 'event'

	id = Column(Integer, primary_key=True)
	chat_id = Column(Integer)
	name = Column(String(50))
	place = Column(String(50))
	date = Column(DateTime)


if __name__ == "__main__":
	db = Db()
	Base.metadata.create_all(db.engine)
