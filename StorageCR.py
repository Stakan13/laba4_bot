from Storage import Crypto
from sqlalchemy.orm import sessionmaker
from database import get_connection

engine = get_connection()
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
session = Session()


def create(name: str):
    crypto = Crypto(name=name)
    session.add(crypto)
    session.commit()
    session.close()


def read(name):
    return session.query(Crypto).filter(Crypto.name == name).all()

