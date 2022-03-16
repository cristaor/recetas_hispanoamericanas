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

    def test_sin_carreras(self):
        #resultado = self.gestor.crear_carrera(nombre="")
        resultado = self.gestor.listar_carreras()
        self.assertEqual(len(resultado), 0)

    def test_con_carreras(self):
        self.carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
        self.carrera2 = Carrera(nombre = "100 metros planos",ganador="",terminada=False)
        self.session.add(self.carrera1)
        self.session.add(self.carrera2)
        self.session.commit()
        resultado = self.gestor.listar_carreras()
        #self.assertEqual(len(resultado), 2)
        self.assertIsNotNone(resultado)

    def test_con_carreras_ordenadas_alfabeticamente(self):
        self.carrera1 = Carrera(nombre = "Gran Premio de Monaco",ganador="",terminada=False)
        self.carrera2 = Carrera(nombre = "100 metros planos",ganador="",terminada=False)
        self.session.add(self.carrera1)
        self.session.add(self.carrera2)
        self.session.commit()
        resultado = self.gestor.listar_carreras()
        self.assertEqual(resultado[0].nombre, "100 metros planos")
        self.assertEqual(resultado[1].nombre, "Gran Premio de Monaco")
        #self.assertIsNotNone(resultado)

    def test_crear_carrera_nombre_vacio(self):
        resultado = self.gestor.crear_carrera(nombre = "")
        self.assertEqual(resultado, False)

    def test_crear_carrera_nombre_espacios_blanco(self):
        resultado = self.gestor.crear_carrera(nombre = "      ")
        self.assertEqual(resultado, False)

    def test_crear_carrera_nombre_correcto(self):
        resultado = self.gestor.crear_carrera(nombre = "Carrera de prueba")
        #self.assertNotEqual(resultado, True)
        self.assertEqual(len(resultado), 1)

    def test_crear_carrera_nombre_repetido(self):
        resultado = self.gestor.crear_carrera(nombre = "Carrera de prueba")
        resultado = self.gestor.crear_carrera(nombre = "Carrera de prueba")
        self.assertEqual(resultado, False)

    def test_dar_carrera_id_invalido(self):
        resultado = self.gestor.dar_carrera(id_carrera = 0)
        self.assertEqual(resultado, False)

    def test_dar_carrera_id_valido_no_existente_en_db(self):
        resultado = self.gestor.crear_carrera(nombre = "Carrera de prueba")
        resultado2 = self.gestor.dar_carrera(id_carrera = 51)
        self.assertEqual(resultado2, False)

    def test_dar_carrera_id_valido_y_existente_en_db(self):
        resultado = self.gestor.crear_carrera(nombre = "Carrera de prueba")
        resultado2 = self.gestor.dar_carrera(id_carrera = 1)
        #self.assertEqual(resultado2, True)
        self.assertNotEqual(resultado2, 0)

    def test_carrera_sin_apuestas(self):
        #resultado = self.gestor.crear_carrera(nombre="")
        resultado = self.gestor.listarApuestasPorcarrera(id_carrera=0)
        self.assertEqual(len(resultado), 0)

    def test_carrera_con_apuestas(self):
        nombre_carrera = self.data_factory.bs();
        resultado = self.gestor.crear_carrera(nombre_carrera)
        carrera_id = self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera).first().id_carrera
        #print("consulta id= " + str(carrera_id))

        # Crear Competidor
        probabilidad = self.data_factory.pyfloat(1,2,0,0.0,1.0)
        nombre_competidor = self.data_factory.name()
        creado=self.gestor.crear_competidor(carrera_id, nombre_competidor, probabilidad)
        if creado:
            competidor = self.session.query(Competidor).filter(Competidor.nombre == nombre_competidor).first()
            #print("Competidor id "+ str(competidor.id))
            nombre_apostador = self.data_factory.name();
            apostador1 = Apostador(nombre=nombre_apostador)
            self.session.add(apostador1)
            valor_apuesta = self.data_factory.pyint(0, 1000)
            apuesta1=Apuesta(valor=valor_apuesta, carrera=carrera_id, competidor=competidor.id)
            self.session.add(apuesta1)
            apostador1.apuestas = [apuesta1]
            competidor.apuestas = [apuesta1]
            self.session.commit()

        resultado = self.gestor.listarApuestasPorcarrera(carrera_id)
        self.assertEqual(len(resultado), 1)

    def test_carrera_con_apuestas_ordenadas_por_Apostador_alfabeticamente(self):
        nombre_carrera = self.data_factory.bs();
        resultado = self.gestor.crear_carrera(nombre_carrera)
        carrera_id = self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera).first().id_carrera
        #print("consulta id= " + str(carrera_id))

        # Crear Competidor
        probabilidad = self.data_factory.pyfloat(1,2,0,0.0,1.0)
        nombre_competidor = self.data_factory.name()
        creado=self.gestor.crear_competidor(carrera_id, nombre_competidor, probabilidad)
        if creado:
            competidor = self.session.query(Competidor).filter(Competidor.nombre == nombre_competidor).first()
            #print("Competidor id "+ str(competidor.id))
            apostador1 = Apostador(nombre="Sergio Soler")
            apostador2 = Apostador(nombre="Andres Arenas")
            self.session.add(apostador1)
            self.session.add(apostador2)
            valor_apuesta = self.data_factory.pyint(0, 1000)
            valor_apuesta2 = self.data_factory.pyint(0, 1000)
            apuesta1=Apuesta(valor=valor_apuesta, carrera=carrera_id, competidor=competidor.id)
            apuesta2=Apuesta(valor=valor_apuesta2, carrera=carrera_id, competidor=competidor.id)
            self.session.add(apuesta1)
            self.session.add(apuesta2)
            apostador1.apuestas = [apuesta1]
            apostador2.apuestas = [apuesta2]
            competidor.apuestas = [apuesta1, apuesta2]
            self.session.commit()

        resultado = self.gestor.listarApuestasPorcarrera(carrera_id)
        apostador_aux=self.gestor.dar_apostador(resultado[0].apostador)
        apostador_aux2=self.gestor.dar_apostador(resultado[1].apostador)
        self.assertEqual(apostador_aux[0].nombre, "Andres Arenas")
        self.assertEqual(apostador_aux2[0].nombre, "Sergio Soler")

    def test_sin_apostadores(self):
        #resultado = self.gestor.crear_carrera(nombre="")
        resultado = self.gestor.listar_apostadores()
        self.assertEqual(len(resultado), 0)

    def test_con_apostadores(self):
        for i in range(3):
            nombre_apostador = self.data_factory.name();
            apostador1 = Apostador(nombre=nombre_apostador)
            self.session.add(apostador1)
            self.session.commit()

        resultado = self.gestor.listar_apostadores()
        #self.assertEqual(len(resultado), 2)
        self.assertNotEqual(len(resultado), 0)

    def test_terminar_carrera_parametros_no_validos(self):

        resultado = self.gestor.terminar_carrera(0, "Juan Montoya")
        resultado2 = self.gestor.terminar_carrera(1, "")
        self.assertEqual(resultado, False)
        self.assertEqual(resultado2, False)

    def test_terminar_carrera_parametros_validos(self):
        nombre_carrera = self.data_factory.bs();
        resultado = self.gestor.crear_carrera(nombre_carrera)
        carrera_id = self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera).first().id_carrera
        # Crear Competidor
        probabilidad = self.data_factory.pyfloat(1,2,0,0.0,1.0)
        nombre_competidor = self.data_factory.name()
        creado=self.gestor.crear_competidor(carrera_id, nombre_competidor, probabilidad)
        if creado:
            resultado = self.gestor.terminar_carrera(carrera_id, nombre_competidor)


        self.assertEqual(resultado, True)
    
    def test_listar_apostadores_reporte(self):
       apostadores =  self.gestor.listar_apostadores_reporte(0)
       self.assertNotEqual(len(apostadores), 0)

    def test_listar_apostadores_reporte_con_datos(self):

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
            apostador1 = Apostador(nombre="Carlos Soler")
            apostador2 = Apostador(nombre="Gabriel Arenas")
            self.session.add(apostador1)
            self.session.add(apostador2)
            self.session.commit()
            valor_apuesta = self.data_factory.pyint(0, 1000)
            valor_apuesta2 = self.data_factory.pyint(0, 1000)
            apostador_c = self.gestor.dar_apostadorPorNombre("Carlos Soler")
            apostador_d = self.gestor.dar_apostadorPorNombre('Gabriel Arenas')
            self.gestor.crear_apuesta(carrera_id,valor_apuesta, competidor, apostador_c[0].id)
            self.gestor.crear_apuesta(carrera_id,valor_apuesta2, competidor, apostador_d[0].id)

            
            
            resultado = self.gestor.listar_apostadores_reporte(carrera_id)

            apostador_aux=self.gestor.dar_apostador(resultado[0].apostador)
            apostador_aux2=self.gestor.dar_apostador(resultado[1].apostador)

            self.assertEqual(apostador_aux2[0].nombre, "Gabriel Arenas")
            self.assertEqual(apostador_aux[0].nombre, "Carlos Soler")
    
    def test_validar_ganancia(self):
        nombre_carrera = self.data_factory.bs();
        resultado = self.gestor.crear_carrera(nombre_carrera)
        carrera_id = self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera).first().id_carrera
        #print("consulta id= " + str(carrera_id))

        apostador1 = Apostador(nombre="Carlos Soler")
        apostador2 = Apostador(nombre="Gabriel Arenas")
        self.session.add(apostador1)
        self.session.add(apostador2)
        self.session.commit()
        valor_apuesta = 100
        valor_apuesta2 = 200
        apostador_c = self.gestor.dar_apostadorPorNombre("Carlos Soler")
        apostador_d = self.gestor.dar_apostadorPorNombre('Gabriel Arenas')
        # Crear Competidor
        for i in range(0,2):
            probabilidad = 0.45
       
            nombre_competidor = self.data_factory.name()
            creado=self.gestor.crear_competidor(carrera_id, nombre_competidor, probabilidad)
            if creado:
                competidor = self.session.query(Competidor).filter(Competidor.nombre == nombre_competidor).first().id
                #print("Competidor id "+ str(competidor.id))
                self.gestor.crear_apuesta(carrera_id,valor_apuesta, competidor, apostador_c[0].id)
                self.gestor.crear_apuesta(carrera_id,valor_apuesta2, competidor, apostador_d[0].id)
                
        
        self.gestor.terminar_carrera(carrera_id, nombre_competidor)
        
        resultado2 = self.gestor.calcular_ganancia_apostadores(carrera_id)
        
        
        self.assertEqual(resultado2[0]['nombre'], "Carlos Soler")
        self.assertEqual(resultado2[1]['nombre'], "Gabriel Arenas")
        self.assertEqual(resultado2[0]['valor'], 222.0)
        self.assertEqual(resultado2[1]['valor'], 444.0)
    
    def test_validar_ganancias_casa(self):

        nombre_carrera = self.data_factory.bs();
        resultado = self.gestor.crear_carrera(nombre_carrera)
        carrera_id = self.session.query(Carrera).filter(Carrera.nombre == nombre_carrera).first().id_carrera
        #print("consulta id= " + str(carrera_id))

        apostador1 = Apostador(nombre="Carlos Soler")
        apostador2 = Apostador(nombre="Gabriel Arenas")
        self.session.add(apostador1)
        self.session.add(apostador2)
        self.session.commit()
        valor_apuesta = 100
        valor_apuesta2 = 200
        apostador_c = self.gestor.dar_apostadorPorNombre("Carlos Soler")
        apostador_d = self.gestor.dar_apostadorPorNombre('Gabriel Arenas')
        # Crear Competidor
        for i in range(0,2):
            probabilidad = 0.45
       
            nombre_competidor = self.data_factory.name()
            creado=self.gestor.crear_competidor(carrera_id, nombre_competidor, probabilidad)
            if creado:
                competidor = self.session.query(Competidor).filter(Competidor.nombre == nombre_competidor).first().id
                #print("Competidor id "+ str(competidor.id))
                self.gestor.crear_apuesta(carrera_id,valor_apuesta, competidor, apostador_c[0].id)
                self.gestor.crear_apuesta(carrera_id,valor_apuesta2, competidor, apostador_d[0].id)
                
        
        self.gestor.terminar_carrera(carrera_id, nombre_competidor)
        
        resultado2 = self.gestor.calcular_ganancia_casa(carrera_id)

        self.assertEqual(resultado2, -66.0)





    


