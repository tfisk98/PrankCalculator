from Calculator import Calculator
from CalcInterface import CalcInterface
from PySide6.QtWidgets import QApplication
import sys


def main():
    print("Hello, User, Welcome to the calculator program!")

    calc = Calculator()
    app = QApplication(sys.argv)
    interface = CalcInterface(calc)
    interface.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

