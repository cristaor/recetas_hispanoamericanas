from PyQt5.QtWidgets import QApplication

from .Vista_lista_carreras import Vista_lista_carreras
from .Vista_lista_apostadores import Vista_lista_apostadores
from .Vista_carrera import Vista_carrera
from .Vista_lista_apuestas import Vista_lista_apuestas
from .Vista_reporte_ganancias import Vista_reporte_ganancias

class App_EPorra(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_EPorra, self).__init__(sys_argv)
        
        self.logica = logica
        self.mostrar_vista_lista_carreras()
        
        
    def mostrar_vista_lista_carreras(self):
        """
        Esta función inicializa la ventana de la lista de carreras
        """
        self.vista_lista_carreras = Vista_lista_carreras(self) 
        self.vista_lista_carreras.mostrar_carreras(self.logica.listar_carreras())

    def guardar_carrera(self, nombre):
        """
        Esta función guarda una nueva carrera o los cambios sobre una existente
        """
        if self.carrera_actual == -1:
            resultado = self.logica.crear_carrera(nombre)
        else:
            resultado = self.logica.editar_carrera(self.carrera_actual, nombre)
        #if resultado== False:
         #   print("No se puede crear" + str(resultado))
        if resultado != 0:
            self.carrera_actual = resultado[0].id_carrera
            self.vista_lista_carreras.mostrar_carreras(self.logica.listar_carreras())


    def dar_competidor(self, id_competidor):
        """
        Esta función retorna la información de un competidor
        """
        #return self.logica.dar_competidor(self.carrera_actual, id_competidor)
        return self.logica.dar_competidor(id_competidor)

    def aniadir_competidor(self, nombre, probabilidad):
        """
        Esta función inserta un nuevo competidor en la carrera actual
        """
        self.logica.crear_competidor(self.carrera_actual, nombre, probabilidad)
           
    def editar_competidor(self, id_competidor, nombre, probabilidad):
        """
        Esta función edita la información de un competidor en una carrera
        """
        self.logica.editar_competidor(self.carrera_actual, id_competidor, nombre, probabilidad)
    
    def eliminar_competidor(self, id_competidor):
        """
        Esta función elimina un competidor de una carrera
        """
        if self.carrera_actual!=-1:
            self.logica.eliminar_competidor(self.carrera_actual, id_competidor)

    def dar_apostador(self, id_apostador):
        """
        Esta función retorna la información de un competidor
        """
        #return self.logica.dar_competidor(self.carrera_actual, id_competidor)
        return self.logica.dar_apostador(id_apostador)

    def aniadir_apostador(self, nombre):
        """
        Esta función inserta un apostador a la aplicación
        """
        self.logica.crear_apostador(nombre)
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.listar_apostadores())
        
    def editar_apostador(self, id, nombre):
        """
        Esta función edita la información de un apostador
        """
        self.logica.editar_apostador(id, nombre)
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.listar_apostadores())

    def mostrar_apostadores(self):
        """
        Esta función muestra la ventana con la lista de apostadores
        """
        self.vista_lista_apostadores=Vista_lista_apostadores(self)
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.listar_apostadores())

    def dar_apostadores(self):
        """
        Esta función retorna la lista de apostadores desde la lógica
        """
        return self.logica.listar_apostadores()

    def dar_competidores(self):
        """
        Esta función retorna la lista de competidores
        """
        return self.logica.listar_competidores(self.carrera_actual)

    def mostrar_apuestas(self, id_carrera):
        """
        Esta función muestra las apuestas de una carrera
        """
        self.carrera_actual = id_carrera
        #nombre_carrera = self.logica.dar_carrera(id_carrera)['Nombre']
        nombre_carrera = self.logica.dar_carrera(self.carrera_actual)

        self.vista_lista_apuestas=Vista_lista_apuestas(self)
        #print("Valor carrera para apuestas " + str(nombre_carrera) + " de la carrera " +  str(id_carrera));
        if nombre_carrera:
                    #self.vista_carrera.mostrar_competidores(nombre_carrera[0].nombre, self.logica.listar_competidores(self.carrera_actual))
                    self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera[0].nombre, self.logica.listarApuestasPorcarrera(id_carrera))
        #self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera, self.logica.dar_apuestas_carrera(id_carrera))
        else:
            print("No existen apuestas asociadas a esta carrera")

    def dar_apuesta(self, id_apuesta):
        """
        Esta función retorna la información de una apuesta particular
        """
        return self.logica.dar_apuesta(self.carrera_actual, id_apuesta)

    def aniadir_apuesta(self, competidor, valor, apostador):
        """
        Esta función crea una nueva apuesta asociada a una carrera
        """
        competidor2=self.logica.dar_competidorPorNombre(competidor)
        apostador2=self.logica.dar_apostadorPorNombre(apostador)

        #self.logica.crear_apuesta(apostador, self.carrera_actual, valor, competidor)
        aceptado=self.logica.crear_apuesta( self.carrera_actual, valor, competidor2[0].id, apostador2[0].id)
        if aceptado:
            if self.carrera_actual >0:
                nombre_carrera = self.logica.dar_carrera(self.carrera_actual)
                if nombre_carrera:
                    #self.vista_carrera.mostrar_competidores(nombre_carrera[0].nombre, self.logica.listar_competidores(self.carrera_actual))
                    self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera[0].nombre, self.logica.listarApuestasPorcarrera(self.carrera_actual))
        else:
            print("Error al crear la apuesta")

        #nombre_carrera = self.logica.dar_carrera(self.carrera_actual)['Nombre']
        #self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera, self.logica.dar_apuestas_carrera(self.carrera_actual))




    def eliminar_carrera(self, indice_carrera):
        """
        Esta función elimina una carrera
        """
        self.logica.eliminar_carrera(indice_carrera)
        self.vista_lista_carreras.mostrar_carreras(self.logica.dar_carreras())

    def mostrar_reporte_ganancias(self):
        """
        Esta función muestra el reporte de ganancias para una carrera con apuestas
        """
        #lista_ganancias, ganancias_casa = self.logica.dar_reporte_ganancias(self.carrera_actual)
        lista_ganancias = self.logica.calcular_ganancia_apostadores(self.carrera_actual)
        ganancias_casa = self.logica.calcular_ganancia_casa(self.carrera_actual)

        self.vista_reporte_ganancias = Vista_reporte_ganancias(self)
        self.vista_reporte_ganancias.mostrar_ganancias(lista_ganancias, ganancias_casa)


    def eliminar_apostador(self, id_apostador):
        """
        Esta función elimina un apostador
        """
        self.logica.eliminar_apostador(id_apostador)
        self.vista_lista_apostadores.mostrar_apostadores(self.logica.listar_apostadores())

    def eliminar_apuesta(self, id_apuesta):
        """
        Esta función elimina una apuesta
        """
        resultado = self.logica.eliminar_apuesta(self.carrera_actual, id_apuesta)
        print(resultado)
        nombre_carrera = self.logica.dar_carrera(self.carrera_actual)['Nombre']
        self.vista_lista_apuestas.mostrar_apuestas(nombre_carrera, self.logica.dar_apuestas_carrera(self.carrera_actual))
    
    def mostrar_carrera(self, id_carrera=-1):
        """
        Esta función muestra una carrera en la ventana de carreras
        """
        self.carrera_actual = id_carrera
        if id_carrera != -1:
            self.vista_carrera = Vista_carrera(self)
            print("Carrera " + str(self.carrera_actual))

            nombre_carrera = self.logica.dar_carrera(self.carrera_actual)
            if ((isinstance(nombre_carrera, int)) or (isinstance(nombre_carrera, bool))) :
                nombre_carrera2=str(nombre_carrera)
            else:
                nombre_carrera2=nombre_carrera[0].nombre
            print("Nombre carrera " + nombre_carrera2)
            self.vista_carrera.mostrar_competidores(nombre_carrera2, self.logica.listar_competidores(self.carrera_actual))
        else:
            self.vista_carrera = Vista_carrera(self)
            self.vista_carrera.mostrar_competidores('',[])

    def aniadir_competidor(self, nombre, probabilidad):
        """
        Esta función inserta un nuevo competidor en una carrera
        """
        aceptado=self.logica.crear_competidor(self.carrera_actual, nombre, probabilidad)
        print("Carrera actual " + str(self.carrera_actual))
        if aceptado:
            if self.carrera_actual >0:
                nombre_carrera = self.logica.dar_carrera(self.carrera_actual)
                if nombre_carrera:
                    self.vista_carrera.mostrar_competidores(nombre_carrera[0].nombre, self.logica.listar_competidores(self.carrera_actual))
        else:
            print("Error al crear el competidor")

    def terminar_carrera(self, id_carrera, competidor):
        resultado = self.logica.terminar_carrera(id_carrera, competidor)


