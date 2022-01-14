from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QHBoxLayout, QRadioButton, QGridLayout,QApplication, \
    QLabel, QListWidget, QGroupBox, QCheckBox, QComboBox,QDialog, QDialogButtonBox, QTabWidget, QWidget, QVBoxLayout, QButtonGroup, QTextEdit
import sys
from qtrangeslider import QLabeledRangeSlider
from qtrangeslider.qtcompat.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtWebEngineWidgets, QtGui, QtWidgets
import pandas as pd
import plotly.graph_objs as go
import csv
from os.path import abspath

class mainwindow(QDialog):
    def __init__(self, data):
        super(mainwindow, self).__init__()
        self.data = data
        self.filtereddatabase = []

        self.setWindowTitle("NAIDEA")
        self.setWindowIcon(QIcon('icon.png'))
        self.showMaximized()

        #create filter object
        FilterLayout = QHBoxLayout()
        FilterLayout.addWidget(self.createHeader1a(), 1)#import/export
        FilterLayout.addWidget(self.createHeader2a(), 4)# filters
        FilterLayout.addWidget(self.Header3(), 4)# images
        self.firstTab = FirstTab(self)

        #The key to plotting Treeview information
        #https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/

        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableView.setObjectName("tableView")

        #create tab widget object
        tabs = QTabWidget()
        tabs.addTab(self.firstTab, "Macro-Level")
        tabs.addTab(self.tableView, "Farm-Level")
        tabs.addTab(ThirdTab(), "Help")

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addLayout(FilterLayout)
        vbox.addWidget(tabs)
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
        rightmiddlelayout.addWidget(self.der_a)
        rightmiddlelayout.addWidget(self.der_b)
        rightmiddlelayout.addWidget(self.der_c)
        rightmiddlelayout.addWidget(self.der_d)
        rightmiddlelayout.addWidget(self.der_e)

        self.filterbutton = QPushButton("Filter")
        self.filterbutton.clicked.connect(self.on_filterButtonLoad_clicked)
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
        # fname = "C:/NAIDEADATA.csv"
        # database for treeview
        df1 = pd.read_csv(fname[0])
        df2 = df1[["farm_id", "milk_yield_litres", "TotalKWh", "CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]].groupby("farm_id",                                                                                                         as_index=False).sum().round()
        df3_size = df1[["farm_id", "herd_size", "milking_cows"]].groupby("farm_id").mean().round()
        df2 = pd.merge(left=df3_size, right=df2, left_on='farm_id', right_on='farm_id')
        df4 = df1[["farm_id", "re_thermal_m3", "re_solarpv_kw", "re_wind_kw", "res_capacity_kw", "low_energy_lighting",
                       "night_rate_electricity", "heat_recovery", "green_electricity", "num_parlour_units", "milking_frequency",
                       "milking_duration_hours", "hotwash_freq", "milkpump_type", "vacuumpump_power_kw", "VSD", "bulktank_capacity_litres",
                       "waterheating_power_elec_kw", "waterheating_power_gas_kw", "waterheating_power_oil_kw", "hotwatertank_capacity_litres",
                       "coolingsystem_directexpansion", "coolingsystem_platecooler", "coolingsystem_icebank", "coolingsystem_waterchillingunit"]].drop_duplicates(subset='farm_id', keep="first")
        df2 = pd.merge(left=df2, right=df4, left_on='farm_id', right_on='farm_id')
        self.tvdatabase = df2
        self.model = PandasModel(df2)
        self.tableView.setModel(self.model)

        if fname:
            return df1

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

    @QtCore.pyqtSlot()
    def on_filterButtonLoad_clicked(self):
        current_tv = self.tvdatabase
        current_charts = self.importedfile

        #farm size
        minsize = self.slider1.value()[0]
        maxsize = self.slider1.value()[1]

        #VSD
        if self.VSD_yes.isChecked():
            current_tv = current_tv.loc[(current_tv['VSD'] == "yes")]
        elif self.VSD_no.isChecked():
            current_tv = current_tv.loc[(current_tv['VSD'] == "no")]

        # #PHE
        if self.PHE_yes.isChecked():
            current_tv = current_tv.loc[(current_tv['coolingsystem_platecooler'] == "yes")]
        elif self.PHE_no.isChecked():
            current_tv = current_tv.loc[(current_tv['coolingsystem_platecooler'] == "no")]

        # #Cooling System
        # if self.cs_DX.isChecked():
        #     current_tv = current_tv.loc[(current_tv['coolingsystem_directexpansion'] >= 'yes')]
        # elif self.cs_IB.isChecked():
        #     current_tv = current_tv.loc[(current_tv['coolingsystem_icebank'] >= 'yes')]

        #filter treeview database based on slider chart values
        current_tv = current_tv.loc[(current_tv['herd_size'] >= minsize) & (current_tv['herd_size'] <= maxsize)]
        current_charts = current_charts.loc[current_charts['farm_id'].isin(current_tv["farm_id"])]


        if current_tv is None:
            return

        if current_charts is None:
            return

        self.firstTab.MRChart(current_charts)
        self.firstTab.BLChart(current_charts)
        self.firstTab.energychart(current_charts)
        self.model = PandasModel(current_tv)
        self.tableView.setModel(self.model)

        self.filtereddatabase = current_tv




class FirstTab(QWidget):
    def __init__(self, tabwidget):
        super(FirstTab, self).__init__()
        self.tabwidget = tabwidget
        self.data = tabwidget.data
        self.filtereddatabase = []


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

    def infrastructure(self, importedfile):
        groupBox = QGroupBox("Infrastructure Breakdown")

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        right = QVBoxLayout()

        self.radioButton1 = QRadioButton("Low-Energy Lighting")
        self.radioButton1.label = "low_energy_lighting"
        try:
            self.radioButton1.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase))
        except:
            self.radioButton1.toggled.connect(lambda: self.MRChart(self.tabwidget.importedfile))

        right.addWidget(self.radioButton1)

        self.radioButton2 = QRadioButton("Green Electricity")
        self.radioButton2.setChecked(True)
        self.radioButton2.label = "green_electricity"
        try:
            self.radioButton2.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase))
        except:
            self.radioButton2.toggled.connect(lambda: self.MRChart(self.tabwidget.importedfile))

        right.addWidget(self.radioButton2)

        self.radioButton3 = QRadioButton("Variable Speed Drive")
        self.radioButton3.label = "VSD"
        try:
            self.radioButton3.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase))
        except:
            self.radioButton3.toggled.connect(lambda: self.MRChart(self.tabwidget.importedfile))
        right.addWidget(self.radioButton3)

        self.radioButton4 = QRadioButton("Plate Cooler")
        self.radioButton4.label = "coolingsystem_platecooler"
        try:
            self.radioButton4.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase))
        except:
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

class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    window = mainwindow(data=None)
    window.show()
    app.exec()