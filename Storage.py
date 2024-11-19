from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Crypto(Base):

    __tablename__ = 'crypto'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(5), nullable=False)
