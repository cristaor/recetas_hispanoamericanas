import unittest

from src.logica.GestorEporra import GestorEporra
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apuesta import Apuesta
from src.modelo.apostador import Apostador
from src.modelo.declarative_base import Session
from faker import Faker
import random



class ApostadorTestCase(unittest.TestCase):

    def setUp(self):
        '''Crear una instancia de GestorEporra'''
        self.gestor = GestorEporra()

        '''iniciar sesion'''
        self.session = Session()

        '''Crea una isntancia de Faker'''
        self.data_factory = Faker()


    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()
        '''Consulta todos los álbumes'''
        busqueda = self.session.query(Competidor).all()

        '''Borra todos los competidores'''
        for competidor in busqueda:
            self.session.delete(competidor)

        busqueda2 = self.session.query(Carrera).all()

        '''Borra todos los competidores'''
        for carrera in busqueda2:
            self.session.delete(carrera)

        busqueda3 = self.session.query(Apostador).all()

        '''Borra todos los aspostadores'''
        for apostador in busqueda3:
            self.session.delete(apostador)

        busqueda4 = self.session.query(Apuesta).all()

        '''Borra todas las apuestas'''
        for apuesta in busqueda4:
            self.session.delete(apuesta)

        self.session.commit()
        self.session.close()


    def test_sin_apostadores(self):
        #resultado = self.gestor.crear_carrera(nombre="")
        resultado = self.gestor.listar_apostadores()
        self.assertEqual(len(resultado), 0)

    def test_con_apostadores(self):
        nombre_apostador1 = self.data_factory.name()
        nombre_apostador2 = self.data_factory.name()
        apostador1 = Apostador(nombre=nombre_apostador1)
        apostador2 = Apostador(nombre=nombre_apostador2)
        self.session.add(apostador1)
        self.session.add(apostador2)
        self.session.commit()
        resultado = self.gestor.listar_apostadores()
        self.assertNotEqual(len(resultado), 0)

    def test_crear_apostador_nombre_incorrecto(self):
        resultado = self.gestor.crear_apostador(nombre = "")
        resultado2 = self.gestor.crear_apostador(nombre = "     ")
        self.assertEqual(resultado, False)
        self.assertEqual(resultado2, False)

    def test_crear_apostador_nombre_correcto(self):
        nombre_apostador1 = self.data_factory.name()
        resultado = self.gestor.crear_apostador(nombre = nombre_apostador1)
        self.assertEqual(resultado, True)

    def test_crear_carrera_nombre_repetido(self):
        nombre_apostador1 = self.data_factory.name()
        resultado = self.gestor.crear_apostador(nombre = nombre_apostador1)
        resultado2 = self.gestor.crear_apostador(nombre = nombre_apostador1)
        self.assertEqual(resultado2, False)
