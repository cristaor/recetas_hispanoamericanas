import unittest

from src.logica.GestorEporra import GestorEporra
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.declarative_base import Session

class CompetidorTestCase(unittest.TestCase):

    def setUp(self):
        '''Crear una instancia de GestorEporra'''
        self.gestor = GestorEporra()

        '''iniciar sesion'''
        self.session = Session()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()
        '''Consulta todos los competidores'''
        busqueda = self.session.query(Competidor).all()

        '''Borra todos los competidores'''
        for competidor in busqueda:
            self.session.delete(competidor)

        busqueda2 = self.session.query(Carrera).all()

        '''Borra todos los competidores'''
        for carrera in busqueda2:
            self.session.delete(carrera)

        self.session.commit()
        self.session.close()


    def test_sin_competidores(self):
        #resultado = self.gestor.crear_carrera(nombre="")
        resultado = self.gestor.listar_competidores(id_carrera = -1)
        self.assertEqual(len(resultado), 0)

    def test_con_competidores(self):
        #Crear Carrera
        carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
        self.session.add(carrera1)
        self.session.commit()

        # Crear Competidores
        competidor1 = Competidor(nombre="Juan Pablo Montoya",probabilidad=0.15)
        competidor2 = Competidor(nombre="Michael Schumacher",probabilidad=0.65)
        competidor3 = Competidor(nombre="Kimi Raikkonen",probabilidad=0.2)
        self.session.add(competidor1)
        self.session.add(competidor2)
        self.session.add(competidor3)
        self.session.commit()
         # Relacionar competidores con Carreras
        carrera1.competidores = [competidor1,competidor2,competidor3]
        self.session.commit()

        busqueda = self.session.query(Carrera).filter(Carrera.nombre == carrera1.nombre).all()
        #print ("busqueda " + busqueda[0].nombre)
        if len(busqueda) > 0:
            resultado = self.gestor.listar_competidores(id_carrera = busqueda[0].id_carrera)
        else:
            resultado = busqueda

        self.assertNotEqual(len(resultado), 0)

    def test_crear_competidor_nombre_vacio_o_espacios_blanco(self):
        resultado = self.gestor.crear_competidor(carrera = 1, nombre = "", probabilidad= 0.0)
        resultado2 = self.gestor.crear_competidor(carrera = 1, nombre = "     " , probabilidad= 0.0)
        self.assertEqual(resultado, False)
        self.assertEqual(resultado2, False)

    def test_crear_competidor_probabilidad_invalida(self):
        resultado = self.gestor.crear_competidor(carrera = 1, nombre = "Juan Pablo Montoya", probabilidad= "")
        resultado2 = self.gestor.crear_competidor(carrera = 1, nombre = "Juan Pablo Montoya" , probabilidad= 0)
        resultado3 = self.gestor.crear_competidor(carrera = 1, nombre = "Juan Pablo Montoya" , probabilidad= "     ")
        self.assertEqual(resultado, False)
        self.assertEqual(resultado2, False)
        self.assertEqual(resultado3, False)

    def test_crear_competidor_nombre_correcto(self):
        #Crear Carrera
        carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
        self.session.add(carrera1)
        self.session.commit()

        busqueda = self.session.query(Carrera).filter(Carrera.nombre == carrera1.nombre).all()
        #print ("busqueda " + busqueda[0].nombre)
        if len(busqueda) > 0:
            # Crear Competidores
            resultado = self.gestor.crear_competidor(carrera = busqueda[0].id_carrera, nombre="Juan Pablo Montoya", probabilidad=0.15)
        else:
            resultado = busqueda

        self.assertEqual(resultado, True)

    def test_crear_competidor_nombre_repetido(self):
        #Crear Carrera
        carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
        self.session.add(carrera1)
        self.session.commit()

        busqueda = self.session.query(Carrera).filter(Carrera.nombre == carrera1.nombre).all()
        #print ("busqueda " + busqueda[0].nombre)
        if len(busqueda) > 0:
            # Crear Competidores
            self.gestor.crear_competidor(carrera = busqueda[0].id_carrera, nombre="Juan Pablo Montoya", probabilidad=0.15)
            resultado2 = self.gestor.crear_competidor(carrera = busqueda[0].id_carrera, nombre="Juan Pablo Montoya", probabilidad=0.15)
        else:
            resultado2 = busqueda

        self.assertEqual(resultado2, False)

    def test_crear_competidores_probabilidad_mayor_a_uno(self):
        #Crear Carrera
        carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
        self.session.add(carrera1)
        self.session.commit()

        busqueda = self.session.query(Carrera).filter(Carrera.nombre == carrera1.nombre).all()
        #print ("busqueda " + busqueda[0].nombre)
        if len(busqueda) > 0:
            # Crear Competidores
            resultado2=self.gestor.crear_competidor(carrera = busqueda[0].id_carrera, nombre="Juan Pablo Montoya", probabilidad=1.5)
            #resultado2 = self.gestor.crear_competidor(carrera = busqueda[0].id_carrera, nombre="Juan Pablo Montoya", probabilidad=0.15)
        else:
            resultado2 = busqueda

        self.assertEqual(resultado2, False)

    def test_crear_competidores_suman_probabilidad_mayor_a_uno(self):
        #Crear Carrera
        carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
        self.session.add(carrera1)
        self.session.commit()

        busqueda = self.session.query(Carrera).filter(Carrera.nombre == carrera1.nombre).all()
        #print ("busqueda " + busqueda[0].nombre)
        if len(busqueda) > 0:
            # Crear Competidores
            resultado2=self.gestor.crear_competidor(carrera = busqueda[0].id_carrera, nombre="Juan Pablo Montoya", probabilidad=0.5)
            if resultado2 == True:
                resultado2 = self.gestor.crear_competidor(carrera = busqueda[0].id_carrera, nombre="Kimmi Raikonen", probabilidad=0.6)
        else:
            resultado2 = busqueda

        self.assertEqual(resultado2, False)

    def test_dar_competidor_id_invalido(self):
        resultado = self.gestor.dar_competidor(id_competidor = 0)
        self.assertEqual(resultado, False)

    def test_dar_competidor_id_valido_y_existente_en_db(self):
        resultado = self.gestor.crear_competidor(carrera = 1, nombre="Juan Pablo Montoya", probabilidad=0.5)
        resultado2 = self.gestor.dar_competidor(id_competidor = 1)
        self.assertEqual(len(resultado2), 1)
