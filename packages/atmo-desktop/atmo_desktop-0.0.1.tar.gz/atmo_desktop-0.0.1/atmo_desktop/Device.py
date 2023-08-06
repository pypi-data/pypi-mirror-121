import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pandas.io.parsers import read_csv
from graphs.Graph import Graph
from dialogs.graphDialog import graphDialog
import os
import csv
from versionParsing import getHeader

class Device(QFrame):
    def __init__(self, file_name, main_window):
        super().__init__()

        self.main_window = main_window
        self.seconds = 0
        self.data_file = file_name
        self.file_name = file_name.split('/')[-1]
        self.device_name = self.file_name
        self.init_ui()
        self.setVisible(False)
        self.graph_type_selection = ""
        self.y_axis = ""
        self.x_axis = ""
        self.cancel_graph_creation = False

    def init_ui(self):
        """Method used to create most of the gui parts."""
        self.setFixedHeight(460)
        self.hbox = QVBoxLayout()

        #Frame containing every selected chart by user.
        self.chart_frame = QFrame()
        #chart_frame.setFrameShape(QFrame.StyledPanel)
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
        self.options_groupbox = QGroupBox(f"Device Options - {self.device_name}")

        #ScrollArea for the graph options.
        self.options_scroll_area = QScrollArea()
        #options_scroll_area.setWidget(options_groupbox)
        self.options_scroll_area.setWidgetResizable(True)
        #self.options_scroll_area.setFixedWidth(120)

        #Creating a space for the option labels read from an input file.
        self.options_vbox.addWidget(self.options_scroll_area)
        self.options_frame.setLayout(self.options_vbox)
        self.chart_frame.setLayout(self.chart_grid_layout)

        #Splitter used to resize both frames above.
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.chart_frame)
        self.splitter.addWidget(self.options_frame)
        self.splitter.setSizes([200,10])

        #self.hbox.addWidget(self.deviceTopBar)
        self.hbox.addWidget(self.splitter)
        self.setLayout(self.hbox)
        self.read_file()

    def close_tab(self, currentIndex):
        """Method used to remove tabs in the tab group."""
        self.tabs.removeTab(currentIndex)

    def set_graph_selection(self, selection):
        """Helper method to keep track of graph type selection."""
        self.graph_type_selection = selection

    def set_axis(self, x, y):
        """Helper method used to set the correct axis names when creating a new graph."""
        self.x_axis = x
        self.y_axis = y

    def set_graph_creation(self, boolean):
        """Lets us know if the user clicked on the cancel button when
        creating a new graph.
        """
        self.cancel_graph_creation = boolean

    #Function used to handle Action Signals sent by checking/unchecking a checkbox.
    def onCheckBox_Toggled(self):
        """Method creates a new graph and adds it to the screen."""
        dialog = graphDialog(self)
        dialog.init(self)
        dialog.exec_()

        if not self.cancel_graph_creation:
            #Here we add a tab to our tab container, we use our custom Graph class which takes 2 arguments for plotting our data.
            #1 for sec_start
            self.tabs.addTab(Graph(self.df[self.x_axis], self.df[self.y_axis], self.x_axis, self.y_axis, self.graph_type_selection), f"{self.x_axis} - {self.y_axis}")

            #Looks for the new tab and sets it as the active tab.
            for index in range(self.tabs.count()):
                if self.tabs.tabText(index) == f"{self.x_axis} - {self.y_axis}":
                    self.tabs.setCurrentIndex(index)

        self.cancel_graph_creation = False

    #Method used to read in a file using a QFileDialog from PyQt5.QtWidgets.
    def read_file(self):
        #Options for the QFileDialog
        options = QFileDialog.Options() #This part will retrieve the default options.
        options |= QFileDialog.DontUseNativeDialog #This part will decide whethere it uses the default options or the selected Option.

        #variable to keep a path to the selected file within our file system.
        file_name = self.data_file

        #Checks if there is a file with such a path, and goes ahead and reads it.
        if file_name:
            f = open(file_name, 'r')
            first_line = f.readline()
            f.close()

            if len(first_line.split(',')) < 50:
                outputFileName = os.path.splitext(file_name)[0] + "_modified.csv"

                with open(file_name, 'r') as inFile, open(outputFileName, 'w') as outfile:
                    r = csv.reader(inFile)
                    w = csv.writer(outfile)
                
                    #Skip first 
                    for x in range(144):
                        next(r)

                    count = 0 # Needed to verify its the first line, so we can add the proper header.

                    for row in r:

                        if count == 0:
                            version = float(row[0])
                            w.writerow(getHeader(version))
                            count += 1
            
                        w.writerow(row)

                file_name = outputFileName
                self.data_file = file_name

            self.df = pd.read_csv(file_name)
            self.df = self.df[self.df.columns.drop(list(self.df.filter(regex='reserved')))]

        # Here we grab the necessary option labels depending on version number.
        self.options_list = list(self.df.columns)

        # Here we add the corresponding options to the option frame
        self.options_list_layout = QFormLayout()
        self.add_graph_button = QPushButton("Add Graph")
        self.close_button = QPushButton("Close Device")

        self.close_button.clicked.connect(self.close_device)
        self.options_list_layout.addRow(self.close_button)

        self.add_graph_button.clicked.connect(self.onCheckBox_Toggled)
        self.options_list_layout.addRow(self.add_graph_button)

        #Adding and displaying all option lables into a groupbox.
        self.options_groupbox.setLayout(self.options_list_layout)
        self.options_scroll_area.setWidget(self.options_groupbox)

    def close_device(self):
        """Method used for calling the clos_device method in main window. """
        # Remove created file to make sure we dont create too much junk.
        os.remove(self.data_file)

        self.main_window.close_device(self.device_name, self)

    def get_device_name(self):
        """Method returns the current device name"""
        return self.device_name

    def get_original_file_name(self):
        """Method returns file being read."""
        return self.file_name