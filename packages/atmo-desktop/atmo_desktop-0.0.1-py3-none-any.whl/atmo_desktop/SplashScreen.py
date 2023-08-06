from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from PyQt5 import QtCore

class SplashScreen(QWidget):
    """ Class used to create a Splash Screen Widget
        It also creates a small progress bar which takes n times to completion.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Splash Screen")
        self.setFixedSize(500,500)
        #self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setWindowFlag(QtCore.Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300 # total instance

        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(10)


    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.label_title = QLabel(self.frame)
        self.label_title.setObjectName('LabelTitle')

        # center label title
        self.label_title.resize(self.width() - 10, 150)
        self.label_title.move(0,0) # x, y
        self.label_title.setText('AtmoSniffer Desktop App')
        self.label_title.setAlignment(Qt.AlignCenter)

        #self.labelDescription = QLabel(self.frame)

        self.label_image = QLabel(self.frame)
        self.label_image.setFixedSize(200, 200)
        self.label_image.move(self.width()/2 - 100, self.label_title.height())
        pixmap = QPixmap("./images/logo.png")
        pixmap = pixmap.scaledToHeight(self.label_image.height(), Qt.SmoothTransformation)
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar(self.frame)
        self.progress_bar.resize(self.width() - 200 - 10, 20)
        self.progress_bar.move(100, self.label_image.height() + 200)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFormat('%p%')
        self.progress_bar.setRange(0, self.n)
        self.progress_bar.setValue(20)

        self.label_loading = QLabel(self.frame)
        self.label_loading.resize(self.width() - 10, 50)
        self.label_loading.move(0, self.progress_bar.y() + 20)
        self.label_loading.setObjectName("label_loading")
        self.label_loading.setAlignment(Qt.AlignCenter)
        self.label_loading.setText("Loading all components...")

    def loading(self):
        self.progress_bar.setValue(self.counter)

        if self.counter >= self.n:
            self.timer.stop()
            self.close()

        self.counter += 1
