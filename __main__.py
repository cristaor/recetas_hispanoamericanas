import sys
from PyQt5.QtWidgets import QApplication
from src.vista.InterfazEPorra import App_EPorra
from src.logica.GestorEporra import GestorEporra

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = GestorEporra()

    app = App_EPorra(sys.argv, logica)
    sys.exit(app.exec_())
