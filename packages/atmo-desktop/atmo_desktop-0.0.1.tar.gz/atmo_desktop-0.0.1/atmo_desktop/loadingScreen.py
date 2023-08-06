from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)
        
        self.movie = QMovie("./images/loading.gif")

        self.label_animation.setMovie(self.movie)

        self.show()


    #Animation loading function
    def startAnimation(self):
        self.movie.start()
        print("started")

    def stopAnimation(self):
        self.movie.stop()
        #self.close()