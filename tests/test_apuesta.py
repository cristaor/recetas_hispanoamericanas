import unittest

from src.logica.GestorEporra import GestorEporra
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apuesta import Apuesta
from src.modelo.apostador import Apostador
from src.modelo.declarative_base import Session
from faker import Faker
import random

class CarreraTestCase(unittest.TestCase):

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
        busqueda = self.session.query(Carrera).all()

        '''Borra todos los álbumes'''
        for carrera in busqueda:
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

    def test_sin_apuestas(self):
        #resultado = self.gestor.crear_carrera(nombre="")
        resultado = self.gestor.listar_apuestas()
        self.assertEqual(len(resultado), 0)

    def test_con_apuestas(self):
        for i in range(3):
            valor_apuesta = self.data_factory.pyint(1, 1000)
            apostador1 = self.data_factory.pyint(1, 100)
            competidor1 = self.data_factory.pyint(1, 100)
            carrera1= self.data_factory.pyint(1, 10)
            apuesta1=Apuesta(valor=valor_apuesta, carrera=carrera1, competidor=competidor1, apostador=apostador1)
            self.session.add(apuesta1)
            self.session.commit()

        resultado = self.gestor.listar_apuestas()
        #self.assertEqual(len(resultado), 2)
        self.assertNotEqual(len(resultado), 0)

    def test_crear_apuesta_valor_vacio_o_espacios_blanco(self):
        resultado = self.gestor.crear_apuesta(carrera_id = 1, valor_apuesta = "", competidor_id = 1, apostador_id = 1)
        resultado2 = self.gestor.crear_apuesta(carrera_id = 1, valor_apuesta = "    ", competidor_id = 1, apostador_id = 1)
        self.assertEqual(resultado, False)
        self.assertEqual(resultado2, False)

    def test_crear_apuesta_valor_fuera_rango(self):
        resultado = self.gestor.crear_apuesta(carrera_id = 1, valor_apuesta = 0.1, competidor_id = 1, apostador_id = 1)
        resultado2 = self.gestor.crear_apuesta(carrera_id = 1, valor_apuesta = 400000000000000, competidor_id = 1, apostador_id = 1)
        self.assertEqual(resultado, False)
        self.assertEqual(resultado2, False)

    def test_crear_apuesta_valores_correctos(self):
        nombre_carrera = self.data_factory.bs();
        resultado = self.gestor.crear_carrera(nombre_carrera)
        carrera_id = self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera).first().id_carrera
        #print("consulta id= " + str(carrera_id))

        # Crear Competidor
        probabilidad = self.data_factory.pyfloat(1,2,0,0.0,1.0)
        nombre_competidor = self.data_factory.name()
        creado=self.gestor.crear_competidor(carrera_id, nombre_competidor, probabilidad)
        if creado:
            competidor = self.session.query(Competidor).filter(Competidor.nombre == nombre_competidor).first().id
            #print("Competidor id "+ str(competidor.id))
            nombre_apostador = self.data_factory.name()
            apostador1 = Apostador(nombre=nombre_apostador)
            self.session.add(apostador1)
            self.session.commit()
            apostador_id = self.session.query(Apostador).filter(Apostador.nombre == nombre_apostador).first().id

            valor_apuesta = self.data_factory.pyint(1, 1000)
            resultado=self.gestor.crear_apuesta(carrera_id, valor_apuesta, competidor, apostador_id)

        self.assertEqual(len(resultado), 1)
