from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial


class Dialogo_crear_apostador(QDialog):
    #Diálogo para crear o editar un apostador

    def __init__(self,apostador):
        """
        Constructor del diálogo
        """   
        super().__init__()

        
        self.setFixedSize(400, 125)
        self.setWindowIcon(QIcon("src/devcuentasclaras/recursos/smallLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()
        
        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #Si se va a crear un nuevo apostador o se va a editar, usamos el mismo diálogo
        titulo=""
        if(apostador==None):
            titulo="Nuevo Apostador"
        else:
            titulo="Editar Apostador"

        self.setWindowTitle("E-Porra - {}".format(titulo))
       
        #Creación de las etiquetas y los campos de texto

        etiqueta_nombre=QLabel("Nombre")
        distribuidor_dialogo.addWidget(etiqueta_nombre,numero_fila,0)                

        self.texto_nombre=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_nombre,numero_fila,1)
        numero_fila=numero_fila+1

        #Creación de los botones para guardar o cancelar
        caja_botones = QGroupBox()
        caja_botones.setLayout(QHBoxLayout())
        caja_botones.setStyleSheet('''
                QGroupBox{border:none}''')

        self.btn_guardar = QPushButton("Guardar")
        caja_botones.layout().addWidget(self.btn_guardar)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        caja_botones.layout().addWidget(self.btn_cancelar)
        self.btn_cancelar.clicked.connect(self.cancelar)

        distribuidor_dialogo.addWidget(caja_botones, numero_fila, 0, 1, 2)

        #Si el diálogo se va a usar para editar, se pone la información correspondiente en los campos de texto

        if (apostador!=None):
            self.texto_nombre.setText(apostador["Nombre"])


    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """
        nombre = self.texto_nombre.text()
        if (len(nombre) <=0) or (len(nombre.strip())==0):
            self.resultado=0
            self.setWindowTitle("Nombre Invalido")
        else:
            self.resultado=1
            self.close()

        return self.resultado


    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """   

        self.resultado=o
        self.close()
        return self.resultado


