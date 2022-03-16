from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apuesta import Apuesta
from src.modelo.apostador import Apostador
from src.modelo.declarative_base import engine, Base, session
from sqlalchemy import text

class GestorEporra():

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = session

    #nueva abstraccion para listar contenido envarias pantallas
    def listar_registros(self,clase, atributo, filtro):
        busqueda2 = session.execute(text("SELECT * from " + str(clase) + " " + filtro +  " order by " + atributo ))
        busqueda=busqueda2.mappings().all()
        return busqueda

    def listar_carreras(self):
        return self.listar_registros('Carrera', 'nombre','')

    def crear_carrera(self, nombre):
        if len(nombre) <=0:
            return False
        elif len(nombre.strip())==0:
            return False
        else:
            busqueda = session.query(Carrera).filter(Carrera.nombre == nombre).all()
            if len(busqueda) == 0:
                carrera = Carrera(nombre=nombre, ganador='', terminada=False)
                session.add(carrera)
                session.commit()
                busqueda2 = session.query(Carrera).filter(Carrera.nombre == nombre).all()
                if len(busqueda2)==0:
                    return 0
                else:
                    return busqueda2
            else:
                print("La carrera ya existe " + nombre)
                return False

    def dar_carrera(self, id_carrera):
        return self.dar_atributos_clase('Carrera', "Carreras", 'id_carrera', id_carrera)

    def listar_competidores(self, id_carrera):
        return self.listar_registros('Competidor', 'nombre','where carrera=' + str(id_carrera))

    def crear_competidor(self, carrera, nombre, probabilidad):
        if (len(nombre) <=0) or (len(nombre.strip())==0):
            #print("Nombre invalido ")
            return False
        elif (isinstance(probabilidad, float) !=1):
            #print("Probabilidad Invalida ")
            return False
        elif probabilidad > 1.0:
            print("Probabilidad Mayor del umbral ")
            return False
        else:
            suma_probabilidad = self.validar_probabilidad(probabilidad, carrera)
            if suma_probabilidad <=1.0:
                busqueda = self.session.query(Competidor).filter(Competidor.nombre == nombre).all()
                if len(busqueda) == 0:
                    competidor3 = Competidor(nombre = nombre, probabilidad= probabilidad, carrera = carrera)
                    self.session.add(competidor3)
                    self.session.commit()
                    self.listar_competidores(carrera)
                    return True
                else:
                    print("El competidor ya existe " + nombre)
                    return False
            else:
                print("La suma de las probabilidades es mayor a uno ")
                return False

    def validar_probabilidad(self, probabilidad, carrera):
        competidores = self.listar_competidores(carrera)
        suma=0.0
        if len(competidores) > 0:
            for competidor in competidores:
                print ("Competidor " + str(competidor.probabilidad))
                suma=suma + competidor.probabilidad
            suma = suma + probabilidad
            return suma
        else:
            return 0

    def dar_competidor(self, id_competidor):
        return self.dar_atributos_clase('Competidor', "Competidores", 'id', id_competidor)

    def listarApuestasPorcarrera(self, id_carrera):
        return self.listar_registros('Apuesta, Apostador', 'Apostador.nombre','where Apuesta.carrera=' + str(id_carrera) + " and Apostador.id=Apuesta.apostador")

    def dar_apostador(self, id_apostador):
        return self.dar_atributos_clase('Apostador', "Apostadores", 'id', id_apostador)

    #abstraccion de varios metodos dar_*
    def dar_atributos_clase(self, clase, desc_clase, atributo, valor_atributo):
        if type(valor_atributo) is str:
            valor_atributo2=len(valor_atributo)
        else:
            valor_atributo2=valor_atributo

        if valor_atributo2<=0:
            print("Nuevo registro de " + desc_clase + str(valor_atributo))
            return False
        else:
            busqueda2 = session.execute(text("SELECT * from " + str(clase) +  " where " + atributo +"='" + str(valor_atributo)+"'"))
            busqueda=busqueda2.mappings().all()
            if len(busqueda)==0:
                return False
            else:
                return busqueda

    def listar_apostadores(self):
        return self.listar_registros('Apostador', 'nombre','')

    def listar_apuestas(self):
        return self.listar_registros('Apuesta', 'apostador','')

    def crear_apuesta(self, carrera_id, valor_apuesta, competidor_id, apostador_id):
        if not carrera_id:
            print("Carrera invalida")
            return False
        elif not competidor_id:
            print("Competidor invalido")
            return False
        elif not apostador_id:
            print("Apostador invalido")
            return False
        elif (isinstance(valor_apuesta, float) !=1) and (isinstance(valor_apuesta, int) !=1):
            print("Valor Invalido")
            return False
        elif (valor_apuesta <  1) or (valor_apuesta > 100000000):
            print("Valor fuera del rango (1-100000000)")
            return False
        else:
            apuesta1=Apuesta(valor=valor_apuesta, carrera=carrera_id, competidor=competidor_id, apostador=apostador_id)
            session.add(apuesta1)
            session.commit()
            busqueda2 = session.execute(text("SELECT * from Apuesta where carrera=" + str(carrera_id) + " and apostador=" + str(apostador_id) + " and competidor=" + str(competidor_id)))
            busqueda=busqueda2.mappings().all()
            if len(busqueda)==0:
                return 0
            else:
                return busqueda

    def dar_apostadorPorNombre(self, nombre_apostador):
        return self.dar_atributos_clase('Apostador', "Apostadores", 'nombre', nombre_apostador)

    def dar_competidorPorNombre(self, nombre_competidor):
        return self.dar_atributos_clase('Competidor', "Competidores", 'nombre', nombre_competidor)

    def terminar_carrera(self, id_carrera, nombre_competidor):
        if (len(nombre_competidor) <=0) or (len(nombre_competidor.strip())==0):
            print("Nombre Competidor invalido ")
            return False
        elif (id_carrera <=0) or (not id_carrera):
            print("Carrera invalida")
            return False
        else:
            competidor_id = self.session.query(Competidor).filter(Competidor.nombre == nombre_competidor).first().id
            if(competidor_id > 0):
                carrera = session.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()
                if len(carrera.nombre)==0:
                    return False
                else:
                    carrera.terminada=1
                    carrera.ganador=competidor_id
                    session.commit()
                    return True
            else:
                return False


    def listar_apostadores_reporte(self, id_carrera):
         if (id_carrera <=0) or (not id_carrera):
             print("Carrera invalida")
             apostador={1,2}
             return apostador
         else:
             return self.listar_registros('Apuesta, Apostador', 'Apostador.nombre','where Apuesta.carrera=' + str(id_carrera) + " and Apostador.id=Apuesta.apostador")

    def calcular_ganancia_apostadores(self, id_carrera):
        if (id_carrera <=0) or (not id_carrera):
            print("Carrera invalida")
            return False
        else:
            ganador = self.session.query(Carrera).filter(Carrera.id_carrera == id_carrera).first().ganador
            print("EL ganador es " + str(ganador))
            apuestas=self.listarApuestasPorcarrera(id_carrera)
            lista_ganancias=[]
            #print(apuestas)
            apostador_antiguo=""
            i=0
            ganancias_apostador=0
            for apuesta in apuestas:
                #print("Apostador " + apuesta.nombre)
                if(apostador_antiguo != apuesta.nombre) and i > 0:
                    lista_ganancias.append({'nombre':apostador_antiguo,'valor':ganancias_apostador})
                    print("Gano ",apostador_antiguo, str(ganancia))
                    ganancias_apostador=0

                if apuesta.competidor==int(ganador):
                    probabilidad = self.session.query(Competidor).filter(Competidor.id == apuesta.competidor).first().probabilidad
                    ganancia = self.dar_ganancia_apostador(float(apuesta.valor), probabilidad)
                    #print("Gano " + str(ganancia))
                    ganancias_apostador+=ganancia

                apostador_antiguo=apuesta.nombre
                i=i+1
            lista_ganancias.append({'nombre':apuesta.nombre,'valor':ganancias_apostador})
            print("Gano ",apuesta.nombre, str(ganancia))

            return lista_ganancias

    def dar_ganancia_apostador(self, valor, probabilidad):
        if valor<=0 or probabilidad <=0:
            return 0
        else:
            cuota=round(probabilidad / (1 - probabilidad),2)
            ganancia = round(valor + (valor/cuota),0)
            return ganancia

    def calcular_ganancia_casa(self, id_carrera):
        if (id_carrera <=0) or (not id_carrera):
            print("Carrera invalida")
            return False
        else:
            total_ganancias=0
            total_apuestas=0
            saldo_casa=0
            ganancias=self.calcular_ganancia_apostadores(id_carrera)
            for ganancia in ganancias:
                total_ganancias+=ganancia['valor']

            #calcular total_apuestas
            apuestas=self.listarApuestasPorcarrera(id_carrera)
            for apuesta in apuestas:
                total_apuestas+=float(apuesta.valor)

            saldo_casa=total_apuestas-total_ganancias

            print("ganacias ",total_ganancias," Apuestas ",total_apuestas)

            return saldo_casa
