import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os

class Db(object):
    def __init__(self):
        self.engine = sqlalchemy.create_engine(os.environ['BOT_DB'], client_encoding='utf8')
        self.metadata = sqlalchemy.MetaData(bind=self.engine, reflect=True)


    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

# conn, meta = connect()
# events = meta.tables['events']
# clause = events.insert().values(name='Beer', place='CraftHouse', date=datetime.datetime(2018, 1, 12, 20, 0))
# conn.execute(clause)
# for row in conn.execute(events.select()):
#   print(row)