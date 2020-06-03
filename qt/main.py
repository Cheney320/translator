import sys
from qt.window_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from train_models.language_detector import LanguageDetector


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

