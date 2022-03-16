from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial


class Dialogo_crear_apuesta(QDialog):
    #Diálogo para crear o editar una apuesta

    def __init__(self, apostadores, competidores, apuesta=None):
        """
        Constructor del diálogo
        """   
        super().__init__()

        
        self.setFixedSize(340, 250)
        self.setWindowIcon(QIcon("src/devcuentasclaras/recursos/smallLogo.png"))

        self.resultado = ""
        self.apostadores = apostadores
        self.competidores = competidores

        self.widget_lista = QListWidget()
        

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #Si el diálogo se usa para crear o editar, el título cambia.

        titulo=""
        if(apuesta==None):
            titulo="Nueva apuesta"
        else:
            titulo="Editar apuesta"
      

        self.setWindowTitle(titulo)

        #Creación de las etiquetas y campos de texto

        etiqueta_concepto=QLabel("Apostador")
        distribuidor_dialogo.addWidget(etiqueta_concepto,numero_fila,0)                


        self.combobox_apostadores = QComboBox(self)
        for apostador2 in self.apostadores:
            if type(apostador2) is dict:
                apostador=apostador2
            else:
                apostador=dict(apostador2)
            self.combobox_apostadores.addItem(apostador["nombre"])
        distribuidor_dialogo.addWidget(self.combobox_apostadores,numero_fila,1,1,3)
        numero_fila=numero_fila+1


        etiqueta_valor=QLabel("Valor")
        distribuidor_dialogo.addWidget(etiqueta_valor,numero_fila,0)                

        self.texto_valor=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_valor,numero_fila,1,1,3)
        numero_fila=numero_fila+1

        etiqueta_viajero=QLabel("Competidor")
        distribuidor_dialogo.addWidget(etiqueta_viajero,numero_fila,0)                

        
        self.combobox_competidores = QComboBox(self)
        for competidor2 in self.competidores:
            if type(competidor2) is dict:
                competidor=competidor2
            else:
                competidor=dict(competidor2)
            self.combobox_competidores.addItem(competidor["nombre"])
        distribuidor_dialogo.addWidget(self.combobox_competidores,numero_fila,1,1,3)

        numero_fila=numero_fila+1

        #Creación de los botones para guardar o cancelar

        if(len(apostadores)>0):
            self.btn_guardar = QPushButton("Guardar")
            distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
            self.btn_guardar.clicked.connect(self.guardar)
        else:
            self.setWindowTitle("No se puede Crear apuesta. No existen apostadores")

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Si el diálogo se usa para editar, se debe poblar con la información del gasto a editar
        if apuesta != None:
            self.texto_valor.setText(str(apuesta["valor"]))
            indice_apostador = self.combobox_apostadores.findText(apuesta["apostador"])
            self.combobox_apostadores.setCurrentIndex(indice_apostador)
            indice_competidor = self.combobox_competidores.findText(apuesta["competidor"])
            self.combobox_competidores.setCurrentIndex(indice_competidor)

    
    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """   
        try:
            valor = int(self.texto_valor.text())
            print ("Valor apuesta" + str(valor))
            isInt=True

        except:
            isInt=False

        if not isInt:
            error="Valor debe ser numerico"
        elif (valor > 100000000) or (valor <=1):
            error="Valor fuera del rango (1-100000000)"
        else:
            error=""

        if (len(error) > 0):
            titulo=error
            self.resultado=0
            self.setWindowTitle(titulo)
            #self.close()
        else:
            self.resultado=1
            self.close()
        return self.resultado


    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """   
        self.resultado=0
        self.close()
        return self.resultado

