import sys

import numpy as np
from Utils.MediumClass import Medium
from Windows import app


def main():
    aplicacion = app.QtWidgets.QApplication(sys.argv)
    ventana = app.MainWindow()
    ventana.show()
    sys.exit(aplicacion.exec())


if __name__ == "__main__":
    main()
