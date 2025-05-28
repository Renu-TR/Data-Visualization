# -*- coding: utf-8 -*-
"""
All health indicators for India 1960 to 2024
Author: Renu
"""
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Line chart
def save_line_chart(df, x_label, y_label, title, filename, output_folder):
    # Plotting the line chart
    ax = df.plot(kind="line", marker='.')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.title(title)
    # Save the plot to a file
    plt.savefig(os.path.join(output_folder, filename), bbox_inches='tight')
    plt.close()


# Bar chart
def save_bar_chart(ax, x_label, y_label, title, xticks, filename, output_folder):
    # Add labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(xticks)
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    # Save the plot to a file
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, filename))
    plt.close()


if __name__ == "__main__":
    # creating directory to store the visualizations
    out = "./visualizations"
    if not os.path.exists(out):
        os.makedirs(out)

    # reading and filtering the dataset
    columns = ['GHO (CODE)', 'YEAR (DISPLAY)', 'DIMENSION (TYPE)', 'DIMENSION (CODE)', 'DIMENSION (NAME)', 'Numeric']
    data = pd.read_csv("health_indicators_ind.csv")
    data = data.loc[1:, columns]
    data['YEAR (DISPLAY)'] = data['YEAR (DISPLAY)'].astype('int')
    data['Numeric'] = data['Numeric'].astype('float')
    data.sort_values(by=['YEAR (DISPLAY)'], inplace=True)
    data = data.drop_duplicates()

    # obesity and physical inactivity charts
    # Prevelance of obesity among adults
    df_obesity_among_adults = data[data['GHO (CODE)'] == 'NCD_BMI_30C']
    df_obesity_among_adults = df_obesity_among_adults[["YEAR (DISPLAY)", "DIMENSION (CODE)", "Numeric"]]
    df_obesity_among_adults = df_obesity_among_adults.groupby(by=["YEAR (DISPLAY)", "DIMENSION (CODE)"])["Numeric"].mean().unstack()
    save_line_chart(df_obesity_among_adults, "YEAR", "PERCENTAGE OF OBESITY", "OBESITY", "obesity.png", out)

    # % Insufficient physical activity
    df_physical_activity = data[data['GHO (CODE)']=='NCD_PAC']
    df_physical_activity = df_physical_activity[["YEAR (DISPLAY)", "DIMENSION (CODE)", "Numeric"]]
    df_physical_activity = df_physical_activity.groupby(by=["YEAR (DISPLAY)", "DIMENSION (CODE)"])["Numeric"].mean().unstack()
    save_line_chart(df_physical_activity, "YEAR", "PERCENTAGE OF INACTIVITY", "INSUFFICIENT PHYSICAL ACTIVITY", "insufficient_physical_activity.png", out)

    data_merged = pd.merge(df_obesity_among_adults, df_physical_activity, on="YEAR (DISPLAY)", suffixes=("_obesity", "_activity"))
    data_merged.head()

    # Compute correlation matrix
    corr_matrix = data_merged.corr()

    # Create a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig(os.path.join(out, "correlation_matrix_obesity_vs_physical_inactivity.png"), bbox_inches='tight')

    #Cholestrol rates in adults
    df_cholestrol = data[data['GHO (CODE)'] == 'NCD_CHOL_MEANNONHDL_A']
    df_cholestrol = df_cholestrol[["YEAR (DISPLAY)", "DIMENSION (CODE)", "Numeric"]]
    df_cholestrol = df_cholestrol.groupby(by=["YEAR (DISPLAY)", "DIMENSION (CODE)"])["Numeric"].mean().unstack()
    df_cholestrol = df_cholestrol.reset_index()

    # Plotting the  bar chart
    years = df_cholestrol['YEAR (DISPLAY)']
    width = 0.35  # Width of the bars

    fig, ax = plt.subplots(figsize=(20, 8))

    # Plot stacked bars
    ax.bar(years - width/2, df_cholestrol['SEX_FMLE'], width, label='FEMALE CHOLESTROL LEVELS', color='lightblue')
    ax.bar(years + width/2, df_cholestrol['SEX_MLE'], width, label='MALE CHOLESTROL LEVELS', color='lightgreen')
    save_bar_chart(ax, "YEAR", "MEAN OF NON-HDL CHOLESTROL LEVELS", "NON HDL CHOLESTROL LEVELS", years, "non_hdl_cholesterol_levels.png", out)

    #Women with Anaemia
    # Number of non-pregnant women (aged 15-49 years) with anaemia (thousands)

    NonpregnantWomen_Anemia = data.loc[(data['GHO (CODE)'] == 'NUTRITION_ANAEMIA_NONPREGNANT_NUM') & (data['DIMENSION (TYPE)']=='SEVERITY'), ["YEAR (DISPLAY)", "DIMENSION (CODE)", "Numeric"]]
    NonpregnantWomen_Anemia = NonpregnantWomen_Anemia.groupby(by=["YEAR (DISPLAY)", "DIMENSION (CODE)"])["Numeric"].mean().unstack()
    NonpregnantWomen_Anemia['SEVERITY_TOTAL'] = NonpregnantWomen_Anemia['SEVERITY_MILD'] + NonpregnantWomen_Anemia['SEVERITY_MODERATE'] +  NonpregnantWomen_Anemia['SEVERITY_SEVERE']
    save_line_chart(NonpregnantWomen_Anemia, "YEAR", "NUMBER OF ANAEMIC CASES", "NUMBER OF ANAEMIC CASES IN NON-PREGNANT WOMEN", "NonpregnantWomen_Anemia.png", out)

    # Number of pregnant women (aged 15-49 years) with anaemia (thousands)

    PregnantWomen_Anemia = data.loc[(data['GHO (CODE)'] == 'NUTRITION_ANAEMIA_PREGNANT_NUM') & (data['DIMENSION (TYPE)']=='SEVERITY'), ["YEAR (DISPLAY)", "DIMENSION (CODE)", "Numeric"]]
    PregnantWomen_Anemia = PregnantWomen_Anemia.groupby(by=["YEAR (DISPLAY)", "DIMENSION (CODE)"])["Numeric"].mean().unstack()
    PregnantWomen_Anemia['SEVERITY_TOTAL'] = PregnantWomen_Anemia['SEVERITY_MILD'] + PregnantWomen_Anemia['SEVERITY_MODERATE'] +  PregnantWomen_Anemia['SEVERITY_SEVERE']
    save_line_chart(PregnantWomen_Anemia, "YEAR", "NUMBER OF ANAEMIC CASES", "NUMBER OF ANAEMIC CASES IN PREGNANT WOMEN", "pregnantWomen_Anemia.png", out)

    # anemic women dataframe
    Data_merge_Anemia = pd.merge(NonpregnantWomen_Anemia, PregnantWomen_Anemia, on='YEAR (DISPLAY)', suffixes=('_NON_PREGNANT', '_PREGNANT')).reset_index()

    # Plotting the stacked bar chart for anemic women
    years = Data_merge_Anemia['YEAR (DISPLAY)']

    # Create subplots for pregnant and non-pregnant women side by side
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot stacked bars for pregnant women
    ax.bar(years - width/2, Data_merge_Anemia['SEVERITY_SEVERE_PREGNANT'], width, label='Severe (Pregnant)', color='darkblue')
    ax.bar(years - width/2, Data_merge_Anemia['SEVERITY_MODERATE_PREGNANT'], width, bottom=Data_merge_Anemia['SEVERITY_SEVERE_PREGNANT'], label='Moderate (Pregnant)', color='blue')
    ax.bar(years - width/2, Data_merge_Anemia['SEVERITY_MILD_PREGNANT'], width, bottom=Data_merge_Anemia['SEVERITY_SEVERE_PREGNANT'] + Data_merge_Anemia['SEVERITY_MODERATE_PREGNANT'], label='Mild (Pregnant)', color='lightblue')

    # Plot stacked bars for non-pregnant women
    ax.bar(years + width/2, Data_merge_Anemia['SEVERITY_SEVERE_NON_PREGNANT'], width, label='Severe (Non-Pregnant)', color='darkred')
    ax.bar(years + width/2, Data_merge_Anemia['SEVERITY_MODERATE_NON_PREGNANT'], width, bottom=Data_merge_Anemia['SEVERITY_SEVERE_NON_PREGNANT'], label='Moderate (Non-Pregnant)', color='red')
    ax.bar(years + width/2, Data_merge_Anemia['SEVERITY_MILD_NON_PREGNANT'], width, bottom=Data_merge_Anemia['SEVERITY_SEVERE_NON_PREGNANT'] + Data_merge_Anemia['SEVERITY_MODERATE_NON_PREGNANT'], label='Mild (Non-Pregnant)', color='lightcoral')

    save_bar_chart(
        ax, 
        "YEAR", 
        "NUMBER OF ANAEMIC CASES", 
        "SEVERITY OF ANAEMIA IN PREGNANT AND NON-PREGNANT WOMEN OVER THE YEARS (2000 - 2019)", 
        years, 
        "anemia_severity_in_pregnant_and_non_pregnant_women.png", 
        out
    )

    # Number of maternal deaths
    Maternal_deaths = data.loc[data["GHO (CODE)"] == "MORT_MATERNALNUM", ['YEAR (DISPLAY)', 'Numeric']]
    Maternal_deaths.rename({"Numeric": "MATERNAL_MORTALITY_NUM"}, axis=1, inplace=True)
    ax = Maternal_deaths.set_index('YEAR (DISPLAY)').plot(kind="line", marker='*')
    ax.set_title('NUMBER OF MATERNAL DEATHS')
    ax.set_ylabel("NUMBER OF DEATH CASES")
    plt.savefig(os.path.join(out, "maternal_deaths.png"))

    # correlating maternal mortality and anemia in pregnant women
    plt.figure(figsize=(8, 6))
    df_anemia_and_maternal_mortality = pd.merge(Data_merge_Anemia, Maternal_deaths, on="YEAR (DISPLAY)")
    df_anemia_and_maternal_mortality = df_anemia_and_maternal_mortality[["YEAR (DISPLAY)", "SEVERITY_TOTAL_PREGNANT", "MATERNAL_MORTALITY_NUM"]]
    ax2 = sns.regplot(x='SEVERITY_TOTAL_PREGNANT', y='MATERNAL_MORTALITY_NUM', data=df_anemia_and_maternal_mortality, marker='o', color='b', line_kws={'color': 'red'})
    ax2.set_title('CORRELATION OF ANAEMIA IN PREGNANT WOMEN AND  MATERNAL DEATHS')
    plt.savefig(os.path.join(out, "correlation_of_anemia_in_pregnant_women_with_maternal_deaths.png"))

    # Mean hemoglobin level of pregnant women (aged 15-49 years)
    df_mean_hb_pregnant = data.loc[data['GHO (CODE)'] == 'HEMOGLOBINLEVEL_PREGNANT_MEAN', ['YEAR (DISPLAY)', 'Numeric']]
    df_mean_hb_pregnant.rename({"Numeric": "mean_hb"}, inplace=True, axis=1)

    # mean hb count in non-pregnant women
    df_mean_hb_non_pregnant = data.loc[data['GHO (CODE)'] == 'HEMOGLOBINLEVEL_NONPREGNANT_MEAN', ['YEAR (DISPLAY)', 'Numeric']]
    df_mean_hb_non_pregnant.rename({"Numeric": "mean_hb"}, inplace=True, axis=1)

    # mean bh count merged
    df_mean_hb = pd.merge(df_mean_hb_non_pregnant, df_mean_hb_pregnant, on="YEAR (DISPLAY)", suffixes=("_non_pregnant", "_pregnant"))

    # Plotting the stacked bar chart for mean hb count
    years = df_mean_hb['YEAR (DISPLAY)']

    # Create subplots for pregnant and non-pregnant women side by side
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot stacked bars for pregnant women
    ax.bar(years - width/2, df_mean_hb['mean_hb_pregnant'], width, label='mean hb count (pregnant)', color='lightblue')

    # Plot stacked bars for non-pregnant women
    ax.bar(years + width/2, df_mean_hb['mean_hb_non_pregnant'], width, label='mean hb count (Non-pregnant)', color='lightcoral')

    save_bar_chart(
        ax, 
        "YEAR", 
        "MEAN HAEMOGLOBIN COUNT", 
        "MEAN HB COUNT OF PREGNANT AND NON-PREGNANT WOMEN", 
        years, 
        "mean_hb_count_in_women.png", 
        out
    )

    print("finished exporting visualizations...")
