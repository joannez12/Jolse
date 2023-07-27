from sqlalchemy import Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date, Float
import datetime

Base = declarative_base()

def create_items_table(engine):
    Base.metadata.create_all(engine)

class Item(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(250), nullable=False)
    img = Column(String(250))

class Price(Base):
    __tablename__ = "Price"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Product.id'))
    item = relationship(Item)
    sale_price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=False)
    date = Column(Date, default=datetime.date.today())
