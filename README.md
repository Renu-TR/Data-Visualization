# All health indicators for India 1960 to 2024

This notebook intends to visualize the following india health indicators for the period 1960 to 2024 with the data available from **WHO** and derive useful insights from it.

- physical inactivity, cholesterol rates and obesity among adults
- anemia cases in pregnant and non-pregnant women and their hemoglobin levels.
- maternal mortality rates over time

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Data](#data)
- [Requirements](#requirements)
- [Installation and Usage](#installation-and-usage)

## Overview

The aim of this notebook is to:
1. **Visualize** the trend of maternal mortality, mean hemoglobin count, anemic cases in pregnant and non-pregnant women, obesity, cholestrol rates and physical inactivity among adults over time.
2. **Correlate** the severity of anemia in pregnant women with maternal deaths and obesity among adults with insufficient physical activity.

## Features

- **Stacked bar charts** comparing anemia severity in pregnant and non-pregnant women.
- **Bar charts** comparing mean Hb count in pregnant and non-pregnant women.
- **Correlation analysis** between anemia cases in pregnant women and maternal deaths.
- **Correlation matrix** between physical inactivity and obesity among adults.
- Use of **linear regression** to explore the association.
- **Visualization** of trends of different health indicators over time.

## Data



- **Obesity among Adults**: Percentage annual prevalence of obesity among adults categorized by gender (male, female, both_sex)
- **Insufficient Physical Activity among Adults**: Percentage annual prevalence of insufficient physical activity among adults categorized by gender (male, female, both_sex)
- **Non-HDL Cholesterol among Adults**: Mean non-HDL cholesterol levels among adults categorized by gender (male, female, both_sex)
-  **Anemia in Pregnant Women**: Total number of anemia cases categorized by severity (mild, severe, and moderate).
- **Anemia in Non-Pregnant Women**: For comparison, anemia severity in non-pregnant women is also visualized.
- **Haemoglobin Levels in Pregnant Women**: annual mean haemoglobin levels in pregnant women
- **Haemoglobin Levels in Non-Pregnant Women**: for comparison haemoglobin levels in non-pregnant women is also visualized.
- **Maternal Mortality**: The total number of maternal deaths recorded annually.

## Requirements

The following libraries are used in the notebook:
- `pandas`
- `matplotlib`
- `seaborn`


These libraries are pre-installed in Google Colab, so no manual installation is required unless you're running this locally.

## Installation and Usage

### Run in Google Colab
1. Open the notebook in Google Colab by clicking [this link](https://colab.research.google.com/drive/1p3lTqsMUPr9E03LGIliVWQvzYpvCDkAX?usp=sharing).
2. Copy the **health_indicators_ind.csv** file to the runtime's file system. you can drag and drop the file to desired path.
3. **Execute each cell** to run the analysis step by step. After running the module import cell, the second step (second cell in notebook) is to build the dataframe from the csv file using **`pd.read_csv()`** method in pandas. The method takes the absolute file path of the csv file as a parameter. replace it with the path to which you have uploaded the csv file.
 - ex: if you have copied the csv file to **sample_data/health_indicators_ind.csv**, then
 ```
data = pd.read_csv('sample_data/health_indicators_ind.csv')
```

4. You can **copy the notebook** to your own Google Drive by clicking "File" -> "Save a copy in Drive". You can then modify the cells to perform your own custom analysis.

### Run locally (python version 3.8)
1. A python script `all_health_indicators_for_india_1960_to_2024.py` is added to generate the various visualization locally.
2. Install the above mentioned requirements using ***pip***
```
pip install pandas matplotlib seaborn
```
2. Copy the dataset (`health_indicators_ind.csv`) to the path where the python script is being executed so as to read the csv file.
3. Run the script using terminal using the python3.8 executable in local machine
```
python all_health_indicators_for_india_1960_to_2024.py
```
4. The visualizations will be exported as ***png*** files in the `visualizations` directory.