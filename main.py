from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QFileDialog, QPushButton, QHBoxLayout, QRadioButton, QGridLayout,QApplication, \
    QLabel, QListWidget, QGroupBox, QCheckBox, QComboBox,QDialog, QDialogButtonBox, QTabWidget, QWidget, QVBoxLayout, QButtonGroup, QTextEdit
import sys
from qtrangeslider import QLabeledRangeSlider
from qtrangeslider.qtcompat.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QStandardItem, QFont
from PyQt5 import QtCore, QtWebEngineWidgets, QtGui, QtWidgets
import pandas as pd
import plotly.graph_objs as go
import numpy as np

class mainwindow(QDialog):
    def __init__(self, data):
        super(mainwindow, self).__init__()
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

        #The key to plotting Treeview information
        #https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/

        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableView.setObjectName("tableView")

        # KPI Tableview


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
        # fname = "C:/NAIDEADATA2.csv"
        # database for treeview
        df1 = pd.read_csv(fname[0])
        total_db, cooling_db, vacuum_db, heating_db, combined_db = self.processimportedfile(df1)
        wandb_total = pd.read_csv('wandbtotalkwh.csv')
        df1["TotalKWh"] = pd.DataFrame([self.predict_total(data=total_db.iloc[i, 1:total_db.shape[1]], wandb=wandb_total) for i in range(len(total_db))], columns=['TotalKWh'])
        wandb_cooling = pd.read_csv('wandbcoolingkwh.csv')
        df1["CoolingKWh"] = pd.DataFrame([self.predict_cooling(data=cooling_db.iloc[i, 1:cooling_db.shape[1]], wandb=wandb_cooling) for i in range(len(cooling_db))], columns=['CoolingKWh'])
        wandb_vacuum = pd.read_csv('wandbvacuumkwh.csv')
        df1["VacuumKWh"] = pd.DataFrame([self.predict_vacuum(data=vacuum_db.iloc[i, 1:vacuum_db.shape[1]], wandb=wandb_vacuum) for i in range(len(vacuum_db))], columns=['VacuumKWh'])
        wandb_heating = pd.read_csv('wandbwaterheatkwh.csv')
        df1["WaterHeatKWh"] = pd.DataFrame([self.predict_heating(data=heating_db.iloc[i, 1:heating_db.shape[1]], wandb=wandb_heating) for i in range(len(heating_db))], columns=['WaterHeatKWh'])
        wandb_combined = pd.read_csv('wandbcombinedkwh.csv')
        df1["CombinedKWh"] = pd.DataFrame([self.predict_combined(data=combined_db.iloc[i, 1:combined_db.shape[1]], wandb=wandb_combined) for i in range(len(combined_db))], columns=['CombinedKWh'])
        # df1["WaterHeatKWh"] = df1["CombinedKWh"] - df1["CoolingKWh"] - df1["VacuumKWh"]
        # Manual processing
        df1['CoolingKWh'].values[df1['milk_yield_litres'] == 0] = 0
        df1['VacuumKWh'].values[df1['milk_yield_litres'] == 0] = 0
        df1['WaterHeatKWh'].values[df1['waterheating_power_elec_kw'] == 0] = 0
        # Adjust cooling, vacuum and WH based on their % of combined prediction
        CVW = df1['CoolingKWh']+df1['VacuumKWh']+df1['WaterHeatKWh']
        df1['CoolingKWh'] = df1['CombinedKWh']*(sum(df1['CoolingKWh'])/sum(CVW))
        df1['VacuumKWh'] = df1['CombinedKWh']*(sum(df1['VacuumKWh'])/sum(CVW))
        df1['WaterHeatKWh'] = df1['CombinedKWh']*(sum(df1['WaterHeatKWh'])/sum(CVW))
        df1["OtherKWh"] = df1["TotalKWh"] - df1["CombinedKWh"] #- df1["CoolingKWh"] - df1["VacuumKWh"]
        df1.to_csv('predict_df.csv')
        # "CoolingKWh", "VacuumKWh", "WaterHeatKWh", "CombinedKWh", "OtherKWh"
        df2 = df1[["farm_id", "milk_yield_litres", "TotalKWh"]].groupby("farm_id", as_index=False).sum().round()
        df2["wh_lm"] = df2["TotalKWh"]/ df2["milk_yield_litres"] * 1000
        self.bins = [0, 23,	36,	49,	62,	1000]
        df2["DER"] = pd.DataFrame(np.digitize(df2["wh_lm"], self.bins), columns=["DER"])
        df2['DER'] = df2['DER'].astype(str)
        df2['DER'] = df2['DER'].replace(str(1), 'A')
        df2['DER'] = df2['DER'].replace(str(2), 'B')
        df2['DER'] = df2['DER'].replace(str(3), 'C')
        df2['DER'] = df2['DER'].replace(str(4), 'D')
        df2['DER'] = df2['DER'].replace(str(5), 'E')
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
        self.on_filterButtonLoad_clicked()

    def printgetslider1(self):

        return self.slider1.value()

    def processimportedfile(self, data):
        # fname = "C:/NAIDEADATA2.csv"
        # df1 = pd.read_csv(fname)
        data_mdl = data[["farm_id", "month", "milk_yield_litres", "herd_size", "milking_cows",
                     "re_thermal_m3", "num_parlour_units", "milking_frequency", "hotwash_freq",
                     "milkpump_type", "vacuumpump_power_kw", "VSD", "bulktank_capacity_litres",
                     "waterheating_power_elec_kw", "waterheating_power_gas_kw", "waterheating_power_oil_kw",
                     "hotwatertank_capacity_litres","coolingsystem_directexpansion", "coolingsystem_platecooler",
                     "coolingsystem_icebank", "coolingsystem_waterchillingunit"]]
        data_mdl['re_thermal_m3'].values[data_mdl['re_thermal_m3'] > 0] = 2
        data_mdl['re_thermal_m3'].values[data_mdl['re_thermal_m3'] == 0] = 1
        data_mdl = data_mdl.rename(columns={"month": "Month", "milk_yield_litres": "MilkYield", "herd_size": "DairyCows_Total",
                                            "milking_cows": "DairyCows_Milking", "re_thermal_m3": "Parlour_SolarThermalY_N",
                                            "num_parlour_units": "NoOfParlourUnits", "waterheating_power_elec_kw": "TotalWaterHeaterPower",
                                            "hotwatertank_capacity_litres": "TotalWaterHeaterVolume", "bulktank_capacity_litres": "TotalBulkTankVolume",
                                            "vacuumpump_power_kw": "TotalVacuumPower"})
        hzhw = pd.get_dummies(data_mdl['hotwash_freq'])+1
        hzhw = hzhw.rename(columns={"once a day": "OAD", "once a month": "OAM", "once a week": "OAW",
                                    "once every two days": "E2ndD"})
        milkpump = pd.get_dummies(data_mdl['milkpump_type'])+1
        # milkpump.columns = milkpump.columns.str.lower()
        PHE = pd.get_dummies(data_mdl['coolingsystem_platecooler'])+1 #yes ==2
        PHE = PHE.rename(columns={"yes": "GWPHE"})
        DXIB = pd.get_dummies(data_mdl['coolingsystem_directexpansion']) + 1  # DX=1
        DXIB = DXIB.rename(columns={"no": "IBDX"})
        ICWPHE = pd.get_dummies(data_mdl['coolingsystem_waterchillingunit']) + 1  # yes ==2
        ICWPHE = ICWPHE.rename(columns={"yes": "ICWPHE"})
        VSD = pd.get_dummies(data_mdl['VSD']) + 1  # yes ==2
        VSD = VSD.rename(columns={"yes": "Parlour_VacuumPump1_VariableSpeedY_N"})
        data_mdl = data_mdl.drop(columns=["VSD"])
        # WH Fuel source
        WH = data_mdl[["TotalWaterHeaterPower", "waterheating_power_gas_kw", "waterheating_power_oil_kw"]]
        WH['TotalWaterHeaterPower'].values[WH['TotalWaterHeaterPower'] > 0] = 1
        gasoroil = WH["waterheating_power_gas_kw"] + WH["waterheating_power_oil_kw"]
        gasoroil.values[gasoroil > 0] = 1
        electric = WH['TotalWaterHeaterPower']
        electricplus = gasoroil + electric
        ElectricAndOil = electricplus.to_frame(name = "ElectricAndOil")
        Electric = electric + 1
        Electric.values[electricplus == 2] = 1
        Electric = pd.DataFrame(Electric.values, columns = ["Electric"])
        # Dwelling
        Dwelling = np.ones((len(ElectricAndOil), 1), dtype=int)
        Dwelling = pd.DataFrame(Dwelling, columns = ["Dwelling"])
        # Milking
        Milking = np.ones((len(ElectricAndOil), 1), dtype=int)
        Milking = pd.DataFrame(Milking, columns = ["Milking"])
        Milking['Milking'].values[data_mdl['MilkYield'] == 0] = 2

        # Form datasets for TCVH
        df = pd.concat([data_mdl, hzhw[['OAD', "OAM", "OAW", "E2ndD"]],
                        milkpump[['Diaphram','High Speed','Double Diaphram','Single Speed', 'VSD']],
                        PHE['GWPHE'], DXIB['IBDX'], ICWPHE['ICWPHE'], VSD['Parlour_VacuumPump1_VariableSpeedY_N'],
                        ElectricAndOil["ElectricAndOil"], Electric["Electric"], Dwelling["Dwelling"], Milking["Milking"]], axis=1)
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(' ', '')

        # Create datasets for each DV, with required vars in correct order.
        total_vars = ['farm_id', 'month', 'dairycows_milking', 'dairycows_total', 'milkyield','ibdx', 'gwphe', 'icwphe', 'totalbulktankvolume', 'parlour_vacuumpump1_variablespeedy_n', 'oad', 'oam', 'oaw', 'parlour_solarthermaly_n', 'totalwaterheatervolume','totalwaterheaterpower', 'electricandoil', 'diaphram', 'doublediaphram','highspeed','vsd','dwelling','milking']
        total_vars = [each.lower() for each in total_vars]
        total_db = df[total_vars]
        total_db = total_db.fillna(total_db.mean().round())

        cooling_vars = ['farm_id', 'Month',	'DairyCows_Total',	'MilkYield',	'NoOfParlourUnits',	'IBDX',	'GWPHE',	'ICWPHE',	'TotalBulkTankVolume']
        cooling_vars = [each.lower() for each in cooling_vars]
        cooling_db = df[cooling_vars]
        cooling_db = cooling_db.fillna(cooling_db.mean().round())

        vacuum_vars = ['farm_id', 'Month', 'DairyCows_Total',	'MilkYield',	'NoOfParlourUnits',	'TotalVacuumPower',	'Parlour_VacuumPump1_VariableSpeedY_N']
        vacuum_vars = [each.lower() for each in vacuum_vars]
        vacuum_db = df[vacuum_vars]
        vacuum_db = vacuum_db.fillna(vacuum_db.mean().round())

        heating_vars = ['farm_id', 'Month', 'DairyCows_Milking',	'DairyCows_Total',	'MilkYield',	'E2ndD',	'OAD',	'OAM',	'OAW',	'Parlour_SolarThermalY_N',	'TotalWaterHeaterVolume',	'TotalWaterHeaterPower',	'Electric',	'ElectricAndOil']
        heating_vars = [each.lower() for each in heating_vars]
        heating_db = df[heating_vars]
        heating_db = heating_db.fillna(heating_db.mean().round())

        combined_vars = ['farm_id', 'Month', 'DairyCows_Milking', 'DairyCows_Total', 'MilkYield', 'NoOfParlourUnits', 'IBDX', 'GWPHE', 'ICWPHE', 'TotalBulkTankVolume', 'TotalVacuumPower', 'Parlour_VacuumPump1_VariableSpeedY_N', 'E2ndD', 'OAD', 'OAM', 'OAW', 'Parlour_SolarThermalY_N', 'TotalWaterHeaterVolume', 'TotalWaterHeaterPower', 'Electric',	'ElectricAndOil']
        combined_vars = [each.lower() for each in combined_vars]
        combined_db = df[combined_vars]
        combined_db = combined_db.fillna(combined_db.mean().round())

        return total_db, cooling_db, vacuum_db, heating_db, combined_db

    def predict_total(self, data, wandb):
        # data = total_db.iloc[0, 1:23]
        # wandb = pd.read_csv('wandbtotal.csv')
        data["dairycows_milking"] = np.sqrt(data["dairycows_milking"])
        data["dairycows_total"] = np.log(data["dairycows_total"])
        data["milkyield"] = np.sqrt(data["milkyield"])
        data["totalbulktankvolume"] = np.log(data["totalbulktankvolume"])
        data["totalwaterheatervolume"] = np.reciprocal(data["totalwaterheatervolume"])
        data["totalwaterheaterpower"] = np.sqrt(data["totalwaterheaterpower"])
        minmax = wandb.iloc[wandb.shape[0]-2:wandb.shape[0], 1:wandb.shape[1]-3]
        data_std = pd.DataFrame(2 * np.subtract(data, minmax.iloc[0].values.tolist()) / np.subtract(minmax.iloc[1].values.tolist(), minmax.iloc[0].values.tolist()) -1)
        # wandbtotal = pd.to_pickle(wandb, 'wandbtotal.pkl')
        # wandbtotal = pd.read_pickle('wandbtotal.pkl')

        # https://stackoverflow.com/questions/45830206/pyinstaller-created-exe-file-can-not-load-a-keras-nn-model
        weights = wandb.iloc[0:wandb.shape[0]-2, 1:wandb.shape[1]-3]
        innerbias = wandb["Bias"][0:wandb.shape[0]-2]
        outerlayerbias = wandb["Outputlayerweights"][0:wandb.shape[0]-2]
        outerbias = wandb["Outputbias"][0]
        minkWh = wandb["Bias"].iloc[-2]
        maxkWh = wandb["Bias"].iloc[-1]
        # print(maxkWh)

        # explode input data
        input_trans_minmax = pd.DataFrame(data_std)
        input_trans_minmax = input_trans_minmax.transpose()
        input_trans_minmax = input_trans_minmax.append([input_trans_minmax] * (weights.shape[0] - 1), ignore_index=True)

        inputxweights = np.multiply(weights.to_numpy(), input_trans_minmax)
        hiddensum = inputxweights.sum(axis=1)
        transfcnplusbias = np.tanh(hiddensum + innerbias)
        TFBplusbias = transfcnplusbias * outerlayerbias
        outerlayersum = sum(TFBplusbias)
        outerlayersumTF = np.tanh(outerlayersum + outerbias)

        predictionvalue = (((outerlayersumTF + 1) * (maxkWh - minkWh)) / 2) + minkWh
        return predictionvalue

    def predict_cooling(self, data, wandb):
        # data = cooling_db.iloc[0, 1:9]
        # wandb = pd.read_csv('wandbcooling.csv')
        data["dairycows_total"] = np.log(data["dairycows_total"])
        data["milkyield"] = np.cbrt(data["milkyield"])
        data["totalbulktankvolume"] = np.log(data["totalbulktankvolume"])
        data["noofparlourunits"] = np.log(data["noofparlourunits"])
        minmax = wandb.iloc[wandb.shape[0]-2:wandb.shape[0], 1:wandb.shape[1]-3]
        data_std = pd.DataFrame(2 * np.subtract(data, minmax.iloc[0].values.tolist()) / np.subtract(minmax.iloc[1].values.tolist(), minmax.iloc[0].values.tolist()) -1)
        # wandbtotal = pd.to_pickle(wandb, 'wandbtotal.pkl')
        # wandbtotal = pd.read_pickle('wandbtotal.pkl')

        # https://stackoverflow.com/questions/45830206/pyinstaller-created-exe-file-can-not-load-a-keras-nn-model
        weights = wandb.iloc[0:wandb.shape[0]-2, 1:wandb.shape[1]-3]
        innerbias = wandb["Bias"][0:wandb.shape[0]-2]
        outerlayerbias = wandb["Outputlayerweights"][0:wandb.shape[0]-2]
        outerbias = wandb["Outputbias"][0]
        minkWh = wandb["Bias"].iloc[-2]
        maxkWh = wandb["Bias"].iloc[-1]
        # print(maxkWh)

        # explode input data
        input_trans_minmax = pd.DataFrame(data_std)
        input_trans_minmax = input_trans_minmax.transpose()
        input_trans_minmax = input_trans_minmax.append([input_trans_minmax] * (weights.shape[0] - 1), ignore_index=True)

        inputxweights = np.multiply(weights.to_numpy(), input_trans_minmax)
        hiddensum = inputxweights.sum(axis=1)
        transfcnplusbias = np.tanh(hiddensum + innerbias)
        TFBplusbias = transfcnplusbias * outerlayerbias
        outerlayersum = sum(TFBplusbias)
        outerlayersumTF = np.tanh(outerlayersum + outerbias)

        predictionvalue = (((outerlayersumTF + 1) * (maxkWh - minkWh)) / 2) + minkWh

        return predictionvalue

    def predict_vacuum(self, data, wandb):
        # data = cooling_db.iloc[0, 1:9]
        # wandb = pd.read_csv('wandbcooling.csv')
        data["dairycows_total"] = np.log(data["dairycows_total"])
        data["milkyield"] = np.cbrt(data["milkyield"])
        data["totalvacuumpower"] = np.log(data["totalvacuumpower"])
        data["noofparlourunits"] = np.log(data["noofparlourunits"])
        minmax = wandb.iloc[wandb.shape[0]-2:wandb.shape[0], 1:wandb.shape[1]-3]
        data_std = pd.DataFrame(2 * np.subtract(data, minmax.iloc[0].values.tolist()) / np.subtract(minmax.iloc[1].values.tolist(), minmax.iloc[0].values.tolist()) -1)
        # wandbtotal = pd.to_pickle(wandb, 'wandbtotal.pkl')
        # wandbtotal = pd.read_pickle('wandbtotal.pkl')

        # https://stackoverflow.com/questions/45830206/pyinstaller-created-exe-file-can-not-load-a-keras-nn-model
        weights = wandb.iloc[0:wandb.shape[0]-2, 1:wandb.shape[1]-3]
        innerbias = wandb["Bias"][0:wandb.shape[0]-2]
        outerlayerbias = wandb["Outputlayerweights"][0:wandb.shape[0]-2]
        outerbias = wandb["Outputbias"][0]
        minkWh = wandb["Bias"].iloc[-2]
        maxkWh = wandb["Bias"].iloc[-1]
        # print(maxkWh)

        # explode input data
        input_trans_minmax = pd.DataFrame(data_std)
        input_trans_minmax = input_trans_minmax.transpose()
        input_trans_minmax = input_trans_minmax.append([input_trans_minmax] * (weights.shape[0] - 1), ignore_index=True)

        inputxweights = np.multiply(weights.to_numpy(), input_trans_minmax)
        hiddensum = inputxweights.sum(axis=1)
        transfcnplusbias = np.tanh(hiddensum + innerbias)
        TFBplusbias = transfcnplusbias * outerlayerbias
        outerlayersum = sum(TFBplusbias)
        outerlayersumTF = np.tanh(outerlayersum + outerbias)

        predictionvalue = (((outerlayersumTF + 1) * (maxkWh - minkWh)) / 2) + minkWh
        # predictionvalue.values[data["milkyield"] == 0] = 0
        return predictionvalue

    def predict_heating(self, data, wandb):
        # data = cooling_db.iloc[0, 1:9]
        # wandb = pd.read_csv('wandbcooling.csv')
        data["dairycows_milking"] = np.sqrt(data["dairycows_milking"])
        data["dairycows_total"] = np.log(data["dairycows_total"])
        data["milkyield"] = np.sqrt(data["milkyield"])
        data["totalwaterheatervolume"] = np.reciprocal(data["totalwaterheatervolume"])
        data["totalwaterheaterpower"] = 1/(1 + np.exp(-data["totalwaterheaterpower"]))
        minmax = wandb.iloc[wandb.shape[0]-2:wandb.shape[0], 1:wandb.shape[1]-3]
        data_std = pd.DataFrame(2 * np.subtract(data, minmax.iloc[0].values.tolist()) / np.subtract(minmax.iloc[1].values.tolist(), minmax.iloc[0].values.tolist()) -1)
        # wandbtotal = pd.to_pickle(wandb, 'wandbtotal.pkl')
        # wandbtotal = pd.read_pickle('wandbtotal.pkl')

        # https://stackoverflow.com/questions/45830206/pyinstaller-created-exe-file-can-not-load-a-keras-nn-model
        weights = wandb.iloc[0:wandb.shape[0]-2, 1:wandb.shape[1]-3]
        innerbias = wandb["Bias"][0:wandb.shape[0]-2]
        outerlayerbias = wandb["Outputlayerweights"][0:wandb.shape[0]-2]
        outerbias = wandb["Outputbias"][0]
        minkWh = wandb["Bias"].iloc[-2]
        maxkWh = wandb["Bias"].iloc[-1]
        # print(maxkWh)

        # explode input data
        input_trans_minmax = pd.DataFrame(data_std)
        input_trans_minmax = input_trans_minmax.transpose()
        input_trans_minmax = input_trans_minmax.append([input_trans_minmax] * (weights.shape[0] - 1), ignore_index=True)

        inputxweights = np.multiply(weights.to_numpy(), input_trans_minmax)
        hiddensum = inputxweights.sum(axis=1)
        transfcnplusbias = np.tanh(hiddensum + innerbias)
        TFBplusbias = transfcnplusbias * outerlayerbias
        outerlayersum = sum(TFBplusbias)
        outerlayersumTF = np.tanh(outerlayersum + outerbias)

        predictionvalue = (((outerlayersumTF + 1) * (maxkWh - minkWh)) / 2) + minkWh
        # predictionvalue.values[data["electric"] == 1] = 0
        return predictionvalue

    def predict_combined(self, data, wandb):
        # data = combined_db.iloc[0, 1:22]
        # wandb = pd.read_csv('wandbcooling.csv')
        # wandb = wandb_combined
        data["dairycows_milking"] = np.sqrt(data["dairycows_milking"])
        data["dairycows_total"] = np.log(data["dairycows_total"])
        data["milkyield"] = np.sqrt(data["milkyield"])
        data["noofparlourunits"] = np.log(data["noofparlourunits"])
        data["totalbulktankvolume"] = np.log(data["totalbulktankvolume"])
        data["totalvacuumpower"] = np.log(data["totalvacuumpower"])
        data["totalwaterheatervolume"] = np.reciprocal(data["totalwaterheatervolume"])
        data["totalwaterheaterpower"] = np.sqrt(data["totalwaterheaterpower"])
        minmax = wandb.iloc[wandb.shape[0]-2:wandb.shape[0], 1:wandb.shape[1]-3]
        data_std = pd.DataFrame(2 * np.subtract(data, minmax.iloc[0].values.tolist()) / np.subtract(minmax.iloc[1].values.tolist(), minmax.iloc[0].values.tolist()) -1)
        # wandbtotal = pd.to_pickle(wandb, 'wandbtotal.pkl')
        # wandbtotal = pd.read_pickle('wandbtotal.pkl')

        # https://stackoverflow.com/questions/45830206/pyinstaller-created-exe-file-can-not-load-a-keras-nn-model
        weights = wandb.iloc[0:wandb.shape[0]-2, 1:wandb.shape[1]-3]
        innerbias = wandb["Bias"][0:wandb.shape[0]-2]
        outerlayerbias = wandb["Outputlayerweights"][0:wandb.shape[0]-2]
        outerbias = wandb["Outputbias"][0]
        minkWh = wandb["Bias"].iloc[-2]
        maxkWh = wandb["Bias"].iloc[-1]

        # explode input data
        input_trans_minmax = pd.DataFrame(data_std)
        input_trans_minmax = input_trans_minmax.transpose()
        input_trans_minmax = input_trans_minmax.append([input_trans_minmax] * (weights.shape[0] - 1), ignore_index=True)

        inputxweights = np.multiply(weights.to_numpy(), input_trans_minmax)
        hiddensum = inputxweights.sum(axis=1)
        transfcnplusbias = np.tanh(hiddensum + innerbias)
        TFBplusbias = transfcnplusbias * outerlayerbias
        outerlayersum = sum(TFBplusbias)
        outerlayersumTF = np.tanh(outerlayersum + outerbias)

        predictionvalue = (((outerlayersumTF + 1) * (maxkWh - minkWh)) / 2) + minkWh
        return predictionvalue

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
        if self.cs_DX.isChecked():
            current_tv = current_tv.loc[(current_tv['coolingsystem_directexpansion'] == "yes")]
        elif self.cs_IB.isChecked():
            current_tv = current_tv.loc[(current_tv['coolingsystem_icebank'] == "yes")]

        # DER
        der_logical = [self.der_a.isChecked(), self.der_b.isChecked(), self.der_c.isChecked(), self.der_d.isChecked(), self.der_e.isChecked()]
        DER_selected = np.array(["A", "B", "C", "D", "E"])[np.array(der_logical)]
        current_tv = current_tv[(current_tv['DER'].isin(DER_selected))]

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
        self.filtereddatabase_ann = current_tv
        self.filtereddatabase_mth = current_charts

        self.mdl = self.firstTab.kpi_table(self.filtereddatabase_ann)
        self.firstTab.tableViewkpi.setModel(self.mdl)

class FirstTab(QWidget):
    def __init__(self, tabwidget):
        super(FirstTab, self).__init__()
        self.tabwidget = tabwidget
        self.data = tabwidget.data
        self.filtereddatabase = []
        self.filtereddatabase_ann = []

        bottomright = QGridLayout()
        bottomright.addWidget(self.kpi(self.filtereddatabase_ann), 0, 0, 1, 1)
        bottomright.addWidget(self.info(self.data), 1, 0, 2, 1)

        # Grid layout of entire tab
        layout = QGridLayout()
        layout.addWidget(self.infrastructure(self.data), 0, 0)
        layout.addWidget(self.energy(), 0, 1)
        layout.addWidget(self.energymonth(), 1, 0)
        layout.addLayout(bottomright, 1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)


        self.setLayout(layout)

    def info(self, data):  # function defining characteristics of each group/grid object
        groupBox = QGroupBox("Terms + Conditions")
        label = QTextEdit()
        label.setFrameStyle(0)
        label.setReadOnly(True)
        label.textCursor().insertHtml("The National Artificial Intelligent Dairy Energy Application (NAIDEA) was developed and is maintained by researchers in the MeSSO research group at the Munster Technological University (messo.mtu.ie). NAIDEA is not for use by commercial bodies. Contact messo@mtu.ie for further information.")

        ExLayout = QVBoxLayout()
        ExLayout.addWidget(label)

        groupBox.setLayout(ExLayout)
        groupBox.setFlat(True)

        return groupBox

    def kpi_table(self, data):

        try:
            val = len(data)
            if val == 0:
                self.modelkpi.setItem(0, 0, QStandardItem(str("")))
            else:
                self.modelkpi.setItem(0, 0, QStandardItem(str(f'{round(val):,}')))
        except:
            self.modelkpi.setItem(0, 0, QStandardItem(str("")))

        try:
            val = sum(data["TotalKWh"])
            if val == 0:
                self.modelkpi.setItem(0, 1, QStandardItem(str("")))
            else:
                self.modelkpi.setItem(0, 1, QStandardItem(str(f'{round(val):,}')))
        except:
            self.modelkpi.setItem(0, 1, QStandardItem(str("")))

        try:
            val = sum(data["TotalKWh"]) / sum(data["milk_yield_litres"]) * 1000
            self.modelkpi.setItem(0, 2, QStandardItem(str(round(val, 1))))
        except:
            self.modelkpi.setItem(0, 2, QStandardItem(str("")))

        try:
            val = data["TotalKWh"] / data["herd_size"]
            val = val.mean()
            if val == 0:
                self.modelkpi.setItem(0, 3, QStandardItem(str("")))
            else:
                self.modelkpi.setItem(0, 3, QStandardItem(str(f'{round(val):,}')))

        except:
            self.modelkpi.setItem(0, 3, QStandardItem(str("")))

        try:
            val = sum(data["TotalKWh"]) / sum(data["milk_yield_litres"]) * 1000
            bins = [0, 23, 36, 49, 62, 1000]
            DER = np.digitize(val, bins)
            DER = DER.astype(str)
            DER = DER.replace(str(1), 'A')
            DER = DER.replace(str(2), 'B')
            DER = DER.replace(str(3), 'C')
            DER = DER.replace(str(4), 'D')
            DER = DER.replace(str(5), 'E')
            self.modelkpi.setItem(0, 4, QStandardItem(DER))
        except:
            self.modelkpi.setItem(0, 4, QStandardItem(str("")))

        try:
            val = sum(data["TotalKWh"])*.324
            if val == 0:
                self.modelkpi.setItem(0, 5, QStandardItem(str("")))
            else:
                self.modelkpi.setItem(0, 5, QStandardItem(str(f'{round(val):,}')))
        except:
            self.modelkpi.setItem(0, 5, QStandardItem(str("")))

        return self.modelkpi

    def kpi(self, data):
        qss = """
        {border: none;}
        """
        groupBoxkpi = QGroupBox("Key Performance Indicators")

        self.modelkpi = QtGui.QStandardItemModel(self)
        self.modelkpi.setRowCount(1)
        self.modelkpi.setColumnCount(6)
        self.tableViewkpi = QtWidgets.QTableView(self)
        self.tableViewkpi.setFixedHeight(62) # height of available space
        self.tableViewkpi.setShowGrid(False) # removes horizontal lines
        self.tableViewkpi.setStyleSheet('QTableView::item {border-right: 1px solid #d6d9dc; QTableView::item {border-bottom: 1px solid #d6d9dc;}')
        self.tableViewkpi.setFrameStyle(0)
        self.tableViewkpi.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableViewkpi.setObjectName("tableViewkpi")
        self.tableViewkpi.verticalHeader().hide()
        self.modelkpi.setHeaderData(0, Qt.Horizontal, "No. of Farms")
        self.modelkpi.setHeaderData(1, Qt.Horizontal, "kWh")
        self.modelkpi.setHeaderData(2, Qt.Horizontal, "Wh / Lm")
        self.modelkpi.setHeaderData(3, Qt.Horizontal, "kWh /Farm /Cow")
        self.modelkpi.setHeaderData(4, Qt.Horizontal, "Average DER")
        self.modelkpi.setHeaderData(5, Qt.Horizontal, "kg CO\u2082")
        # 'kh CO{}'.format(get_sub('2'))

        # Align text in tableview
        for item in range(0, 6):
            self.tableViewkpi.setItemDelegateForColumn(item, AlignDelegate(self.kpi_table(data)))

        self.tableViewkpi.setModel(self.kpi_table(data))

        layout = QHBoxLayout()
        layout.addWidget(self.tableViewkpi)


        groupBoxkpi.setLayout(layout)
        groupBoxkpi.setFlat(True)
        return groupBoxkpi

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
        self.radioButton1.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton1)

        self.radioButton2 = QRadioButton("Green Electricity")
        self.radioButton2.setChecked(True)
        self.radioButton2.label = "green_electricity"
        self.radioButton2.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton2)

        self.radioButton3 = QRadioButton("Variable Speed Drive")
        self.radioButton3.label = "VSD"
        self.radioButton3.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton3)

        self.radioButton4 = QRadioButton("Plate Cooler")
        self.radioButton4.label = "coolingsystem_platecooler"
        self.radioButton4.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
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
            # Fix DER Chart here
            # importedfile.to_csv('IF.csv')
            # importedfile = importedfile[["farm_id", "DER"]].drop_duplicates()
            # print(importedfile)
            # fig = go.Pie(labels=importedfile["DER"], hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>")
            kwhdata = importedfile[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]]
            summed = round(kwhdata.sum(axis=0))
            fig = go.Pie(labels=["Milk Cooling", "Milk Harvesting", "Water Heating", "Other Use"], values=summed.values,
                         hovertemplate="%{label}: <br>Sum: %{value} kWh <extra></extra>")

        elif self.radioButton7.isChecked():
            summed = round(kwhdata.sum(axis=0)*0.324)
            fig = go.Pie(labels=["Milk Cooling", "Milk Harvesting", "Water Heating", "Other Use"], values=summed.values,  hovertemplate = "%{label}: <br>Sum: %{value} kg CO\u2082 <extra></extra>")

        layout = go.Layout(autosize=True, legend=dict(orientation="h",xanchor='center', x=0.5))
        fig = go.Figure(data=fig, layout=layout)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        self.browserEn.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def energy(self):
        groupBox = QGroupBox("Energy/Carbon Breakdown")

        right = QVBoxLayout()

        self.radioButton5 = QRadioButton("Energy Breakdown")
        self.radioButton5.toggled.connect(lambda: self.energychart(self.tabwidget.filtereddatabase_mth))
        right.addWidget(self.radioButton5)

        self.radioButton6 = QRadioButton("Dairy Energy Rating")
        self.radioButton6.setChecked(True)
        self.radioButton6.toggled.connect(lambda: self.energychart(self.tabwidget.filtereddatabase_mth))
        right.addWidget(self.radioButton6)

        self.radioButton7 = QRadioButton("Carbon Dioxide")
        self.radioButton7.toggled.connect(lambda: self.energychart(self.tabwidget.filtereddatabase_mth))
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

    def energymonth(self): # box and whisker
        groupBox = QGroupBox("Monthly Energy Statistics")

        right = QVBoxLayout()

        self.radioButton8 = QRadioButton("Electricity Use")
        self.radioButton8.setChecked(True)
        self.radioButton8.toggled.connect(lambda: self.BLChart(self.tabwidget.filtereddatabase_mth))
        right.addWidget(self.radioButton8)

        self.radioButton9 = QRadioButton("Electricity Use / Litre")
        self.radioButton9.toggled.connect(lambda: self.BLChart(self.tabwidget.filtereddatabase_mth))
        right.addWidget(self.radioButton9)

        self.radioButton10 = QRadioButton("Electricity Use / Farm / Cow")
        self.radioButton10.toggled.connect(lambda: self.BLChart(self.tabwidget.filtereddatabase_mth))
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

        groupBox = QGroupBox("Help Section")
        label = QTextEdit()
        label.setFrameStyle(0)
        label.setReadOnly(True)
        label.textCursor().insertHtml("Helpful Information.")

        checkbox = QCheckBox("Agree the T&C's")

        #create layout
        layout = QVBoxLayout()
        layout.addWidget(label)
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

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    window = mainwindow(data=None)
    window.show()
    app.exec()