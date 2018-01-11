from db import Db
from models import Event

class EventRepository(object):
	def __init__(self):
		self.db = Db()

	def __enter__(self):
		self.session = self.db.create_session()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.session.close()

	def create(self, name, place, date, chat_id):
		event = Event(name=name, place=place, chat_id=chat_id, date=date)
		self.session.add(event)
		self.session.commit()

	def get(self, id):
		return list(self.session.query(Event).filter(Event.id==id))[0]

	def list(self, chat_id):
		return list(self.session.query(Event).filter(Event.chat_id==chat_id))

	def delete(self, chat_id):
		self.session.query(Event).filter(Event.chat_id==chat_id).delete()
		self.session.commit()
		
