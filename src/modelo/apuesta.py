from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Apuesta(Base):
    __tablename__ = 'apuesta'

    id = Column(Integer, primary_key=True)
    valor = Column(String)

    carrera = Column(Integer, ForeignKey('carrera.id_carrera'))
    competidor = Column(Integer, ForeignKey('competidor.id'))
    apostador = Column(Integer, ForeignKey('apostador.id'))
