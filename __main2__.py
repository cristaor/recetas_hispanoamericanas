from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta

from src.modelo.declarative_base import Session, engine, Base

if __name__ == '__main__':
   #Crea la BD
   Base.metadata.create_all(engine)

   #Abre la sesion
   session = Session()

   #crear carrera
   carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
   carrera2 = Carrera(nombre = "100 metros planos",ganador="",terminada=False)
   session.add(carrera1)
   session.add(carrera2)
   session.commit()

   # Crear Competidores
   competidor1 = Competidor(nombre="Juan Pablo Montoya",probabilidad=0.15)
   competidor2 = Competidor(nombre="Michael Schumacher",probabilidad=0.65)
   competidor3 = Competidor(nombre="Kimi Raikkonen",probabilidad=0.2)
   competidor4 = Competidor(nombre="Usain Bolt",probabilidad=0.7)
   competidor5 = Competidor(nombre="Robson da Silva",probabilidad=0.3)
   session.add(competidor1)
   session.add(competidor2)
   session.add(competidor3)
   session.add(competidor4)
   session.add(competidor5)
   session.commit()

   # Crear Apostadores
   apostador1 = Apostador(nombre="Carlos Perez")
   apostador2 = Apostador(nombre="Juan Mendez")
   session.add(apostador1)
   session.add(apostador2)

   # Crear Apuestas
   apuesta1 = Apuesta(valor="300")
   apuesta2 = Apuesta(valor="100")
   apuesta3 = Apuesta(valor="20")
   apuesta4 = Apuesta(valor="38")
   apuesta5 = Apuesta(valor="247")
   session.add(apuesta1)
   session.add(apuesta2)
   session.add(apuesta3)
   session.add(apuesta4)
   session.add(apuesta4)

   # Relacionar competidores con Carreras
   carrera1.competidores = [competidor1,competidor2,competidor3]
   carrera2.competidores = [competidor4,competidor5]
   session.commit()

   # Relacionar apuestas con apostadores
   apostador1.apuestas = [apuesta1,apuesta2]
   apostador2.apuestas = [apuesta3,apuesta4,apuesta5]
   session.commit()

   # Relacionar apuestas con competidores
   competidor1.apuestas = [apuesta1]
   competidor2.apuestas = [apuesta2]
   competidor3.apuestas = [apuesta3]
   competidor4.apuestas = [apuesta4]
   competidor5.apuestas = [apuesta5]
   session.commit()

   # Relacionar apuestas con carreras
   carrera1.apuestas = [apuesta1, apuesta2, apuesta3]
   carrera2.apuestas = [apuesta4, apuesta5]
   session.commit()


   session.commit()
   session.close()
