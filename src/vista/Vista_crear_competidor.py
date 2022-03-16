from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial

class Dialogo_crear_competidor(QDialog):
    #Diálogo para crear un competidor

    def __init__(self, competidor=None):
        """
        Constructor del diálogo
        """    
        super().__init__()

        self.setFixedSize(400,110)
        
        self.setWindowIcon(QIcon("src/recursos/smallLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #El título del diálogo varía si se usa para crear o editar un competidor

        titulo=""
        if competidor is None:
            titulo="Nuevo Competidor"
        else:
            titulo="Editar Competidor"
        self.setWindowTitle(titulo)
        
        #Creación de las etiquetas

        etiqueta_nombre=QLabel("Nombre")
        distribuidor_dialogo.addWidget(etiqueta_nombre,numero_fila,0,1,3)                
        

        self.texto_nombre=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_nombre,numero_fila,1,1,3)
        numero_fila=numero_fila+1

        etiqueta_probabilidad=QLabel("Probabilidad")
        distribuidor_dialogo.addWidget(etiqueta_probabilidad,numero_fila,0,1,3)                
        

        self.texto_probabilidad=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_probabilidad,numero_fila,1,1,3)
        numero_fila=numero_fila+1


        #Creación de los botones
        
        self.btn_guardar = QPushButton("Guardar")
        distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Si el diálogo se usa para editar, se debe mostrar el nombre de la actividad a editar
        
        if (competidor!=None):
            self.texto_nombre.setText(competidor['Nombre'])
            self.texto_probabilidad.setText(str(competidor['Probabilidad']))

    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """
        try:
            probabilidad = float(self.texto_probabilidad.text())
            print ("Probabilidad " + str(probabilidad))
            isfloat=True
        except:
            isfloat=False

        nombre = self.texto_nombre.text()

        if (len(nombre) <=0) or (len(nombre.strip())==0):
            error="Nombre Invalido"
        elif not isfloat:
            error="probabilidad debe ser numerica"
        elif (probabilidad > 1.0) or (probabilidad <=0):
            error="probabilidad debe ser entre 0.1 y 1.0"
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


