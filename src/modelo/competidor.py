from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Competidor(Base):
    __tablename__ = 'competidor'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    probabilidad = Column(Float)

    carrera = Column(Integer, ForeignKey('carrera.id_carrera'))
    apuestas= relationship('Apuesta', cascade='all,delete,delete-orphan')
