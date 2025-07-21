from PyQt5.QtWidgets import QApplication
from ui_controller import UIController
import sys

def main():
    app = QApplication(sys.argv)
    window = UIController()
    window.show()
    sys.exit(app.exec() )

if __name__ == "__main__":
    main()

