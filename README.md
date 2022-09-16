# National Artificial Intelligent Dairy Energy Application (NAIDEA). 

![banner](https://github.com/shine10101/NAIDEA_Public/blob/20dd70a0dd116115bc7de64a71d08b9bac91fa7f/Screenshot.png)

# Introduction

NAIDEA was developed to integrate macro-level survey information collected on Ireland’s population of dairy farms with artificial neural network models developed to simulate total, milk cooling, milk harvesting and water heating electricity use using easily attainable farm details. These models were trained using monitored consumption data, milk production, stock data and infrastructural data collected over six years on 74 pasture-based dairy farms, and validated using nested cross-validation. The methodology also employed hyperparameter tuning and multiple variable selection techniques to identify the farm details that maximized prediction accuracy, that could then be collected as part of nationwide farm surveys.  

NAIADEA is a desktop application offering:

1. Import/export functionality, that allows users to import data (.csv) required for generating energy predictions using five pre-trained artificial neural network models, export the processed dataset and results including farm-level Dairy Energy Ratings as well as input a carbon intensity value (gCO2/kWh) to ensure carbon emission calculations are always up to date. 
2. Macro-level energy statistics on Ireland's population of dairy farms, that can be monitored over time to calculate the effectiveness of changes to government policy. E.g. electricity consumption per litre
3. A filtering mechanism was also incorporated to allow users to filter energy statistics according to farm size or the presence of energy technologies such as plate coolers or variable speed drives. This allows government bodies to calculate energy statistics for specific dairy farm demographics.
4. A Dairy Energy Rating for each farm, allowing farms that are using energy efficiently or inefficiently to be easily identified, allowing government bodies to then direct those dairy farms using energy inefficiently towards the existing suite of decision support tools such as the ![Agricultural Energy Optimization Platform](https://github.com/shine10101/AEOP_Public/blob/e66a3d8d044fd63433682655d39d4c55b7c971e6/README.md).

NAIDEA's targeted approach can help fast track the proliferation of energy efficient and renewable energy technologies to help offset agri-related emissions while having the added benefit of 1) reducing the electricity demand from the electrical grid, 2) increasing the penetration of renewable energy contributing to overall demand, and 3) allowing farmers to become more energy independent, thereby reducing the impact of future increases in energy prices on production costs. NAIDEA has been developed in collaboration between Munster Technological University, Bord Bia, the Sustainable Energy Authority of Ireland and Teagasc. 

# Getting Started

## Running Source File
1. Download respository files
2. Ensure resources/base are located in the same file directory as main.py
3. Run main.py

## Accessing NAIDEA

Open NAIDEA_windows.exe and follow installation guidelines (currently only available for windows systems). NAIDEA_windows.exe is available at: https://doi.org/10.5281/zenodo.6511392

## Usage Steps

Step 1. Insert current carbon intensity value. The current default value equals Ireland’s 2020 carbon intensity value of 296 kg CO2 / kWh as reported by SEAI (reference). This value can be updated at any stage by updating the figure and pressing the ‘Filter’ button.

Step 2. Import Dataset. A full description of dataset and data handling requirements and example dataset is available at below. Once a csv file is selected from the file explorer and imported to NAIDEA, all models are called, electricity consumption values calculated and farm-level DERs determined. The length of time this process takes will depends on the size of the imported file. Once finished, the macro-level statistics section will be populated with intuitive charts and the key performance indicator table.

Step 3. Select/deselect filter parameters as appropriate. The default parameters ensure all farms within the imported dataset are selected. Once the user deselects as required, the user can then press the “Filter” button to confirm and re-populate NAIDEA’s figures and tables. NAIDEA’s filter parameters can be updated and initialized at any time.

Step 4. View generated figures and tables, while toggling through different charts using the radio buttons to the right of each chart.

## NAIDEA features

### Dairy Energy Rating (DER)

A novel dairy energy rating (DER) was developed to allow NAIDEA users intuitively determine each dairy farm’s total electrical energy consumption efficiency (Watt-hour (Wh) / liter) in relation to the population mean. A DER was developed consisting of a five-point scale from A to E, whereby A represented those farms with the least electricity consumption per liter, C represented mean efficiency, and E represented the largest electricity consumption per liter category. The DER also accounted for the generation of renewable energy through a solar photovoltaic system. For each farm, the estimated annual renewable energy generation (kWh) (if any) was subtracted from the forecasted total annual electricity consumption of the dairy farm prior to determining the DER of said farm.

### Application Development

NAIDEA was developed to enable dairy stakeholders take advantage of the above ANN models and DER functionality. The development of NAIDEA was underpinned by five aims and objectives that focused on delivering a finished product that had: 1) a simple installation process, 2) an intuitive and user-friendly interface, 3) import and export functionality, 4) the ability to quantify each farm’s electrical energy use in relation to the mean, and 5) a filtering mechanism to allow end-users to customize outputs in relation to installed infrastructural equipment, farm size and DER. NAIDEA’s GUI was designed and developed using Python (version 3.8) and it’s PyQt5 (version 5.15.6) package. The GUI was packaged as a standalone application using ![fman](https://build-system.fman.io/), a powerful package for deploying PyQt5 based desktop applications. For demonstrative purposes, a dummy database was constructed to present NAIDEA’s functionality.

