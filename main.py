import sys
from PyQt5.QtWidgets import QApplication
from parse_gui import SSHParserGUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SSHParserGUI()
    gui.show()
    sys.exit(app.exec_())