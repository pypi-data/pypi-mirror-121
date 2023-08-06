import sys
from PyQt5 import QtGui

import qdarkstyle
import serial
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Device import Device
from dialogs.comsDialog import comsDialog
from dynamicDevice import dynamicDevice
from SplashScreen import SplashScreen

import webbrowser


class Window(QWidget):
    def __init__(self, splash):
        """Initializing method for the whole desktop application.
        """

        self.WELCOME_MESSAGE_ENABLED = True

        super().__init__()
        self.setWindowIcon(QtGui.QIcon("./images/logo.png"))
        self.device_list = [] # Keeps track of current opened devices.
        self.com_list = [] # Keeps track of current connected communication ports.
        self.title = 'AtmoSniffer'
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 400
        self.init_ui()

        self.splash = splash
        self.timer = QTimer() # Timer used to wait for splash screen to finish.
        self.timer.timeout.connect(self.check_splash)
        self.timer.start(20)

    def check_splash(self):
        """Function used to check when to enable the main window application."""
        if not self.splash.isVisible():
            self.timer.stop()
            self.setEnabled(True)

    def init_ui(self):
        """Method used to initialize all UI components in the application.
        """
        # Setting basic application components.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Menu Bar Section #
        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu('File')
        self.help_menu = self.menu_bar.addMenu('Help')
        self.view_menu = self.menu_bar.addMenu('View')

        # Exit Button and on click trigger action.
        self.exit_button = QAction('Exit', self)
        self.exit_button.setShortcut('Ctrl+Q')
        self.exit_button.triggered.connect(self.close)

        # Help menu item to direct people to github repository
        self.help_github = QAction('Github', self)
        self.help_menu.addAction(self.help_github)
        self.help_github.triggered.connect(self.redirect_to_github)

        # Menu item for hiding/showing the commandWindow
        self.view_terminal_window = QAction('Terminal', self)
        self.view_menu.addAction(self.view_terminal_window)
        self.view_terminal_window.triggered.connect(self.toggle_terminal_window)

        #Menu item for displaying information about current application.
        self.view_info_popup = QAction('Info', self)
        self.view_menu.addAction(self.view_info_popup)
        self.view_info_popup.triggered.connect(self.show_info_popup)

        # Menu item for opening a file.
        self.open_file = QAction('Open File', self)
        self.open_file.setShortcut('Ctrl+O')
        self.file_menu.addAction(self.open_file)
        self.open_file.triggered.connect(self.read_file)

        # Menu item for connecting to a device
        self.connect_device_menu = QAction('Connect Device', self)
        self.connect_device_menu.setShortcut('Ctrl+D')
        self.file_menu.addAction(self.connect_device_menu)
        self.connect_device_menu.triggered.connect(self.choose_com)

        # This vBoxLayout keeps the menu bar and main frame separated.
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        self.main_layout = QVBoxLayout()

        # Making sure the menu bar stays on top with a stretch of 1.
        self.sp_up = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sp_up.setVerticalStretch(1)

        self.menu_bar.setSizePolicy(self.sp_up)
        self.vbox.addWidget(self.menu_bar)

        # QtextEdit to show data being transmitted:
        self.terminal_window = QTextEdit(self)
        self.terminal_window.setReadOnly(True)
        self.terminal_window.setVisible(False)

        # ScrollArea
        self.form_layout = QFormLayout()
        self.group_box = QGroupBox("Devices")

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.group_box)
        self.scroll.setWidgetResizable(True)

        self.group_box.setLayout(self.form_layout)
        self.scroll.setWidget(self.group_box)

        self.main_frame = QFrame()

        self.sp_down = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sp_down.setVerticalStretch(19)
        self.main_frame.setSizePolicy(self.sp_down)

        self.main_layout.addWidget(self.scroll)
        self.main_frame.setLayout(self.main_layout)
        self.vbox.addWidget(self.main_frame)
        self.vbox.addWidget(self.terminal_window)

        self.setLayout(self.vbox)

        # Set up "Welcome Message":
        if self.WELCOME_MESSAGE_ENABLED:
            self.welcome_label = QLabel()
            self.welcome_label.setFont(QtGui.QFont('Times font', 15))
            self.welcome_label.setText("Welcome to the AtmoSniffer Desktop Application!"+
            "\nYou can either:"+
            "\n1. Open a csv file by going to File > Open File or by using the CTRL + O shortcut"+
            "\n2. Connect to a device by going to File > Connect to Device or using the CTRL + D shortcut.")

        self.form_layout.addRow(self.welcome_label)

        self.setEnabled(False)
        self.showMaximized()

    def redirect_to_github(self):
        """ Method used to redirect users to the github guide/read me file."""
        webbrowser.open("https://github.com/Atmosniffer/atmo_desktop/tree/dynamicDeviceV2#-contents-")

    def show_info_popup(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Info")
        dlg.setText("AtmoSniffer Desktop Application" +
        "\nVersion: 0.1.0"+
        "\nCopyright 2021")
        dlg.setIcon(QMessageBox.Question)
        dlg.exec()

    def toggle_terminal_window(self):
        """ This method is used to display the terminal
        on the bottom of the main window.
        """
        if self.terminal_window.isVisible():
            self.terminal_window.setVisible(False)
        else:
            self.terminal_window.setVisible(True)

    def read_file(self):
        """ Method used to read in static files from past records.
        """
        # Options for the QFileDialog
        # This part will retrieve the default options.
        options = QFileDialog.Options()
        # This part will decide whethere it uses the default options or the selected Option.
        options |= QFileDialog.DontUseNativeDialog

        # variable to keep a path to the selected file within our file system.
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choose File:", "", "All Files (*);;Python Files (*.py)", options=options)

        # Checks if there is a file with such a path, and goes ahead and reads it.
        if file_name != "":
            device_name = file_name.split('/')[-1]
            count = 0

            # Check if there are any duplicate devices with the same name.
            for d in self.device_list:
                if d == device_name:
                    count += 1

            if count == 0:  # If no duplicate devices were found then create it and show it on screen.
                self.remove_welcome_message() # Remove the welcome Message it its showing

                new_device = Device(file_name, self)
                self.form_layout.addRow(new_device)
                new_device.setVisible(True)
                self.device_list.append(new_device.get_device_name())

    def remove_welcome_message(self):
        """ Method used to remove welcome message once the user has decided what to do at first. """
        if self.WELCOME_MESSAGE_ENABLED:
                self.form_layout.removeRow(self.welcome_label)
                self.WELCOME_MESSAGE_ENABLED = False

    def update_devices(self):
        """ Helper method to make sure all devices in the device_list 
        are actually added into the formlayout. """
        for d in self.device_list:
            self.form_layout.addRow(d)

    def close_device(self, device_name, device):
        """ Method used for deleting 'closed' device from the device_list """
        for d in self.device_list:
            if d == device_name:
                self.device_list.remove(d)

        device.setVisible(False)
        device.deleteLater()

    def choose_com(self):
        # This line, will take a bit to run. #
        # It gets a list of all COM ports available on the pc. #
        self.com_list = serial.tools.list_ports.comports()

        """ Pop up method for selecting a communication port. """
        dialog = comsDialog(self)
        dialog.init(self, self.com_list)
        dialog.exec_()

    def connect_device(self, com):
        """ Method for listening to a 'device'/communication port. """
        count = 0
        # Check if device already exists.
        for d in self.device_list:
            if d == com:
                count += 1

        # If no device with the same com exist in our device_list, then proceed.
        if count == 0:
            self.remove_welcome_message() # Remove the welcome Message it its showing

            self.device_list.append(com)
            new_device = dynamicDevice(com, self)
            self.form_layout.addRow(new_device)
            new_device.setVisible(True)


if __name__ == '__main__':
    """Routing in charge of invoking main application and splash screen."""
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    splash = SplashScreen()
    splash.show()

    ex = Window(splash)
    sys.exit(app.exec_())
