from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QHBoxLayout, QRadioButton, QGridLayout,QApplication, \
    QLabel, QListWidget, QGroupBox, QCheckBox, QComboBox,QDialog, QDialogButtonBox, QTabWidget, QWidget, QVBoxLayout, QButtonGroup, QTextEdit
import sys
from qtrangeslider import QLabeledRangeSlider
from qtrangeslider.qtcompat.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5 import QtCore, QtWebEngineWidgets
import pandas as pd
import plotly.graph_objs as go
from os.path import abspath

class TabWidget(QDialog):
    def __init__(self, data):
        super(TabWidget, self).__init__()
        self.data = data

        self.setWindowTitle("NAIDEA")
        self.setWindowIcon(QIcon('icon.png'))
        self.showMaximized()

        #create filter object
        FilterLayout = QHBoxLayout()
        FilterLayout.addWidget(self.createHeader1a(), 1)#import/export
        FilterLayout.addWidget(self.createHeader2a(), 4)# filters
        FilterLayout.addWidget(self.Header3(), 4)# images
        self.firstTab = FirstTab(self)

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
        HeaderBox = QGroupBox("Import/Export Data")

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

        QSS = """
        QSlider {
            min-height: 10px;
        }
        
        QSlider::groove:horizontal {
            border: 0px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #888, stop:1 #ddd);
            height: 10px;
            border-radius: 5px;
        }
        QSlider::handle {
            background: qradialgradient(cx:0, cy:0, radius: 1.2, fx:0.35,
                                        fy:0.3, stop:0 #eef, stop:1 #002);
            height: 10px;
            width: 10px;
            border-radius: 5px;
        }
        QSlider::sub-page:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #227, stop:1 #77a);
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        }
        QRangeSlider {
            qproperty-barColor: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #227, stop:1 #77a);
        }
        """

        HeaderBox = QGroupBox("Filter Data")
        leftlayout = QGridLayout()

        self.radiogroup1 = QButtonGroup()
        self.radiogroup2 = QButtonGroup()
        self.radiogroup3 = QButtonGroup()

        label1 = QLabel(self)
        label1.setText("Variable Speed Drive:")
        label1.setAlignment(Qt.AlignTop)
        leftlayout.addWidget(label1, 0, 0)
        self.VSD_yes = QRadioButton("Yes")
        self.VSD_no = QRadioButton("No")
        self.VSD_all = QRadioButton("All")
        self.VSD_all.setChecked(True)
        self.radiogroup1.addButton(self.VSD_yes)
        self.radiogroup1.addButton(self.VSD_no)
        self.radiogroup1.addButton(self.VSD_all)
        leftlayout.addWidget(self.VSD_yes, 0, 1)
        leftlayout.addWidget(self.VSD_no, 0, 2)
        leftlayout.addWidget(self.VSD_all, 0, 3)


        label2 = QLabel(self)
        label2.setText("Plate Cooler:")
        label2.setAlignment(Qt.AlignTop)
        leftlayout.addWidget(label2, 1, 0)
        self.PHE_yes = QRadioButton("Yes")
        self.PHE_no = QRadioButton("No")
        self.PHE_all = QRadioButton("All")
        self.PHE_all.setChecked(True)
        self.radiogroup2.addButton(self.PHE_yes)
        self.radiogroup2.addButton(self.PHE_no)
        self.radiogroup2.addButton(self.PHE_all)
        leftlayout.addWidget(self.PHE_yes, 1, 1)
        leftlayout.addWidget(self.PHE_no, 1, 2)
        leftlayout.addWidget(self.PHE_all, 1, 3)

        label3 = QLabel(self)
        label3.setText("Cooling System:")
        label3.setAlignment(Qt.AlignTop)
        leftlayout.addWidget(label3, 2, 0)
        self.cs_DX = QRadioButton("DX")
        self.cs_IB = QRadioButton("IB")
        self.cs_all = QRadioButton("All")
        self.cs_all.setChecked(True)
        self.radiogroup3.addButton(self.cs_DX)
        self.radiogroup3.addButton(self.cs_IB)
        self.radiogroup3.addButton(self.cs_all)
        leftlayout.addWidget(self.cs_DX, 2, 1)
        leftlayout.addWidget(self.cs_IB, 2, 2)
        leftlayout.addWidget(self.cs_all, 2, 3)
        leftlayout.setRowStretch(leftlayout.rowCount(), 1)

        righttoplayout = QHBoxLayout()
        rightmiddlelayout = QHBoxLayout()
        rightbottomlayout = QHBoxLayout()
        # range slider bars for farm size
        #https://pythonrepo.com/repo/tlambert03-QtRangeSlider-python-graphical-user-interface-applications
        #https://doc.qt.io/qt-5/qslider.html
        label4 = QLabel(self)
        label4.setText("Farm Size\n(No. Cows):")
        label4.setAlignment(Qt.AlignLeft)
        righttoplayout.addWidget(label4)
        self.slider1 = QLabeledRangeSlider(Qt.Horizontal)
        self.slider1.setSingleStep(step=25)
        self.slider1.setEdgeLabelMode(opt=0)
        self.slider1.setHandleLabelPosition(opt=2)
        self.slider1.setRange(5, 500)
        self.slider1.setTickInterval(25)
        self.slider1.setValue((5, 500))
        self.slider1.setStyleSheet(QSS)
        righttoplayout.addWidget(self.slider1)


        label5 = QLabel(self)
        label5.setAlignment(Qt.AlignLeft)
        label5.setText("Dairy Energy\nRating (DER):")
        rightmiddlelayout.addWidget(label5)
        self.der_a = QCheckBox("A")
        self.der_b = QCheckBox("B")
        self.der_c = QCheckBox("C")
        self.der_d = QCheckBox("D")
        self.der_e = QCheckBox("E")
        self.der_a.setChecked(True)
        self.der_b.setChecked(True)
        self.der_c.setChecked(True)
        self.der_d.setChecked(True)
        self.der_e.setChecked(True)
        self.filterbutton = QPushButton("Filter")
        rightmiddlelayout.addWidget(self.der_a)
        rightmiddlelayout.addWidget(self.der_b)
        rightmiddlelayout.addWidget(self.der_c)
        rightmiddlelayout.addWidget(self.der_d)
        rightmiddlelayout.addWidget(self.der_e)
        rightmiddlelayout.addWidget(self.filterbutton)

        rightlayout = QVBoxLayout()
        rightlayout.addLayout(righttoplayout)
        rightlayout.addStretch(1)
        rightlayout.addLayout(rightmiddlelayout)
        rightlayout.addStretch(1)
        rightlayout.addLayout(rightbottomlayout)

        layout = QHBoxLayout()
        layout.addLayout(leftlayout)
        layout.addLayout(rightlayout)
        HeaderBox.setLayout(layout)
        HeaderBox.setFlat(True)#

        return HeaderBox

    def Header3(self): # function defining characteristics of each group/grid object
        HeaderBox = QGroupBox("A Collaboration of:")

        # im = QPixmap("icon.png")
        # label = QLabel()
        # label.setPixmap(im)
        # # label = im.scaled(64, 64)
        # grid = QGridLayout()
        # grid.addWidget(label, 1, 1)
        # HeaderBox.setLayout(grid)

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

        if fname:
            return pd.read_csv(fname[0])

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        importedfile = self.getfile()
        if importedfile is None:
            return
        self.firstTab.MRChart(importedfile)
        self.firstTab.BLChart(importedfile)
        self.firstTab.energychart(importedfile)
        self.importedfile = importedfile

    def printgetslider1(self):

        return self.slider1.value()

class FirstTab(QWidget):
    def __init__(self, tabwidget):
        super(FirstTab, self).__init__() #superclass to access methods of the base class
        self.tabwidget = tabwidget
        self.data = tabwidget.data

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
        label = QTextEdit()
        label.setFrameStyle(0)
        label.setReadOnly(True)
        label.textCursor().insertHtml("The National Artificial Intelligent Dairy Energy Application (NAIDEA) was developed and is maintained by researchers in the MeSSO research group at the Munster Technological University (messo.mtu.ie). NAIDEA is not for use by commercial bodies. Contact messo@mtu.ie for further information.")

        ExLayout = QVBoxLayout()
        ExLayout.addWidget(label)
        groupBox.setLayout(ExLayout)
        groupBox.setFlat(True)
        return groupBox

    def MRChart(self, importedfile): # pie
        # https://pythonbasics.org/pyqt-radiobutton/
        if self.radioButton1.isChecked():
            importedfile = importedfile[["farm_id", self.radioButton1.label]].drop_duplicates()
            fig = go.Pie(labels=importedfile[self.radioButton1.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>")
        elif self.radioButton2.isChecked():
            importedfile = importedfile[["farm_id", self.radioButton2.label]].drop_duplicates()
            fig = go.Pie(labels=importedfile[self.radioButton2.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>")
        elif self.radioButton3.isChecked():
            importedfile = importedfile[["farm_id", self.radioButton3.label]].drop_duplicates()
            fig = go.Pie(labels=importedfile[self.radioButton3.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>")
        elif self.radioButton4.isChecked():
            importedfile = importedfile[["farm_id", self.radioButton4.label]].drop_duplicates()
            fig = go.Pie(labels=importedfile[self.radioButton4.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>")

        layout = go.Layout(autosize=True, legend=dict(orientation="h",xanchor='center', x=0.5))
        fig = go.Figure(data=fig, layout=layout)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        print(self.tabwidget.printgetslider1())

    def infrastructure(self, importedfile):
        groupBox = QGroupBox("Infrastructure Breakdown")

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        right = QVBoxLayout()

        self.radioButton1 = QRadioButton("Low-Energy Lighting")
        self.radioButton1.label = "low_energy_lighting"
        self.radioButton1.toggled.connect(lambda: self.MRChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton1)

        self.radioButton2 = QRadioButton("Green Electricity")
        self.radioButton2.setChecked(True)
        self.radioButton2.label = "green_electricity"
        self.radioButton2.toggled.connect(lambda: self.MRChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton2)

        self.radioButton3 = QRadioButton("Variable Speed Drive")
        self.radioButton3.label = "VSD"
        self.radioButton3.toggled.connect(lambda: self.MRChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton3)

        self.radioButton4 = QRadioButton("Plate Cooler")
        self.radioButton4.label = "coolingsystem_platecooler"
        self.radioButton4.toggled.connect(lambda: self.MRChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton4)


        middleright = QHBoxLayout()
        middleright.addWidget(self.browser)
        middleright.addLayout(right)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)


        return groupBox

    def energychart(self, importedfile):
        kwhdata = importedfile[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]]
        if self.radioButton5.isChecked():
            kwhdata = importedfile[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]]
            summed = round(kwhdata.sum(axis=0))
            fig = go.Pie(labels=["Milk Cooling", "Milk Harvesting", "Water Heating", "Other Use"], values=summed.values,  hovertemplate = "%{label}: <br>Sum: %{value} kWh <extra></extra>")
        elif self.radioButton6.isChecked():
            summed = round(kwhdata.sum(axis=0))
            fig = go.Pie(labels=["Milk Cooling", "Milk Harvesting", "Water Heating", "Other Use"], values=summed.values,  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>")
        elif self.radioButton7.isChecked():
            summed = round(kwhdata.sum(axis=0)*0.324)
            fig = go.Pie(labels=["Milk Cooling", "Milk Harvesting", "Water Heating", "Other Use"], values=summed.values,  hovertemplate = "%{label}: <br>Sum: %{value} gCO2 <extra></extra>")

        layout = go.Layout(autosize=True, legend=dict(orientation="h",xanchor='center', x=0.5))
        fig = go.Figure(data=fig, layout=layout)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        self.browserEn.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def energy(self):
        groupBox = QGroupBox("Energy/Carbon Breakdown")

        right = QVBoxLayout()

        self.radioButton5 = QRadioButton("Energy Breakdown")
        self.radioButton5.label = "low_energy_lighting"
        self.radioButton5.toggled.connect(lambda: self.energychart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton5)

        self.radioButton6 = QRadioButton("Dairy Energy Rating")
        self.radioButton6.setChecked(True)
        self.radioButton6.label = "green_electricity"
        self.radioButton6.toggled.connect(lambda: self.energychart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton6)

        self.radioButton7 = QRadioButton("Carbon Dioxide")
        self.radioButton7.label = "VSD"
        self.radioButton7.toggled.connect(lambda: self.energychart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton7)

        self.browserEn = QtWebEngineWidgets.QWebEngineView(self)
        middleright = QHBoxLayout()
        middleright.addWidget(self.browserEn)
        middleright.addLayout(right)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)


        return groupBox

    def BLChart(self, importedfile):

        smonth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        if self.radioButton8.isChecked():# total
            kwhdata = importedfile[["month", "CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]].groupby("month",
                                                                                                             as_index=False).sum()
            y_axislabel = "Electricity Use\n(kWh)"
            hovertext = "%{x}: <br>%{y} kWh <extra></extra>"
            fig = go.Figure(data=[go.Bar(name='Milk Cooling', x=smonth, y=round(kwhdata["CoolingKWh"], 1)),
                                  go.Bar(name='Milk Harvesting', x=smonth, y=round(kwhdata["VacuumKWh"], 1)),
                                  go.Bar(name='Water Heating', x=smonth, y=round(kwhdata["WaterHeatKWh"], 1)),
                                  go.Bar(name='Other Use', x=smonth, y=round(kwhdata["OtherKWh"], 1))])
                            # hovertemplate="%{x}: <br>%{y} kWh <extra></extra>")


        elif self.radioButton9.isChecked(): # total / litre milk
            kwhdata_perlitre = importedfile[["month", "milk_yield_litres", "CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]].groupby("month", as_index = False).sum()
            month_vector = kwhdata_perlitre["month"]
            kwhdata_perlitre = kwhdata_perlitre[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]].div(
                kwhdata_perlitre.milk_yield_litres, axis=0)
            kwhdata_perlitre = kwhdata_perlitre*1000
            kwhdata_perlitre.insert(loc=0, column="month", value=month_vector)
            kwhdata = kwhdata_perlitre
            y_axislabel = "Electricity Use\n(Wh/Litre)"
            hovertext = "%{label}: <br>%{value} Wh/Litre <extra></extra>"
            fig = go.Figure(data=[go.Bar(name='Milk Cooling', x=smonth, y=round(kwhdata["CoolingKWh"], 1)),
                                  go.Bar(name='Milk Harvesting', x=smonth, y=round(kwhdata["VacuumKWh"], 1)),
                                  go.Bar(name='Water Heating', x=smonth, y=round(kwhdata["WaterHeatKWh"], 1)),
                                  go.Bar(name='Other Use', x=smonth, y=round(kwhdata["OtherKWh"], 1))])
                            # hovertemplate="%{label}: <br>%{value} Wh/Litre <extra></extra>")


        elif self.radioButton10.isChecked(): # total / cow
            kwhdata_percow = importedfile[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]].div(importedfile.herd_size, axis=0)
            kwhdata_percow.insert(loc=0, column="month", value=importedfile['month'])
            kwhdata = kwhdata_percow.groupby("month", as_index=False).mean()
            y_axislabel = "Electricity Use\n(kWh/cow)"
            hovertext = "%{label}: <br>%{value} kWh/Cow <extra></extra>"
            fig = go.Figure(data=[go.Bar(name='Milk Cooling', x=smonth, y=round(kwhdata["CoolingKWh"], 1)),
                                  go.Bar(name='Milk Harvesting', x=smonth, y=round(kwhdata["VacuumKWh"], 1)),
                                  go.Bar(name='Water Heating', x=smonth, y=round(kwhdata["WaterHeatKWh"], 1)),
                                  go.Bar(name='Other Use', x=smonth, y=round(kwhdata["OtherKWh"], 1))])
                            # hovertemplate="%{label}: <br>%{value} kWh/Cow <extra></extra>")

        fig.update_traces(hovertemplate=hovertext)
        fig.update_layout(barmode='stack',
                        legend=dict(orientation="h", xanchor='center', x=0.5), margin=dict(t=0, b=0, l=0, r=0))

        fig.update_yaxes(title=y_axislabel, title_font_size=10)
        self.browserBL.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def der(self): # box and whisker
        groupBox = QGroupBox("Monthly Energy Statistics")

        right = QVBoxLayout()

        self.radioButton8 = QRadioButton("Electricity Use")
        self.radioButton8.toggled.connect(lambda: self.BLChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton8)

        self.radioButton9 = QRadioButton("Electricity Use / Litre")
        self.radioButton9.setChecked(True)
        self.radioButton9.toggled.connect(lambda: self.BLChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton9)

        self.radioButton10 = QRadioButton("Electricity Use / Cow")
        self.radioButton10.toggled.connect(lambda: self.BLChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton10)

        self.browserBL = QtWebEngineWidgets.QWebEngineView(self)
        middleright = QHBoxLayout()
        middleright.addWidget(self.browserBL)
        middleright.addLayout(right)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)

        return groupBox

class SecondTab(QWidget):
    def __init__(self):
        super().__init__()

        # The key to plotting information
        # self.model = QtGui.QStandardItemModel(self)
        # self.tableView = QtWidgets.QTableView(self)
        # self.tableView.setModel(self.model)
        # self.tableView.horizontalHeader().setStretchLastSection(True)

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
    app.setStyle('Breeze')
    tabwidget = TabWidget(data=None)
    tabwidget.show()
    app.exec()