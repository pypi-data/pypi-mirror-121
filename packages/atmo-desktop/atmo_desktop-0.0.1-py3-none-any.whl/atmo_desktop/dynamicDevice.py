import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QInputDialog

from dialogs.commandDialog import commandDialog
from dialogs.graphDialog import graphDialog
from graphs.dynamicGraph import dynamicGraph
from receiver.comThread import comThread


class dynamicDevice(QFrame):
    def __init__(self, com, main_window):
        super().__init__()

        self.main_window = main_window
        self.com = com
        self.cmd_list_back = []
        self.cmd = []
        self.init_ui()
        self.device_thread = comThread(self.com, self, self.main_window)
        self.device_thread.start()
        self.setVisible(False)
        self.df = pd.DataFrame()
        self.graph_type_selection = ""
        self.y_axis = ""
        self.x_axis = ""
        self.cancel_graph_creation = False

    def init_ui(self):
        """Method used to initialize all gui widgets."""
        self.setFixedHeight(460)

        self.hbox = QVBoxLayout()

        #Frame containing every selected chart by user.
        self.chart_frame = QFrame()
        self.chart_grid_layout = QGridLayout()

        #Tab Container
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.chart_grid_layout.addWidget(self.tabs)

        #Frame containing a list with all available charts that can be created.
        self.options_frame = QFrame()
        #options_frame.setFrameShape(QFrame.StyledPanel)
        self.options_vbox = QVBoxLayout()

        #Checkbox Group Container
        self.options_groupbox = QGroupBox(f"Device Options - {self.get_device_name()}")

        #ScrollArea for the graph options.
        self.options_scroll_area = QScrollArea()
        #options_scroll_area.setWidget(options_groupbox)
        self.options_scroll_area.setWidgetResizable(True)

        #Creating a space for the option labels read from an input file.
        self.options_vbox.addWidget(self.options_scroll_area)
        self.options_frame.setLayout(self.options_vbox)
        self.chart_frame.setLayout(self.chart_grid_layout)

        #Splitter used to resize both frames above.
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.chart_frame)
        self.splitter.addWidget(self.options_frame)
        self.splitter.setSizes([200,10])

        self.cmd_frame = QFrame()
        self.cmd_bar_layout = QHBoxLayout()
        self.cmd_text_box = QLineEdit("cmd")
        self.cmd_button = QPushButton("Send")
        self.cmd_button.clicked.connect(self.send_command)

        self.cmd_list = QComboBox(self)
        self.cmd_list.addItems(["AC", "GAS", "GPS", "Bluetooth", "Dongle", "OLED", "Log", "MB", "PM", "Profiler", "CO2", "External Modules"])
        self.cmd_list.activated[str].connect(self.on_changed_cmd_list)

        self.cmd_bar_layout.addWidget(self.cmd_list)
        self.cmd_frame.setLayout(self.cmd_bar_layout)

        self.hbox.addWidget(self.splitter)
        self.setLayout(self.hbox)

        self.options_list_layout = QFormLayout()
        self.add_graph_button = QPushButton("Add Graph")
        self.add_graph_button.setEnabled(False)
        self.close_button = QPushButton("Close Device")

        self.manual_command_button = QPushButton("Manual Command")

        self.manual_command_button.clicked.connect(self.show_command_dialog)
        self.options_list_layout.addRow(self.manual_command_button)

        self.close_button.clicked.connect(self.close_device)
        self.options_list_layout.addRow(self.close_button)

        self.add_graph_button.clicked.connect(self.onCheckBox_Toggled)
        self.options_list_layout.addRow(self.add_graph_button)

        self.options_list_layout.addRow(self.cmd_frame)

        #Adding and displaying all option lables into a groupbox.
        self.options_groupbox.setLayout(self.options_list_layout)
        self.options_scroll_area.setWidget(self.options_groupbox)


    def show_command_dialog(self):
        """Method creates and shows a command dialog"""
        dialog = commandDialog(self)
        dialog.init(self)
        dialog.exec_()

    def send_manual_command(self, command):
        """Method used to send a command to the device thread"""
        self.device_thread.send_command(command)

    def set_graph_creation(self, boolean):
        """Method used for canceling graph creation"""
        self.cancel_graph_creation = boolean

    def on_changed_cmd_list(self, text):
        """Method used to create a command string and send it to the device thread."""
        if not text == "< Back":
            self.cmd_list_back.append([self.cmd_list.itemText(i) for i in range(self.cmd_list.count())])

        self.cmd_list.clear()

        # First part #
        if not self.cmd: ## First Phase: check if we have started making a command or not.
            if text == "AC":
                self.cmd.append("ac")
                self.cmd_list.addItems(["Enable/Disable", "Set ADDR", "Set Pump", "Read", "Raw", "< Back"])
                self.cmd_list.showPopup()
            elif text == "GAS":
                self.cmd.append("gas")
                self.cmd_list.addItems(["Enable/Disable", "HPC Control", "< Back"])
                self.cmd_list.showPopup()

            elif text == "GPS":
                self.cmd.append("gps")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "Bluetooth":
                self.cmd.append("bluetooth")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "Dongle":
                self.cmd.append("dongle")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "OLED":
                self.cmd.append("oled")
                self.cmd_list.addItems(["msg", "Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "Log":
                self.cmd.append("log")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "MB":
                self.cmd.append("mb")
                self.cmd_list.addItems(["Info", "Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "PM":
                self.cmd.append("pm")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "Profiler":
                self.cmd.append("profiler")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "CO2":
                self.cmd.append("co2")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
            elif text == "External Modules":
                self.cmd.append("exm")
                self.cmd_list.addItems(["Enable/Disable", "< Back"])
                self.cmd_list.showPopup()
        else: ## Second Phase: Here we continue on adding more set options depending on the chosen module on phase 1.
            if text == "Enable/Disable":
                if self.cmd[0] in ["ac", "gas", "dongle", "mb"]:
                    self.cmd_list.addItems(["Disable", "Enabled", "Enabled with Debug output", "< Back"])
                elif self.cmd[0] in ["bluetooth", "oled", "log", "pm", "profiler", "co2", "exm"]:
                     self.cmd_list.addItems(["Disable", "Enabled", "< Back"])
                elif self.cmd[0] in ["gps"]:
                    self.cmd_list.addItems(["Disable", "Enabled", "Enabled with Debug output", "Enabled with Verbose Debug output", "< Back"])

                #Append non require argument to command.
                self.cmd.append("<enabled/disabled>")
                self.cmd_list.showPopup()

            if text == "Info":
                if self.cmd[0] in ["mb"]:
                    self.cmd[0] = "mbi"
                    self.cmd_list.addItems(["Pressure", "Temperature", "Relative Humidity", "Battery Volts", "< Back"])

                self.cmd.append("<mbinfo>")
                self.cmd_list.showPopup()

            if text == "HPC Control":
                if self.cmd[0] in ["gas"]:
                    self.cmd_list.addItems(["Disable", "Enabled", "< Back"])
                    self.cmd[0] = "gashdc"

                self.cmd.append("<hpc/disabled/enabled>")
                self.cmd_list.showPopup()

            if text == "Set Pump":
                if self.cmd[0] in ["ac"]:
                    value, b_value = QInputDialog.getInt(self, 'Input Dialog', 'Value: ')
                    self.clear_cmd_list()

                    self.cmd.append("pump")
                    self.cmd.append(f"{value}")
                    self.cmd.append("<end>")

            if text == "Read":
                if self.cmd[0] in ["ac"]:
                    self.clear_cmd_list()
                    self.cmd.append("read")
                    self.cmd.append("<end>")

            if text == "Raw":
                if self.cmd[0] in ["ac"]:
                    self.clear_cmd_list()
                    self.cmd.append("raw")
                    self.cmd.append("<end>")

            if text == "< Back":
                self.cmd_list.addItems(self.cmd_list_back.pop())
                self.cmd.pop()
                self.cmd_list.showPopup()

            if text == "Disable":
                if self.cmd[0] in ["ac", "gas", "gps", "gashdc", "dongle", "bluetooth", "oled", "log", "mb", "pm", "profiler", "co2", "exm"]:
                    self.clear_cmd_list()

                    self.cmd.append("0")
                    self.cmd.append("<end>")

            if text == "Enabled":
                if self.cmd[0] in ["ac", "gas", "gps", "gashdc", "dongle", "bluetooth", "oled", "log", "mb", "pm", "profiler", "co2", "exm"]:
                    self.clear_cmd_list()

                    self.cmd.append("1")
                    self.cmd.append("<end>")

            if text == "Enabled with Debug output":
                if self.cmd[0] in ["ac", "gas", "gps", "dongle", "mb"]:
                    self.clear_cmd_list()

                    self.cmd.append("2")
                    self.cmd.append("<end>")

            if text == "Enabled with Verbose Debug output":
                if self.cmd[0] in ["ac", "gas", "gps"]:
                    self.clear_cmd_list()

                    self.cmd.append("3")
                    self.cmd.append("<end>")

            if text == "Pressure":
                if self.cmd[0] in ["mbi"]:
                    self.clear_cmd_list()

                    self.cmd.append("1")
                    self.cmd.append("<end>")

            if text == "Temperature":
                if self.cmd[0] in ["mbi"]:
                    self.clear_cmd_list()

                    self.cmd.append("2")
                    self.cmd.append("<end>")

            if text == "Relative Humidity":
                if self.cmd[0] in ["mbi"]:
                    self.clear_cmd_list()

                    self.cmd.append("3")
                    self.cmd.append("<end>")

            if text == "Battery Volts":
                if self.cmd[0] in ["mbi"]:
                    self.clear_cmd_list()

                    self.cmd.append("4")
                    self.cmd.append("<end>")

            ## Third Phase: check if command string contains <end>
            ## If so, clean it up, construct it, and send it to device thread.
            if self.cmd:
                for c in self.cmd:
                    if c == "<end>":
                        self.clean_cmd()
                        command = " ".join(self.cmd)
                        self.device_thread.send_command(command)
                        self.cmd = []

    def clean_cmd(self):
        """Method used to clean command string from special command characters."""
        for c in self.cmd:
            if "<" in c and ">" in c:
                self.cmd.remove(c)

    def clear_cmd_list(self):
        """Method used to clear up the command string."""
        while len(self.cmd_list_back) > 0:
            self.cmd_list.clear()
            self.cmd_list.addItems(self.cmd_list_back.pop())

    def onCheckBox_Toggled(self):
        """Method used to create a graph and add it to the main window."""
        dialog = graphDialog(self)
        dialog.init(self)
        dialog.exec_()

        if not self.cancel_graph_creation:
            tab_name = f"{self.x_axis} - {self.y_axis}, {self.graph_type_selection}"

            self.tabs.addTab(dynamicGraph(self.x_axis, self.y_axis, self, self.graph_type_selection), tab_name)

            #Looks for the new tab and sets it as the active tab.
            for index in range(self.tabs.count()):
                if self.tabs.tabText(index) == tab_name:
                    self.tabs.setCurrentIndex(index)

        self.cancel_graph_creation = False

    def close_device(self):
        """Method used for closing a device."""
        self.device_thread.stop()
        self.main_window.close_device(self.com, self)

    def close_tab(self, currentIndex):
        """Method used for closing an opened tab."""
        self.tabs.removeTab(currentIndex)

    def resume_thread(self):
        """Method used to resume the current's device thread."""
        self.device_thread.resume()
        self.device_thread.start()

    def stop_thread(self):
        """Method used to stop thread once a device has been closed."""
        self.device_thread.stop()

    def get_device_name(self):
        """Method returns current device's name"""
        return self.com

    def get_data(self):
        """Method used to return data to device's thread."""
        return self.df

    def update_data_frame(self, d):
        """Method used to update current device's data frame."""
        self.df = d

    def get_com(self):
        """Method used to get current com port."""
        return self.com

    def send_command(self):
        """Method used to send command to device's thread."""
        self.device_thread.send_command(self.cmd_text_box.text())
        self.cmd_text_box.setText("")

    def update_df(self, df):
        """Method used to update current device's data frame."""
        self.df = df

    def set_graph_selection(self, selection):
        """Method used to set the graph selection depending on users choices."""
        self.graph_type_selection = selection

    def set_axis(self, x, y):
        """Method used to set graph axis selections."""
        self.x_axis = x
        self.y_axis = y

    def get_axis_data(self, x_axis, y_axis):
        """Method used to get axis data from device's data frame."""
        return self.df[x_axis], self.df[y_axis]
