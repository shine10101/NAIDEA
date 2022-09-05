from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog, QPushButton, QHBoxLayout, QRadioButton, QGridLayout, \
    QLabel, QGroupBox, QCheckBox, QDialogButtonBox, QTabWidget, QVBoxLayout, QButtonGroup, QTextEdit, QDialog, QWidget, QApplication
from qtrangeslider import QLabeledRangeSlider
from PyQt5.QtGui import QStandardItem, QIcon, QPixmap, QIntValidator
from PyQt5 import QtWebEngineWidgets, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import sys
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import time
import statistics
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class mainwindow(QDialog):
    def __init__(self, data):
        super(mainwindow, self).__init__()
        self.data = data

        # create header sections
        FilterLayout = QHBoxLayout()
        FilterLayout.addWidget(self.createHeader1a(), 1)#import/export
        FilterLayout.addWidget(self.createHeader2a(), 4)# filters
        FilterLayout.addWidget(self.Header3(), 4)  # images

        # Macro-level statistics tab instance
        self.firstTab = FirstTab(self)

        # KPI table
        self.model = QtGui.QStandardItemModel(self)

        # Farm-level table
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableView.setObjectName("tableView")

        # Tab widget objects
        tabs = QTabWidget()
        tabs.addTab(self.firstTab, "Macro-Level")
        tabs.addTab(self.tableView, "Farm-Level")
        tabs.addTab(ThirdTab(), "Help")

        # GUI buttons
        buttonbox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        # GUI Layout
        vbox = QVBoxLayout()
        vbox.addLayout(FilterLayout, 1)
        vbox.addWidget(tabs, 6)
        vbox.addWidget(buttonbox)

        self.setLayout(vbox)

    def createHeader1a(self): # Header Object: Import/Export | Filter | Collaboration

        HeaderBox = QGroupBox("Import/Export Data")

        # Import/Export/CO2 section
        inputfilebtn = QPushButton("Import")
        inputfilebtn.clicked.connect(self.on_pushButtonLoad_clicked) # Load data file when clicked

        self.inptbox = QLineEdit(self)
        self.inptbox.setStyleSheet("border: 0px solid red;")
        self.inptbox.setAlignment(Qt.AlignCenter)
        onlyInt = QIntValidator()
        self.inptbox.setValidator(onlyInt)

        # gCO2 / kWh input box/value
        if not hasattr(self, "carbon"):
            self.inptbox.setText(str(296))

        boxlabel = QLabel("gCO\u2082 / kWh")

        # Export button
        exportfilebtn = QPushButton("Export")
        exportfilebtn.clicked.connect(self.export_clicked)

        # Row 1
        importrow1layout = QHBoxLayout()
        importrow1layout.addWidget(inputfilebtn)
        importrow1layout.addStretch()

        # Row 2
        importrow2layout = QHBoxLayout()
        importrow2layout.addWidget(exportfilebtn)
        importrow2layout.addStretch()

        # Row 3
        importrow3layout = QHBoxLayout()
        importrow3layout.addWidget(self.inptbox)
        importrow3layout.addWidget(boxlabel)
        importrow3layout.addStretch()

        # Import/ Export seciton layout
        HeaderLayout = QGridLayout()
        HeaderLayout.addLayout(importrow1layout, 0, 1)
        HeaderLayout.addLayout(importrow2layout, 1, 1)
        HeaderLayout.addLayout(importrow3layout, 2, 1)
        HeaderBox.setLayout(HeaderLayout)
        HeaderBox.setFlat(True)

        return HeaderBox

    def createHeader2a(self): # Header Object: Filter data section

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

        # Section Heading
        HeaderBox = QGroupBox("Filter Data")

        # Filter section layout (left)
        leftlayout = QGridLayout()

        # Define seperate group for each radio button (n = 3)
        self.radiogroup1 = QButtonGroup()
        self.radiogroup2 = QButtonGroup()
        self.radiogroup3 = QButtonGroup()

        # Radio button 1
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

        # Radio button 2
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

        # Radio button 3
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

        # Filter section layout (right)
        righttoplayout = QHBoxLayout()
        rightmiddlelayout = QHBoxLayout()
        rightbottomlayout = QHBoxLayout()

        # Range Slider Object for filtering herd size
        #https://pythonrepo.com/repo/tlambert03-QtRangeSlider-python-graphical-user-interface-applications
        label4 = QLabel(self)
        label4.setText("Farm Size\n(No. Cows):")
        label4.setAlignment(Qt.AlignLeft)
        righttoplayout.addWidget(label4)
        self.slider1 = QLabeledRangeSlider(Qt.Horizontal)
        self.slider1.setSingleStep(step=25)
        self.slider1.setEdgeLabelMode(opt=0)
        self.slider1.setHandleLabelPosition(opt=2)
        self.slider1.setRange(5, 2001)
        self.slider1.setTickInterval(25)
        self.slider1.setValue((5, 2000))
        self.slider1.setStyleSheet(QSS)
        righttoplayout.addWidget(self.slider1)

        # Filter a/c to calculater DER of each farm
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

        # Filter button to initiate filtering of data
        self.filterbutton = QPushButton("Filter")
        self.filterbutton.clicked.connect(self.on_filterButtonLoad_clicked)
        rightmiddlelayout.addWidget(self.filterbutton)

        # Filter section (right) layout
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
        HeaderBox.setFlat(True)

        return HeaderBox

    def Header3(self): # Header section: collaboration logos
        HeaderBox = QGroupBox("A Collaboration of:")

        label_collab = QLabel()
        pixmap = QPixmap("collab2_trans.png")
        pixmap2 = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label_collab.setPixmap(pixmap2)

        grid = QHBoxLayout()
        grid.addWidget(label_collab)
        HeaderBox.setLayout(grid)

        HeaderBox.setFlat(True)
        return HeaderBox

    def getfile(self): # Import dataset

        # Open file dialog | .csv files only
        option = QFileDialog.Options()
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                CURRENT_DIR, "CSV files (*.csv)", options=option)

        # read file
        # fname = "C:/NAIDEA SAMPLE DATA_BordBia.csv"
        # df1 = pd.read_csv(fname)
        df1 = pd.read_csv(fname[0])

        # Manual filtering
        df1 = df1.drop_duplicates(subset=['farm_id', 'month_str'], keep='first', inplace=False) # drop rows with duplicate farm id and months
        df1 = df1[df1["milking_frequency"].str.contains("Robotic milking frequency") == False] # drop farms with robotic milking
        df1 = df1.reset_index()

        # Create datasets specific to predicting each Dependent variable
        total_db, cooling_db, vacuum_db, heating_db, combined_db = self.processimportedfile(df1)

        # Identify farms requiring scaling
        df_scaling = total_db[["farm_id", "dairycows_total"]].groupby("farm_id").mean().round()
        farmstoscale = df_scaling.index[df_scaling["dairycows_total"] >500].tolist()
        total_scale = total_db[total_db['farm_id'].isin(farmstoscale)]
        cooling_scale = cooling_db[cooling_db['farm_id'].isin(farmstoscale)]
        vacuum_scale = vacuum_db[vacuum_db['farm_id'].isin(farmstoscale)]
        heating_scale = heating_db[heating_db['farm_id'].isin(farmstoscale)]
        combined_scale = combined_db[combined_db['farm_id'].isin(farmstoscale)]

        # Begin scaling here
        scaling_factor = df_scaling[df_scaling["dairycows_total"] >500]/250

        total_scale = self.scaleds(total_scale, scaling_factor, 'down')
        cooling_scale = self.scaleds(cooling_scale, scaling_factor, 'down')
        vacuum_scale = self.scaleds(vacuum_scale, scaling_factor, 'down')
        heating_scale = self.scaleds(heating_scale, scaling_factor, 'down')
        combined_scale = self.scaleds(combined_scale, scaling_factor, 'down')

        # Update dataframes with scaled values for prediction
        total_db.update(total_scale)
        cooling_db.update(cooling_scale)
        vacuum_db.update(vacuum_scale)
        heating_db.update(heating_scale)
        combined_db.update(combined_scale)

        # Load csv files (required for updating pfl files with ANN weights and biases)
        # wandb_total = pd.read_csv('new_wandbtotalkwh.csv')
        # wandb_total = wandb_total.iloc[:, :-2]
        # wandb_cooling = pd.read_csv('wandbcoolingkwh.csv')
        # wandb_vacuum = pd.read_csv('wandbvacuumkwh.csv')
        # wandb_heating = pd.read_csv('wandbwaterheatkwh.csv')
        # wandb_combined = pd.read_csv('wandbcombinedkwh.csv')
        # Convert to pickle files
        # wandbtotal = pd.to_pickle(wandb_total, 'new_wandbtotalkwh.pkl')
        # wandb_cooling = pd.to_pickle(wandb_cooling, 'wandbcoolingkwh.pkl')
        # wandb_vacuum = pd.to_pickle(wandb_vacuum, 'wandbvacuumkwh.pkl')
        # wandb_heating = pd.to_pickle(wandb_heating, 'wandbwaterheatkwh.pkl')
        # wandb_combined = pd.to_pickle(wandb_combined, 'wandbcombinedkwh.pkl')

        # Read pickle files
        wandb_total = pd.read_pickle('new_wandbtotalkwh.pkl')
        wandb_cooling = pd.read_pickle('wandbcoolingkwh.pkl')
        wandb_vacuum = pd.read_pickle('wandbvacuumkwh.pkl')
        wandb_heating = pd.read_pickle('wandbwaterheatkwh.pkl')
        wandb_combined = pd.read_pickle('wandbcombinedkwh.pkl')
        t = time.time()
        # Predict monthly total, cooling, vacuum, heating and combined kWh consumption
        total = total_db.iloc[:, 1:total_db.shape[1]]
        df1["TotalKWh"] = pd.DataFrame([self.predict_total(data=row, wandb=wandb_total) for idx, row in total.iterrows()], columns=['TotalKWh'])
        cooling = cooling_db.iloc[:, 1:cooling_db.shape[1]]
        df1["CoolingKWh"] = pd.DataFrame([self.predict_cooling(data=row, wandb=wandb_cooling) for idx, row in cooling.iterrows()], columns=['CoolingKWh'])
        vacuum = vacuum_db.iloc[:, 1:vacuum_db.shape[1]]
        df1["VacuumKWh"] = pd.DataFrame([self.predict_vacuum(data=row, wandb=wandb_vacuum) for idx, row in vacuum.iterrows()], columns=['VacuumKWh'])
        heating = heating_db.iloc[:, 1:heating_db.shape[1]]
        df1["WaterHeatKWh"] = pd.DataFrame([self.predict_heating(data=row, wandb=wandb_heating) for idx, row in heating.iterrows()], columns=['WaterHeatKWh'])
        combined = combined_db.iloc[:, 1:combined_db.shape[1]]
        df1["CombinedKWh"] = pd.DataFrame([self.predict_combined(data=row, wandb=wandb_combined) for idx, row in combined.iterrows()], columns=['CombinedKWh'])
        print(time.time()-t)

        # Scale up prediction values a/c to scaling factor
        df1_scale = df1[df1['farm_id'].isin(farmstoscale)]
        df1_scale = self.scaleds(df1_scale, scaling_factor, 'up')
        df1.update(df1_scale)

        # Manual processing
        # Milk cooling and vacuum equals 0 when milk production = 0
        df1['CoolingKWh'].values[df1['milk_yield_litres'] == 0] = 0
        df1['VacuumKWh'].values[df1['milk_yield_litres'] == 0] = 0

        # Water heating kWh equals 0 when gas/oil water heating used
        df1['WaterHeatKWh'].values[df1['waterheating_power_elec_kw'] == 0] = 0

        # Adjust cooling, vacuum and WH based on their % of combined prediction
        CVW = df1['CoolingKWh']+df1['VacuumKWh']+df1['WaterHeatKWh']
        df1['CoolingKWh'] = df1['CombinedKWh']*(sum(df1['CoolingKWh'])/sum(CVW))
        df1['VacuumKWh'] = df1['CombinedKWh']*(sum(df1['VacuumKWh'])/sum(CVW))
        df1['WaterHeatKWh'] = df1['CombinedKWh']*(sum(df1['WaterHeatKWh'])/sum(CVW))
        df1["OtherKWh"] = df1["TotalKWh"] - df1["CombinedKWh"]
        df2 = df1[["farm_id", "milk_yield_litres", "TotalKWh"]].groupby("farm_id", as_index=False).sum().round()#, "CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"

        # merge datasets (1. mean herd size and milking cows | 2. sum milk yield and total kWh)
        df3_size = df1[["farm_id", "herd_size", "milking_cows"]].groupby("farm_id").mean().round()
        df2 = pd.merge(left=df3_size, right=df2, left_on='farm_id', right_on='farm_id')

        # Extract features for each farm (i.e. drop duplicates)
        df4 = df1[["farm_id", "re_thermal_m3", "re_solarpv_kw", "re_wind_kw", "res_capacity_kw", "low_energy_lighting",
                       "night_rate_electricity", "heat_recovery", "green_electricity", "num_parlour_units", "milking_frequency",
                       "milking_duration_hours", "hotwash_freq", "milkpump_type", "vacuumpump_power_kw", "VSD", "bulktank_capacity_litres",
                       "waterheating_power_elec_kw", "waterheating_power_gas_kw", "waterheating_power_oil_kw", "hotwatertank_capacity_litres",
                       "coolingsystem_directexpansion", "coolingsystem_platecooler", "coolingsystem_icebank", "coolingsystem_waterchillingunit"]].drop_duplicates(subset='farm_id', keep="first")

        # Renewable Energy Technologies (binary for pie chart)
        retech = df4[["re_thermal_m3", "re_solarpv_kw", "re_wind_kw"]]
        retech.values[retech > 0] = 1
        retech['retech'] = retech['re_thermal_m3'].astype(str) + '_' + retech['re_solarpv_kw'].astype(str)\
                           + '_' + retech['re_wind_kw'].astype(str)
        retech['retech'].values[retech['retech'] == '1.0_0.0_0.0'] = 'Solar Thermal'
        retech['retech'].values[retech['retech'] == '1.0_1.0_0.0'] = 'Solar Thermal, PV'
        retech['retech'].values[retech['retech'] == '1.0_1.0_1.0'] = 'Thermal, PV, Wind'
        retech['retech'].values[retech['retech'] == '0_1.0.0_1.0'] = 'PV, Wind'
        retech['retech'].values[retech['retech'] == '0.0_1.0_0.0'] = 'Solar PV'
        retech['retech'].values[retech['retech'] == '0.0_0.0_1.0'] = 'Wind'
        retech['retech'].values[retech['retech'] == '1_0.0.0_1.0'] = 'Solar Thermal, Wind'
        retech['retech'].values[retech['retech'] == '0.0_0.0_0.0'] = 'None'

        retech['retech'].values[retech['retech'] == '1_0_0'] = 'Solar Thermal'
        retech['retech'].values[retech['retech'] == '1_1_0'] = 'Solar Thermal, PV'
        retech['retech'].values[retech['retech'] == '1_1_1'] = 'Thermal, PV, Wind'
        retech['retech'].values[retech['retech'] == '0_1_1'] = 'PV, Wind'
        retech['retech'].values[retech['retech'] == '0_1_0'] = 'Solar PV'
        retech['retech'].values[retech['retech'] == '0_0_1'] = 'Wind'
        retech['retech'].values[retech['retech'] == '1_0_1'] = 'Solar Thermal, Wind'
        retech['retech'].values[retech['retech'] == '0_0_0'] = 'None'

        # merge (df2 and df4)
        df4['retech'] = retech['retech']
        df2 = pd.merge(left=df2, right=df4, left_on='farm_id', right_on='farm_id')
        # rule of thumb solar pV calculation, as per DEAP software
        df2['pv_kwh'] = round(0.8 * df2["re_solarpv_kw"] * 1074 * 1, 1)  # constant x kWp x kWh/m2 x overshdowing factor
        df2["TotalKWh"] = df2["TotalKWh"] - df2['pv_kwh']
        # Ref: https://www.seai.ie/home-energy/building-energy-rating-ber/support-for-ber-assessors/domestic-ber-resources/
        # Ref: https://www.rexelenergysolutions.ie/solar-electricity/part-l-using-solar-pv/

        # Subtract PB kWh from total kWh
        df2["TotalKWh"] = round(df2["TotalKWh"] - df2['pv_kwh'],1)
        df2['TotalKWh'].values[df2['TotalKWh'] < 0] = 0

        # Process Wh/lm & categorise into bins
        df2["wh_lm"] = round(df2["TotalKWh"]/ df2["milk_yield_litres"] * 1000,2)
        df2["global_diff_%"] = round((df2["wh_lm"] - statistics.mean(df2["wh_lm"])) / statistics.mean(df2["wh_lm"]) * 100,2)
        self.bins = [0, 23,	36,	49,	62,	1000] # bins calculated using monitored dataset
        df2["DER"] = pd.DataFrame(np.digitize(df2["wh_lm"], self.bins), columns=["DER"])
        df2['DER'] = df2['DER'].astype(str)
        df2['DER'] = df2['DER'].replace(str(1), 'A')
        df2['DER'] = df2['DER'].replace(str(2), 'B')
        df2['DER'] = df2['DER'].replace(str(3), 'C')
        df2['DER'] = df2['DER'].replace(str(4), 'D')
        df2['DER'] = df2['DER'].replace(str(5), 'E')
        first_column = df2.pop('DER')
        df2.insert(1, 'DER', first_column)

        # Recommendations: low_energy_lighting, coolingsystem_platecooler, VSD, retech
        # data = data.drop_duplicates(subset='farm_id', keep="first")
        # data = data.reset_index()
        df2['coolingsystem_platecooler'] = df2['coolingsystem_platecooler'].fillna('n/a')
        df2['VSD'] = df2['VSD'].fillna('n/a')
        df2['low_energy_lighting'] = df2['low_energy_lighting'].fillna('n/a')
        red = []
        for row in range(0,len(df2)):
            if df2['low_energy_lighting'].iloc[row].lower() == "no":
                txt1 = "Install energy efficient lighting ; "
            else:
                txt1 = ""

            if df2['coolingsystem_platecooler'].iloc[row].lower() == "no":
                txt2 = "Install milk pre-cooling system ; "
            else:
                txt2 = ""

            if df2['VSD'].iloc[row].lower() == "no":
                txt3 = "Install variable speed drive ; "
            else:
                txt3 = ""

            if df2['retech'].iloc[row].lower() == "none":
                txt4 = "Install renewable energy system"
            else:
                txt4 = ""

            red.append(txt1+txt2+txt3+txt4)

        second_column = pd.DataFrame(red, columns = ['Recommendations'])
        df2.insert(2, 'Recommendations', second_column)

        self.tvdatabase = df2 # annual database
        self.model = PandasModel(df2) # KPI table
        self.tableView.setModel(self.model) # farm-level table


        if fname:
            return df1, df2

    def scaleds(self, total_scale, scaling_factor, action):
        fts = scaling_factor.index.tolist()
        if action =='down':

            for id in fts:
                if 'dairycows_total' in total_scale.columns:
                    total_scale.dairycows_total[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()
                if 'dairycows_milking' in total_scale.columns:
                    total_scale.dairycows_milking[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()
                if 'milkyield' in total_scale.columns:
                    total_scale.milkyield[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()
                if 'noofparlourunits' in total_scale.columns:
                    total_scale.noofparlourunits[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()
                if 'totalbulktankvolume' in total_scale.columns:
                    total_scale.totalbulktankvolume[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()
                if 'totalvacuumpower' in total_scale.columns:
                    total_scale.totalvacuumpower[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()
                if 'totalwaterheatervolume' in total_scale.columns:
                    total_scale.totalwaterheatervolume[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()
                if 'totalwaterheaterpower' in total_scale.columns:
                    total_scale.totalwaterheaterpower[total_scale.farm_id == id] /= scaling_factor.dairycows_total[
                        scaling_factor.index == id].tolist()

        elif action == 'up':

            for id in fts:
                total_scale.TotalKWh[total_scale.farm_id == id] *= scaling_factor.dairycows_total[
                    scaling_factor.index == id].tolist()
                total_scale.CoolingKWh[total_scale.farm_id == id] *= scaling_factor.dairycows_total[
                    scaling_factor.index == id].tolist()
                total_scale.VacuumKWh[total_scale.farm_id == id] *= scaling_factor.dairycows_total[
                    scaling_factor.index == id].tolist()
                total_scale.WaterHeatKWh[total_scale.farm_id == id] *= scaling_factor.dairycows_total[
                    scaling_factor.index == id].tolist()
                total_scale.CombinedKWh[total_scale.farm_id == id] *= scaling_factor.dairycows_total[
                    scaling_factor.index == id].tolist()

        return total_scale

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self): # update charts when import button pressed

        importedfile, annfile = self.getfile()

        if importedfile is None:
            return

        self.firstTab.MRChart(annfile)
        self.firstTab.BLChart(importedfile)
        self.firstTab.energychart(importedfile, annfile)
        self.importedfile = importedfile
        self.on_filterButtonLoad_clicked() # adjust data based on filter section parameters

    @QtCore.pyqtSlot()
    def export_clicked(self): # export treeview file as .csv

        if hasattr(self, "tvdatabase"):

            fileforexport = self.filtereddatabase_ann


            if fileforexport is None:
                return

            option = QFileDialog.Options()
            fname, _ = QFileDialog.getSaveFileName(self, 'Save file',
                                                CURRENT_DIR, "CSV files (*.csv)", options=option)
            if fname:
                fileforexport.to_csv(fname, index=False)

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Export Data")
            msg.setText("Please import data.")
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def processimportedfile(self, data):
        # fname = "C:/NAIDEA SAMPLE DATA_BordBia.csv"
        # data = pd.read_csv(fname)

        # Replace 0 values with nan values
        data['vacuumpump_power_kw'] = data['vacuumpump_power_kw'].replace(0, np.nan)
        data['num_parlour_units'] = data['num_parlour_units'].replace(0, np.nan)
        data['hotwatertank_capacity_litres'] = data['hotwatertank_capacity_litres'].replace(0, np.nan)
        data['waterheating_power_elec_kw'] = data['waterheating_power_elec_kw'].replace(0, np.nan)
        data['bulktank_capacity_litres'] = data['bulktank_capacity_litres'].replace(0, np.nan)

        # Replace values greater than X (assume erroneous) -
        data['vacuumpump_power_kw'][data['vacuumpump_power_kw'] >= 1000] = data['vacuumpump_power_kw'] / 1000
        data['waterheating_power_elec_kw'][data['waterheating_power_elec_kw'] >= 1000] =  data['waterheating_power_elec_kw'] / 1000
        data['bulktank_capacity_litres'][data['bulktank_capacity_litres'] >= 50000] = data['bulktank_capacity_litres'] / 10

        data['vacuumpump_power_kw'][data['vacuumpump_power_kw'] >= 100] = data['vacuumpump_power_kw'] / 100
        data['waterheating_power_elec_kw'][data['waterheating_power_elec_kw'] >= 100] =  data['waterheating_power_elec_kw'] / 100

        data['vacuumpump_power_kw'][data['vacuumpump_power_kw'] >= 20] = data['vacuumpump_power_kw'] / 10
        data['waterheating_power_elec_kw'][data['waterheating_power_elec_kw'] >= 20] =  data['waterheating_power_elec_kw'] / 10

        # replace nan values with 0
        data['re_solarpv_kw'] = data['re_solarpv_kw'].fillna(0)
        data['re_wind_kw'] = data['re_wind_kw'].fillna(0)
        data['re_thermal_m3'] = data['re_thermal_m3'].fillna(0)
        data['coolingsystem_platecooler'] = data['coolingsystem_platecooler'].fillna('n/a')
        data['VSD'] = data['VSD'].fillna('n/a')
        data['low_energy_lighting'] = data['low_energy_lighting'].fillna('n/a')

        # Replace missing values according to farm size using regression coefficients
        data['farm_id'] = pd.Categorical(data.farm_id)
        farmdata = data[["farm_id", "herd_size"]].groupby("farm_id").mean()
        b = np.linspace(0,2000, 41)
        BIN = pd.DataFrame(np.digitize(farmdata, b), columns=['bins'])
        BIN = BIN.set_index(farmdata.index)
        show = pd.concat([farmdata, pd.DataFrame(BIN, columns=['bins'])], axis=1)

        fd = data.drop_duplicates("farm_id")
        fd = fd.set_index('farm_id')
        fd['month'].update(show['bins'])
        fd = fd.rename(columns={'month': 'bins'})

        fd = fd[['bins','num_parlour_units', 'vacuumpump_power_kw', 'waterheating_power_elec_kw', 'bulktank_capacity_litres', 'hotwatertank_capacity_litres']]
        # mdls = pd.read_csv('missingdatamodels.csv')
        # MDM = pd.to_pickle(mdls, 'missingdatamodels.pkl')
        MDM = pd.read_pickle('missingdatamodels.pkl') # missing data model coefficients

        fd2 = fd
        # infer missing datapoints in fd
        for column in fd.columns:
            for row in range(0,len(fd)):
                if pd.isna(fd[column].iloc[row]):
                    fd2[column].iloc[row] = (fd.bins.iloc[row]*MDM[column].iloc[1]) + MDM[column].iloc[0]

        #Round infered data
        fd2["vacuumpump_power_kw"] = round(fd2["vacuumpump_power_kw"], 1)
        fd2["waterheating_power_elec_kw"] = round(fd2["waterheating_power_elec_kw"], 1)
        fd2["num_parlour_units"] = round(fd2["num_parlour_units"], 0)

        # replace in data
        for column in fd2.columns[1:]:
            for row in range(0,len(fd2)):
                farmid = fd2.index[row]
                col = column
                data[col][data['farm_id'] == farmid] = fd2[col].iloc[row]

        # replace herd and milking cow numbers with mean for that month
        x = data.groupby(data.month).herd_size.mean()
        xx = data.groupby(data.month).milking_cows.mean()
        for item in range(len(data)):
            if data['herd_size'][item] == 0:
                m = data['month'][item]
                data['herd_size'][item] = round(x[m],0)
                data['milking_cows'][item] = round(xx[m], 0)

        # Change Yes to yes etc..
        data['VSD'] = data['VSD'].replace("Yes", "yes")
        data['coolingsystem_directexpansion'] = data['coolingsystem_directexpansion'].replace("Yes", "yes")
        data['coolingsystem_icebank'] = data['coolingsystem_icebank'].replace("Yes", "yes")
        data['coolingsystem_platecooler'] = data['coolingsystem_platecooler'].replace("Yes", "yes")
        data['VSD'] = data['VSD'].replace("No", "no")
        data['coolingsystem_directexpansion'] = data['coolingsystem_directexpansion'].replace("No", "no")
        data['coolingsystem_icebank'] = data['coolingsystem_icebank'].replace("No", "no")
        data['coolingsystem_platecooler'] = data['coolingsystem_platecooler'].replace("No", "no")

        data_mdl = data[["farm_id", "month", "milk_yield_litres", "herd_size", "milking_cows",
                     "re_thermal_m3", "num_parlour_units", "milking_frequency", "hotwash_freq",
                     "milkpump_type", "vacuumpump_power_kw", "VSD", "bulktank_capacity_litres",
                     "waterheating_power_elec_kw", "waterheating_power_gas_kw", "waterheating_power_oil_kw",
                     "hotwatertank_capacity_litres","coolingsystem_directexpansion", "coolingsystem_platecooler",
                     "coolingsystem_icebank", "coolingsystem_waterchillingunit"]]

        data_mdl['re_thermal_m3'].values[data_mdl['re_thermal_m3'] > 0] = 2
        data_mdl['re_thermal_m3'].values[data_mdl['re_thermal_m3'] == 0] = 1

        # Rename column headings
        data_mdl = data_mdl.rename(columns={"month": "Month", "milk_yield_litres": "MilkYield", "herd_size": "DairyCows_Total",
                                            "milking_cows": "DairyCows_Milking", "re_thermal_m3": "Parlour_SolarThermalY_N",
                                            "num_parlour_units": "NoOfParlourUnits", "waterheating_power_elec_kw": "TotalWaterHeaterPower",
                                            "hotwatertank_capacity_litres": "TotalWaterHeaterVolume", "bulktank_capacity_litres": "TotalBulkTankVolume",
                                            "vacuumpump_power_kw": "TotalVacuumPower"})

        # Create dummy variables
        hzhw = pd.get_dummies(data_mdl['hotwash_freq'])+1
        hzhw = hzhw.rename(columns={"once a day": "OAD", "once a month": "OAM", "once a week": "OAW",
                                    "once every two days": "E2ndD"})
        milkpump = pd.get_dummies(data_mdl['milkpump_type'])+1
        # milkpump.columns = milkpump.columns.str.lower()
        PHE = pd.get_dummies(data_mdl['coolingsystem_platecooler'])+1 #yes ==2
        PHE = PHE.rename(columns={"yes": "GWPHE", "Yes": "GWPHE"})
        DXIB = pd.get_dummies(data_mdl['coolingsystem_directexpansion']) + 1  # DX=1
        DXIB = DXIB.rename(columns={"no": "IBDX", "No": "IBDX"})
        ICWPHE = pd.get_dummies(data_mdl['coolingsystem_waterchillingunit']) + 1  # yes ==2
        ICWPHE = ICWPHE.rename(columns={"yes": "ICWPHE", "Yes": "ICWPHE"})
        VSD = pd.get_dummies(data_mdl['VSD']) + 1  # yes ==2
        VSD = VSD.rename(columns={"yes": "Parlour_VacuumPump1_VariableSpeedY_N", "Yes": "Parlour_VacuumPump1_VariableSpeedY_N"})
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

        if 'OAM' not in hzhw:
            hzhw['OAM'] = np.ones(len(hzhw))

        # if 'diaphragm', 'doublediaphragm','highspeed','variablespeedpump' is not in milkpump then add column of ones
        if 'Diaphragm' not in milkpump:
            milkpump['Diaphragm'] = np.ones(len(milkpump))

        if 'Double Diaphragm' not in milkpump:
            milkpump['Double Diaphragm'] = np.ones(len(milkpump))

        if 'High Speed' not in milkpump:
            milkpump['High Speed'] = np.ones(len(milkpump))

        if 'Single Speed' not in milkpump:
            milkpump['Single Speed'] = np.ones(len(milkpump))

        if 'Variable Speed Pump' not in milkpump:
            milkpump['Variable Speed Pump'] = np.ones(len(milkpump))

        # Create datasets for total, cooling. vacuum water heating and combined
        df = pd.concat([data_mdl, hzhw[['OAD', "OAM", "OAW", "E2ndD"]],
                        milkpump[['Diaphragm','High Speed','Double Diaphragm','Single Speed', 'Variable Speed Pump']],
                        PHE['GWPHE'], DXIB['IBDX'], ICWPHE['ICWPHE'], VSD['Parlour_VacuumPump1_VariableSpeedY_N'],
                        ElectricAndOil["ElectricAndOil"], Electric["Electric"], Dwelling["Dwelling"], Milking["Milking"]], axis=1)
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(' ', '')

        # Create datasets for each dependent variable, with required vars in correct order.
        # total_vars = ['farm_id', 'month', 'dairycows_milking', 'dairycows_total', 'milkyield','ibdx', 'gwphe', 'icwphe', 'totalbulktankvolume', 'parlour_vacuumpump1_variablespeedy_n', 'oad', 'oam', 'oaw', 'parlour_solarthermaly_n', 'totalwaterheatervolume','totalwaterheaterpower', 'electricandoil', 'diaphragm', 'doublediaphragm','highspeed','variablespeedpump','dwelling','milking']
        # total_vars = ['farm_id', 'month', 'dairycows_total', 'milkyield','noofparlourunits', 'totalbulktankvolume', 'totalvacuumpower', 'oad', 'oam', 'totalwaterheatervolume','totalwaterheaterpower', 'diaphragm', 'parlour_vacuumpump1_variablespeedy_n','milking']
        total_vars = ['farm_id', 'Month', 'DairyCows_Total', 'MilkYield','NoOfParlourUnits','IBDX', 'GWPHE', 'TotalBulkTankVolume', 'Parlour_VacuumPump1_VariableSpeedY_N','E2ndD', 'OAD', 'OAM', 'TotalWaterHeaterVolume','TotalWaterHeaterPower', 'singlespeed', 'variablespeedpump','milking']

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

    def predict_total(self, data, wandb): # predict total kWh consumption
        # data = total_db.iloc[0, 1:14]
        # wandb = wandb_total

        # transform data as per data used for model training
        # data["dairycows_milking"] = np.sqrt(data["dairycows_milking"])
        # data = total_db
        # wandb=wandb_total
        data["dairycows_total"] = np.log(data["dairycows_total"])
        data["milkyield"] = np.sqrt(data["milkyield"])
        data["noofparlourunits"] = np.log(data["noofparlourunits"])
        data["totalbulktankvolume"] = np.log(data["totalbulktankvolume"])
        data["totalwaterheatervolume"] = np.reciprocal(data["totalwaterheatervolume"])
        data["totalwaterheaterpower"] = np.sqrt(data["totalwaterheaterpower"])
        #data["totalvacuumpower"] = np.log(data["totalvacuumpower"])

        # Normalize according to data used for model training
        minmax = wandb.iloc[wandb.shape[0]-2:wandb.shape[0], 1:wandb.shape[1]-3]
        data_std = pd.DataFrame(2 * np.subtract(data, minmax.iloc[0].values.tolist()) / np.subtract(minmax.iloc[1].values.tolist(), minmax.iloc[0].values.tolist()) -1)
        # wandbtotal = pd.to_pickle(wandb, 'wandbtotal.pkl')
        # wandbtotal = pd.read_pickle('wandbtotal.pkl')

        # Model weights and biases
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

        # Calculate predictions
        inputxweights = np.multiply(weights.to_numpy(), input_trans_minmax)
        hiddensum = inputxweights.sum(axis=1)
        transfcnplusbias = np.tanh(hiddensum + innerbias)
        TFBplusbias = transfcnplusbias * outerlayerbias
        outerlayersum = sum(TFBplusbias)
        outerlayersumTF = np.tanh(outerlayersum + outerbias)

        predictionvalue = (((outerlayersumTF + 1) * (maxkWh - minkWh)) / 2) + minkWh

        return predictionvalue

    def predict_cooling(self, data, wandb): # predicting cooling kWh
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

    def predict_vacuum(self, data, wandb): # predicting vacuum kWh
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

    def predict_heating(self, data, wandb): # predicting water heating kWh
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

    def predict_combined(self, data, wandb): # predicting combined kWh
        # data = combined_db.iloc[0, 1:22]
        # wandb = pd.read_csv('wandbcooling.csv')
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
    def on_filterButtonLoad_clicked(self): # action when filter button clicked

        if hasattr(self, "tvdatabase"):

            current_tv = self.tvdatabase # annual
            current_charts = self.importedfile # monthly

            #farm size
            minsize = self.slider1.value()[0]
            maxsize = self.slider1.value()[1]

            #VSD
            if self.VSD_yes.isChecked():
                current_tv = current_tv.loc[(current_tv['VSD'] == "yes")]
            elif self.VSD_no.isChecked():
                current_tv = current_tv.loc[(current_tv['VSD'] == "no")]

            #PHE
            if self.PHE_yes.isChecked():
                current_tv = current_tv.loc[(current_tv['coolingsystem_platecooler'] == "yes")]
            elif self.PHE_no.isChecked():
                current_tv = current_tv.loc[(current_tv['coolingsystem_platecooler'] == "no")]

            #Cooling System
            if self.cs_DX.isChecked():
                current_tv = current_tv.loc[(current_tv['coolingsystem_directexpansion'] == "yes")]
            elif self.cs_IB.isChecked():
                current_tv = current_tv.loc[(current_tv['coolingsystem_icebank'] == "yes")]

            # DER
            der_logical = [self.der_a.isChecked(), self.der_b.isChecked(), self.der_c.isChecked(), self.der_d.isChecked(), self.der_e.isChecked()]
            DER_selected = np.array(["A", "B", "C", "D", "E"])[np.array(der_logical)]
            current_tv = current_tv[(current_tv['DER'].isin(DER_selected))]

            # Filter treeview database based on slider chart values
            current_tv = current_tv.loc[(current_tv['herd_size'] >= minsize) & (current_tv['herd_size'] <= maxsize)]
            current_charts = current_charts.loc[current_charts['farm_id'].isin(current_tv["farm_id"])]

            if len(current_tv) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Filter Data")
                msg.setText("No farms available with current parameters.")
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()

                # Change filtering buttons to original (as per tvdatabase)
                self.slider1.setValue((self.cursel_minsize, self.cursel_maxsize))
                self.__dict__[f"VSD_{self.cursel_vsd}"].setChecked(True)
                self.__dict__[f"PHE_{self.cursel_phe}"].setChecked(True)
                self.__dict__[f"cs_{self.cursel_cs}"].setChecked(True)
                self.der_a.setChecked(self.der[0])
                self.der_b.setChecked(self.der[1])
                self.der_c.setChecked(self.der[2])
                self.der_d.setChecked(self.der[3])
                self.der_e.setChecked(self.der[4])
                return

            if current_charts is None:
                return

            # difference from mean of subset
            current_tv["wh_lm"] = round(current_tv["wh_lm"], 2)
            current_tv["subset_diff_%"] = round((current_tv["wh_lm"] - statistics.mean(current_tv["wh_lm"])) / statistics.mean(current_tv["wh_lm"]) * 100, 2)


            # Macro-level section layout
            self.firstTab.MRChart(current_tv) # Top left
            self.firstTab.BLChart(current_charts) # Top right
            self.firstTab.energychart(current_charts, current_tv) # Bottom left
            current_tv_removed = current_tv.drop(["TotalKWh", "wh_lm", "global_diff_%", "subset_diff_%", "pv_kwh"], axis=1)
            self.model = PandasModel(current_tv_removed)
            self.tableView.setModel(self.model)
            self.filtereddatabase_ann = current_tv
            self.filtereddatabase_mth = current_charts

            self.mdl = self.firstTab.kpi_table(self.filtereddatabase_ann)
            self.firstTab.tableViewkpi.setModel(self.mdl)

            # cookies (to return back to if no data available)
            self.cursel_minsize = self.slider1.value()[0]
            self.cursel_maxsize = self.slider1.value()[1]

            # VSD
            if self.VSD_yes.isChecked():
                self.cursel_vsd = "yes"
            elif self.VSD_no.isChecked():
                self.cursel_vsd = "no"
            elif self.VSD_all.isChecked():
                self.cursel_vsd = "all"

            # #PHE
            if self.PHE_yes.isChecked():
                self.cursel_phe = "yes"
            elif self.PHE_no.isChecked():
                self.cursel_phe = "no"
            elif self.PHE_all.isChecked():
                self.cursel_phe = "all"

            # #Cooling System
            if self.cs_DX.isChecked():
                self.cursel_cs = "DX"
            elif self.cs_IB.isChecked():
                self.cursel_cs = "IB"
            elif self.cs_all.isChecked():
                self.cursel_cs = "all"

            # DER
            self.der = [self.der_a.isChecked(), self.der_b.isChecked(), self.der_c.isChecked(),
                           self.der_d.isChecked(), self.der_e.isChecked()]


        else:
            msg = QMessageBox()
            msg.setWindowTitle("Import Data")
            msg.setText("Please import data before filtering.")
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

class FirstTab(QWidget): # macro-level tab layout
    def __init__(self, tabwidget):
        super(FirstTab, self).__init__()
        # define instance
        self.tabwidget = tabwidget
        self.data = tabwidget.data
        self.filtereddatabase = []
        self.filtereddatabase_ann = []

        # Bottom right
        bottomright = QGridLayout()
        bottomright.addWidget(self.kpi(self.filtereddatabase_ann), 0, 0, 1, 1)
        bottomright.addWidget(self.info(self.data), 1, 0, 2, 1)

        # Grid layout of entire tab
        layout = QGridLayout()
        layout.addWidget(self.infrastructure(self.data), 0, 0) # top left
        layout.addWidget(self.energy(), 0, 1) # top right
        layout.addWidget(self.energymonth(), 1, 0) # bottom left
        layout.addLayout(bottomright, 1, 1) # bottom right
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        self.setLayout(layout)

    def info(self, data):  # Terms and conditions section
        groupBox = QGroupBox("Terms + Conditions")
        label = QTextEdit()
        label.setFrameStyle(0)
        label.setReadOnly(True)
        label.textCursor().insertHtml("The National Artificial Intelligent Dairy Energy Application (NAIDEA) was developed and is maintained by researchers in the MeSSO research group at the Munster Technological University (messo.cit.ie). NAIDEA is not for use by commercial bodies. Contact messo@mtu.ie for further information.")

        ExLayout = QVBoxLayout()
        ExLayout.addWidget(label)

        groupBox.setLayout(ExLayout)
        groupBox.setFlat(True)

        return groupBox

    def kpi_table(self, data): # KPI table bottom right

        try:
            val = len(data) # number of farms
            if val == 0:
                self.modelkpi.setItem(0, 0, QStandardItem(str("")))
            else:
                self.modelkpi.setItem(0, 0, QStandardItem(str(f'{round(val):,}')))
        except:
            self.modelkpi.setItem(0, 0, QStandardItem(str("")))

        try:
            val = np.mean(data["TotalKWh"]) # mean kWh use per farm
            if val == 0:
                self.modelkpi.setItem(0, 1, QStandardItem(str("")))
            else:
                self.modelkpi.setItem(0, 1, QStandardItem(str(f'{round(val):,}')))
        except:
            self.modelkpi.setItem(0, 1, QStandardItem(str("")))

        try:
            val = sum(data["TotalKWh"]) / sum(data["milk_yield_litres"]) * 1000 # mean Wh/Lm
            self.modelkpi.setItem(0, 2, QStandardItem(str(round(val, 1))))
        except:
            self.modelkpi.setItem(0, 2, QStandardItem(str("")))

        try:
            val = data["TotalKWh"] / data["herd_size"]
            val = val.mean() # mean kWh / cow
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
            self.modelkpi.setItem(0, 4, QStandardItem(DER)) # mean DER
        except:
            self.modelkpi.setItem(0, 4, QStandardItem(str("")))

        try:
            val = np.mean(data["TotalKWh"])*float(self.tabwidget.inptbox.text())/1000 # kg CO2 / farm
            if val == 0:
                self.modelkpi.setItem(0, 5, QStandardItem(str("")))
            else:
                self.modelkpi.setItem(0, 5, QStandardItem(str(f'{round(val):,}')))
        except:
            self.modelkpi.setItem(0, 5, QStandardItem(str("")))

        return self.modelkpi

    def kpi(self, data): # key performance indicator table
        qss = """
        {border: none;}
        """
        groupBoxkpi = QGroupBox("Key Performance Indicators")

        # Define KPI table
        self.modelkpi = QtGui.QStandardItemModel(self)
        self.modelkpi.setRowCount(1)
        self.modelkpi.setColumnCount(6)
        self.tableViewkpi = QtWidgets.QTableView(self)
        self.tableViewkpi.setFixedHeight(62) # height of available space
        self.tableViewkpi.setShowGrid(False) # removes horizontal lines
        self.tableViewkpi.setFrameStyle(0)
        self.tableViewkpi.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableViewkpi.setObjectName("tableViewkpi")
        self.tableViewkpi.verticalHeader().hide()

        # Table headings
        self.modelkpi.setHeaderData(0, Qt.Horizontal, "No. of Farms")
        self.modelkpi.setHeaderData(1, Qt.Horizontal, "kWh / Farm")
        self.modelkpi.setHeaderData(2, Qt.Horizontal, "Wh / Lm")
        self.modelkpi.setHeaderData(3, Qt.Horizontal, "kWh / Cow")
        self.modelkpi.setHeaderData(4, Qt.Horizontal, "Average DER")
        self.modelkpi.setHeaderData(5, Qt.Horizontal, "kg CO\u2082 / Farm")

        # Align text in tableview
        for item in range(0, 6):
            self.tableViewkpi.setItemDelegateForColumn(item, AlignDelegate(self.kpi_table(data)))

        self.tableViewkpi.setModel(self.kpi_table(data))

        layout = QHBoxLayout()
        layout.addWidget(self.tableViewkpi)

        groupBoxkpi.setLayout(layout)
        groupBoxkpi.setFlat(True)

        return groupBoxkpi

    def MRChart(self, importedfile): # pie chart (Top left)
        # https://pythonbasics.org/pyqt-radiobutton/
        if self.radioButton1.isChecked(): # pie chart changes depending upon which radio button is checked
            importedfile = importedfile.sort_values(by=[self.radioButton1.label], ascending=True)
            fig = go.Pie(labels=importedfile[self.radioButton1.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>", sort=False)
            layout = go.Layout(autosize=True, legend=dict(orientation="h", xanchor='center', x=0.5))
        elif self.radioButton2.isChecked():
            importedfile = importedfile.sort_values(by=[self.radioButton2.label], ascending=True)
            fig = go.Pie(labels=importedfile[self.radioButton2.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>", sort=False)
            layout = go.Layout(autosize=True, legend=dict(orientation="h", xanchor='center', x=0.5))
        elif self.radioButton3.isChecked():
            importedfile = importedfile.sort_values(by=[self.radioButton3.label], ascending=True)
            fig = go.Pie(labels=importedfile[self.radioButton3.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>", sort=False)
            layout = go.Layout(autosize=True, legend=dict(orientation="h", xanchor='center', x=0.5))
        elif self.radioButton4.isChecked():
            importedfile = importedfile.sort_values(by=[self.radioButton4.label], ascending=True)
            fig = go.Pie(labels=importedfile[self.radioButton4.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>", sort=False)
            layout = go.Layout(autosize=True, legend=dict(orientation="h", xanchor='center', x=0.5))
        elif self.radioButton11.isChecked():
            importedfile = importedfile.sort_values(by=[self.radioButton11.label], ascending=True)
            fig = go.Pie(labels=importedfile[self.radioButton11.label],  hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>", sort=False)
            layout = go.Layout(autosize=True)

        fig = go.Figure(data=fig, layout=layout)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def _on_downloaFunc(self, download): # save image function
        # save_file_name_dialog is a function to show the windows file window
        option = QFileDialog.Options()
        image_path, _ = QFileDialog.getSaveFileName(self, 'Save file',
                                            CURRENT_DIR, "Png files (*.png)", options=option)
        if image_path:
            download.setPath(image_path)
            download.accept()

    def infrastructure(self, importedfile): # Plot infrastructural breakdown pie charts
        groupBox = QGroupBox("Infrastructure Breakdown")

        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.page().profile().downloadRequested.connect(self._on_downloaFunc)
        right = QVBoxLayout()

        # Low-energy lighting
        self.radioButton1 = QRadioButton("Low-Energy Lighting")
        self.radioButton1.label = "low_energy_lighting"
        self.radioButton1.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton1)

        # Green Electricity
        self.radioButton2 = QRadioButton("Green Electricity")
        self.radioButton2.setChecked(True)
        self.radioButton2.label = "green_electricity"
        self.radioButton2.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton2)

        # VSD
        self.radioButton3 = QRadioButton("Variable Speed Drive")
        self.radioButton3.label = "VSD"
        self.radioButton3.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton3)

        # PHE
        self.radioButton4 = QRadioButton("Plate Cooler")
        self.radioButton4.label = "coolingsystem_platecooler"
        self.radioButton4.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton4)

        # Renewable Energy
        self.radioButton11 = QRadioButton("Renewable Energy")
        self.radioButton11.label = "retech"
        self.radioButton11.toggled.connect(lambda: self.MRChart(self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton11)

        middleright = QHBoxLayout()
        middleright.addWidget(self.browser, 3)
        middleright.addLayout(right, 1)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)

        return groupBox

    def energychart(self, importedfile, ann_file): # Pie charts for top right

        kwhdata = importedfile[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]]
        if self.radioButton5.isChecked(): # Changes depending on radio button checked
            kwhdata = importedfile[["CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]]
            summed = round(kwhdata.sum(axis=0))
            fig = go.Pie(labels=["Milk Cooling", "Milk Harvesting", "Water Heating", "Other Use"], values=summed.values,  hovertemplate = "%{label}: <br>Sum: %{value} kWh <extra></extra>", sort=False)
        elif self.radioButton6.isChecked():
            derdata = ann_file[["farm_id", "DER"]]
            derdata = derdata.sort_values(by=['DER'], ascending=True)
            fig = go.Pie(labels=derdata["DER"], hovertemplate = "%{label}: <br>No. Farms: %{value} <extra></extra>", sort=False)
        elif self.radioButton7.isChecked():
            summed = round(kwhdata.sum(axis=0)*float(self.tabwidget.inptbox.text())/1000) #0.296
            fig = go.Pie(labels=["Milk Cooling", "Milk Harvesting", "Water Heating", "Other Use"], values=summed.values,  hovertemplate = "%{label}: <br>Sum: %{value} kg CO\u2082 <extra></extra>", sort=False)

        layout = go.Layout(autosize=True, legend=dict(orientation="h",xanchor='center', x=0.5))
        fig = go.Figure(data=fig, layout=layout)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        self.browserEn.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def energy(self): # Energy/Carbon section
        groupBox = QGroupBox("Energy/Carbon Breakdown")

        right = QVBoxLayout()

        # Energy
        self.radioButton5 = QRadioButton("Energy Breakdown")
        self.radioButton5.toggled.connect(lambda: self.energychart(self.tabwidget.filtereddatabase_mth, self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton5)

        # DER
        self.radioButton6 = QRadioButton("Dairy Energy Rating")
        self.radioButton6.setChecked(True)
        self.radioButton6.toggled.connect(lambda: self.energychart(self.tabwidget.filtereddatabase_mth, self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton6)

        # CO2
        self.radioButton7 = QRadioButton("Carbon Dioxide")
        self.radioButton7.toggled.connect(lambda: self.energychart(self.tabwidget.filtereddatabase_mth, self.tabwidget.filtereddatabase_ann))
        right.addWidget(self.radioButton7)

        self.browserEn = QtWebEngineWidgets.QWebEngineView(self)
        middleright = QHBoxLayout()
        middleright.addWidget(self.browserEn, 3)
        middleright.addLayout(right, 1)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)

        return groupBox

    def BLChart(self, importedfile): # Stacke dbar chart bottom left

        smonth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        if self.radioButton8.isChecked():# total
            kwhdata = importedfile[["month", "CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]].groupby("month",
                                                                                                             as_index=False).mean()
            y_axislabel = "Electricity Use\n(kWh)"
            hovertext = "%{x}: <br>%{y} kWh <extra></extra>"
            fig = go.Figure(data=[go.Bar(name='Milk Cooling', x=smonth, y=round(kwhdata["CoolingKWh"], 1)),
                                  go.Bar(name='Milk Harvesting', x=smonth, y=round(kwhdata["VacuumKWh"], 1)),
                                  go.Bar(name='Water Heating', x=smonth, y=round(kwhdata["WaterHeatKWh"], 1)),
                                  go.Bar(name='Other Use', x=smonth, y=round(kwhdata["OtherKWh"], 1))])
            fig.update_layout(legend=dict(orientation="h", xanchor='center', x=0.5))

        elif self.radioButton9.isChecked(): # total / litre milk
            kwhdata_perlitre = importedfile[["month", "milk_yield_litres", "CoolingKWh", "VacuumKWh", "WaterHeatKWh", "OtherKWh"]].groupby("month", as_index = False).mean()
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
            # ,
            #                       go.Bar(name='Other Use', x=smonth, y=round(kwhdata["OtherKWh"], 1))])


        fig.update_traces(hovertemplate=hovertext)
        fig.update_layout(barmode='stack',
                        legend=dict(orientation="h", xanchor='center', x=0.5), margin=dict(t=0, b=0, l=0, r=0))
        fig.update_layout(legend={'traceorder':'normal'})

        fig.update_yaxes(title=y_axislabel, title_font_size=10)
        self.browserBL.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def energymonth(self): # monthly energy stats bar chart section
        groupBox = QGroupBox("Monthly Energy Statistics")

        right = QVBoxLayout()

        # Electricity use
        self.radioButton8 = QRadioButton("Electricity Use")
        self.radioButton8.setChecked(True)
        self.radioButton8.toggled.connect(lambda: self.BLChart(self.tabwidget.filtereddatabase_mth))
        right.addWidget(self.radioButton8)

        # Wh/Lm
        self.radioButton9 = QRadioButton("Electricity Use / Litre")
        self.radioButton9.toggled.connect(lambda: self.BLChart(self.tabwidget.filtereddatabase_mth))
        right.addWidget(self.radioButton9)

        # kWh / cow
        self.radioButton10 = QRadioButton("Electricity Use / Cow")
        self.radioButton10.toggled.connect(lambda: self.BLChart(self.tabwidget.filtereddatabase_mth))
        right.addWidget(self.radioButton10)

        self.browserBL = QtWebEngineWidgets.QWebEngineView(self)
        middleright = QHBoxLayout()
        middleright.addWidget(self.browserBL, 3)
        middleright.addLayout(right, 1)
        groupBox.setLayout(middleright)
        groupBox.setFlat(True)

        return groupBox

class ThirdTab(QWidget): # Help section (Showing user manual)
    def __init__(self):
        super().__init__()

        groupBox = QGroupBox("Help Section")

        view = QtWebEngineWidgets.QWebEngineView()
        settings = view.settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        url = QtCore.QUrl.fromLocalFile(os.path.join(CURRENT_DIR, "NAIDEA User Manual.pdf"))
        view.load(url)
        view.resize(640, 480)
        view.show()

        #create layout
        layout = QVBoxLayout(self)
        layout.addWidget(view)

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
    appctxt = ApplicationContext()
    appctxt.app.setStyle('Breeze')
    window = mainwindow(data=None)
    # Formatting
    window.showMaximized()
    window.setWindowTitle("NAIDEA")
    window.setWindowIcon(QIcon('icon.ico'))
    sys.exit(appctxt.app.exec())