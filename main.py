from PyQt5.QtWidgets import QFileDialog, QPushButton, QHBoxLayout, QRadioButton, QGridLayout,QStyleFactory,QApplication, \
    QLineEdit, QLabel, QListWidget, QGroupBox, QCheckBox, QComboBox,QDialog, QDialogButtonBox, QTabWidget, QWidget, QVBoxLayout
import sys
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets, QtWebEngineWidgets
import pandas as pd
import plotly.graph_objs as go

class TabWidget(QDialog):
    def __init__(self, data):
        super(TabWidget, self).__init__()
        self.data = data
        self.firstTab = FirstTab(self.data)

        self.setWindowTitle("NAIDEA")
        self.setWindowIcon(QIcon("myicon.png"))
        self.showMaximized()

        #create filter object
        FilterLayout = QHBoxLayout()
        FilterLayout.addWidget(self.createHeader1a(), 2)#column width
        FilterLayout.addWidget(self.createHeader2a(), 2)

        #create tab widget object
        tabwidget = QTabWidget()
        tabwidget.addTab(self.firstTab, "Macro-Level")
        tabwidget.addTab(SecondTab(), "Farm-Level")
        tabwidget.addTab(ThirdTab(), "Help")

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addLayout(FilterLayout)
        vbox.addWidget(tabwidget)
        vbox.addWidget(buttonbox)

        self.setLayout(vbox)

    def createHeader1a(self): # function defining characteristics of each group/grid object
        HeaderBox = QGroupBox("Import Survey Data")

        inputfilebtn = QPushButton("Import")
        inputfilebtn.resize(150, 50)
        inputfilebtn.clicked.connect(self.on_pushButtonLoad_clicked)

        exportfilebtn = QPushButton("Export")
        exportfilebtn.setGeometry(200, 150, 100, 40)
        #import box layout

        #importrow1
        importrow1layout = QHBoxLayout()
        importrow1layout.addWidget(inputfilebtn)
        importrow1layout.addStretch()

        importrow2layout = QHBoxLayout()
        importrow2layout.addWidget(exportfilebtn)
        importrow2layout.addStretch()

        HeaderLayout = QGridLayout()
        HeaderLayout.addLayout(importrow1layout, 0, 1)
        HeaderLayout.addLayout(importrow2layout, 1, 1)
        HeaderBox.setLayout(HeaderLayout)
        HeaderBox.setFlat(True)

        return HeaderBox

    def createHeader2a(self): # function defining characteristics of each group/grid object
        HeaderBox = QGroupBox("Filters")
        HeaderBox.setFlat(True)
        return HeaderBox

    def getfile(self):
        option = QFileDialog.Options()
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "CSV files (*.csv)", options=option)
        # global data
        #data = csv.reader(open(fname[0], "r")) # tableview
        importedfile = pd.read_csv("C:/NAIDEADATA.csv")
        # for row in data:
        #     items = [
        #         QtGui.QStandardItem(field)
        #         for field in row
        #     ]
        #     self.model.appendRow(items)

        return pd.read_csv(fname[0])

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        importedfile = self.getfile()
        if importedfile is None:
            return
        self.firstTab.MRChart(importedfile)
        self.firstTab.BLChart(importedfile)
        self.firstTab.energychart(importedfile)

class FirstTab(QWidget):
    def __init__(self, data):
        super(FirstTab, self).__init__() #superclass to access methods of the base class
        self.data = data

        # The key to plotting information
        # self.model = QtGui.QStandardItemModel(self)
        # self.tableView = QtWidgets.QTableView(self)
        # self.tableView.setModel(self.model)
        # self.tableView.horizontalHeader().setStretchLastSection(True)

        # Grid layout of entire tab
        layout = QGridLayout()
        layout.addWidget(self.infrastructure(self.data), 3, 0)
        layout.addWidget(self.energy(), 3, 1)
        layout.addWidget(self.der(), 4, 0)
        layout.addWidget(self.info(self.data), 4, 1)
        layout.setRowStretch(3, 3)
        layout.setRowStretch(4, 3)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        self.setLayout(layout)

    def info(self, data):  # function defining characteristics of each group/grid object
        groupBox = QGroupBox("NAIDEA Information")
        label = QLabel(str(data))
        print(data)

        ExLayout = QGridLayout()
        ExLayout.addWidget(label)
        groupBox.setLayout(ExLayout)
        return groupBox

    def MRChart(self, importedfile): # pie
            radioButton = self.sender()
            fig = go.Pie(labels=importedfile[self.radioButton.label])
            layout = go.Layout(autosize=True, legend=dict(orientation="h",xanchor='center', x=0.5))
            fig = go.Figure(data=fig, layout=layout)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def infrastructure(self, importedfile):
        groupBox = QGroupBox("Infrastructure Breakdown")

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        right = QVBoxLayout()

        self.radioButton = QRadioButton("Low-Energy Lighting")
        self.radioButton.setChecked(True)
        self.radioButton.label = "low_energy_lighting"
        self.radioButton.toggled.connect(self.MRChart)
        right.addWidget(self.radioButton)

        self.radioButton = QRadioButton("Green Electricity")
        self.radioButton.label = "green-electricity"
        self.radioButton.toggled.connect(self.MRChart)
        right.addWidget(self.radioButton)

        self.radioButton = QRadioButton("Variable Speed Drive")
        self.radioButton.label = "VSD"
        self.radioButton.toggled.connect(self.MRChart)
        right.addWidget(self.radioButton)

        self.radioButton = QRadioButton("Plate Cooler")
        self.radioButton.label = "coolingsystem_platecooler"
        self.radioButton.toggled.connect(self.MRChart)
        right.addWidget(self.radioButton)

        # self.radioButton.setChecked(True)
        # self.radioButton1.toggled.connect(self.MRChart(self.data))

        # right.addWidget(self.radioButton1)
        # right.addWidget(self.radioButton2)
        # right.addWidget(self.radioButton3)
        # right.addWidget(self.radioButton4)

        middleright = QHBoxLayout()
        middleright.addWidget(self.browser)
        middleright.addLayout(right)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)

        return groupBox





    def energychart(self, importedfile):

        kwhdata = importedfile[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]]
        summed = kwhdata.sum(axis=0)
        fig = go.Pie(labels=summed.index, values=summed.values)
        layout = go.Layout(autosize=True, legend=dict(orientation="h",xanchor='center', x=0.5))# height = 600, width = 1000,
        fig = go.Figure(data=fig, layout=layout)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        self.browserEn.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def energy(self):
        groupBox = QGroupBox("Energy Breakdown")

        self.browserEn = QtWebEngineWidgets.QWebEngineView(self)
        exportfilebtn = QCheckBox("Export and do this")
        middleright = QHBoxLayout()
        middleright.addWidget(self.browserEn)
        middleright.addWidget(exportfilebtn)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)


        return groupBox

    def BLChart(self, importedfile):
        fig = go.Figure(data = [go.Bar(name='TotalKWh', x=importedfile["month"], y=importedfile["TotalKWh"]),
                                go.Bar(name='CoolingkWh', x=importedfile["month"], y=importedfile["CoolingKWh"]),
                                go.Bar(name='VacuumKWh', x=importedfile["month"], y=importedfile["VacuumKWh"]),
                                go.Bar(name='WaterHeatKWh', x=importedfile["month"], y=importedfile["WaterHeatKWh"]),
                                go.Bar(name='OtherKWh', x=importedfile["month"], y=importedfile["OtherKWh"])])
        fig.update_layout(barmode='stack',
                        legend=dict(orientation="h",xanchor='center', x=0.5))
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        self.browserBL.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def der(self): # box and whisker
        groupBox = QGroupBox("Dairy Energy Rating")

        self.browserBL = QtWebEngineWidgets.QWebEngineView(self)
        exportfilebtn = QCheckBox("Export and do this")
        middleright = QHBoxLayout()
        middleright.addWidget(self.browserBL)
        middleright.addWidget(exportfilebtn)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)

        return groupBox # box and whiskey

class SecondTab(QWidget):
    def __init__(self):
        super().__init__()

        selectgroup = QGroupBox("Select Operating Systems")  # group box for grouping widgets - Could make a grid using this
        combo = QComboBox() # list box
        list = ["Windows", "Mac", "Linux", "Fedora", "Kali"] # options
        combo.addItems(list)

        #layout for combo box
        selectLayout = QVBoxLayout()#organises widgets vertically
        selectLayout.addWidget(combo)
        selectgroup.setLayout(selectLayout) # adding/set the combo layout to select grou

        #layout for check boxes
        checkgroup = QGroupBox("whch OS do you like?") # Group box number 2
        windows = QCheckBox("Windows")
        mac = QCheckBox("Mac")
        Linux = QCheckBox("Linux")

        checkLayout = QVBoxLayout()#organises widgets vertically
        checkLayout.addWidget(windows)
        checkLayout.addWidget(mac)
        checkLayout.addWidget(Linux)
        checkgroup.setLayout(checkLayout)

        #Brings select and xheck boxes together
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(selectgroup) # adding/setting selectgroup to main lyout
        mainLayout.addWidget(checkgroup)
        self.setLayout(mainLayout)

class ThirdTab(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("Terms and Condition")
        listwidget = QListWidget()
        list = []

        for i in range(1, 20):
            list.append("This is Terms and Conditions")

        listwidget.insertItems(0, list)

        checkbox = QCheckBox("Agree the T&C's")

        #create layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(listwidget)
        layout.addWidget(checkbox)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tabwidget = TabWidget(data=None)
    tabwidget.show()
    app.exec()
