from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Carrera(Base):
    __tablename__ = 'carrera'

    id_carrera = Column(Integer, primary_key=True)
    nombre = Column(String)
    ganador = Column(String)
    terminada = Column(Boolean)

    competidores = relationship('Competidor', cascade='all,delete,delete-orphan')
    apuestas= relationship('Apuesta', cascade='all,delete,delete-orphan')
