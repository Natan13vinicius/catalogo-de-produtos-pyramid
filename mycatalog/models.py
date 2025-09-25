from sqlalchemy import Column, Integer, String, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import zope.sqlalchemy

# Base do SQLAlchemy
Base = declarative_base()

# Sessão global do SQLAlchemy
DBSession = scoped_session(sessionmaker())
zope.sqlalchemy.register(DBSession)

# Modelo de Produto
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image_path = Column(String(255), nullable=True)
