from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


DATABASE_NAME = 'Bot'

engine = create_engine('sqlite:///sqlite3.db')

Base = declarative_base()
metadata_obj = MetaData()

Session = sessionmaker(bind=engine)

session = Session()

user = Table(
  "user",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("sums", Integer),
  Column("contacts", String),
  Column("GPS", String)
)

order = Table(
  "order",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("sums", Integer),
  Column("sum_basket", String),
  Column("contacts", String),
  Column("GPS", String)
)


class User(Base):

  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  sums = Column(Integer)
  contacts = Column(String)
  gps = Column(String)
  
  def update_count_offers(id_to_update, new_desc):
    try:
        query = session.query(User).filter(User.contacts == id_to_update).\
            update({User.count_offers: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()


class Order(Base):

  __tablename__ = 'order'

  id = Column(Integer, primary_key=True)
  sums = Column(Integer)
  sum_basket = Column(String)
  contacts = Column(String)
  gps = Column(String)
  
  def update_count_offers(id_to_update, new_desc):
    try:
        query = session.query(Order).filter(Order.GPS == id_to_update).\
            update({Order.count_offers: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()


def creates(what):
  try:
    what.create(engine)
  except:
    return ''


creates(user)
creates(order)