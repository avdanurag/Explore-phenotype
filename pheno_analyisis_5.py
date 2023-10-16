#### The script takes multi-year, multi-replication enviorment data as input and does exploratory analyisis (histogram, box plot), calculates baisc statistcs (mean, SD, missingness) and perform imputation (save imputed phenotype)    

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import sys

# Check if the input file is provided as an argument
if len(sys.argv) < 2:
    print("Usage: python script_name.py input_file.csv")
    sys.exit(1)

input_file = sys.argv[1]

# Read the phenotype data from the provided CSV file
data = pd.read_csv(input_file)

# Read the phenotype data from a CSV file
#data = pd.read_csv('phenotype_data.csv')

# Calculate the percentage of missing values for each trait
missing_percentages = data.iloc[:, 5:].isnull().mean() * 100

# Impute missing values with mean
data_imputed = data.copy()
data_imputed.iloc[:, 5:] = data_imputed.iloc[:, 5:].fillna(data_imputed.iloc[:, 5:].mean())

# Set up seaborn theme
sns.set(style="whitegrid")
sns.set_palette("husl")

# Create a directory to save the plots
if not os.path.exists('plots'):
    os.makedirs('plots')

# Save each box plot as a separate PDF page with spacing between years
traits = data.columns[5:]
for trait in traits:
    pdf_filename = f'plots/{trait}_box_plot.pdf'
    with plt.style.context("seaborn-whitegrid"):
        pdf = plt.figure(figsize=(8, 6))
        sns.boxplot(data=data_imputed, x='Loc', y=trait, hue='Year', palette="husl", width=0.5)  # Adjust width here
        plt.title(f'{trait} Distribution by Location and Year')
        plt.xlabel('Location')
        plt.ylabel(trait)
        plt.legend(title='Year', loc='upper left', bbox_to_anchor=(1, 1))
        plt.subplots_adjust(wspace=1)  # Add spacing between years
        pdf.savefig(pdf_filename, format='pdf', bbox_inches='tight')
        plt.close()

print("Box plots with spacing between years saved as separate PDF files.")

# Create interactive plots using Plotly
for trait in traits:
    fig = px.box(data_imputed, x='Loc', y=trait, color='Year', title=f'{trait} Distribution by Location and Year')
    fig.update_layout(autosize=False, width=800, height=600)
    plot_filename = f'plots/{trait}_box_plot.html'
    fig.write_html(plot_filename)
    
# Create separate histograms for each year-location combination
for trait in traits:
    for year in data_imputed['Year'].unique():
        for loc in data_imputed['Loc'].unique():
            trait_data = data_imputed[(data_imputed['Year'] == year) & (data_imputed['Loc'] == loc)][trait]
            plt.figure(figsize=(8, 6))
            plt.hist(trait_data, bins=15, alpha=1)
            plt.title(f'{trait} Distribution for Year {year}, Loc {loc}')
            plt.xlabel(trait)
            plt.ylabel('Frequency')
            plt.savefig(f'plots/{trait}_histograms_year_{year}_loc_{loc}.png', format='png', bbox_inches='tight')
            plt.close()

print("Histograms saved.")


import plotly.express as px

# Create separate interactive histograms for each year-location combination
for trait in traits:
    for year in data_imputed['Year'].unique():
        for loc in data_imputed['Loc'].unique():
            trait_data = data_imputed[(data_imputed['Year'] == year) & (data_imputed['Loc'] == loc)][trait]
            fig = px.histogram(trait_data, title=f'{trait} Distribution for Year {year}, Loc {loc}', labels={trait: trait, 'count': 'Frequency'})
            fig.update_layout(bargap=0.1)  # Adjust spacing between bars
            plot_filename = f'plots/{trait}_histogram_interactive_year_{year}_loc_{loc}.html'
            fig.write_html(plot_filename)

print("Interactive histograms saved.")



# Create correlation heatmaps for different years and locations for each trait
for trait in traits:
    corr_data = data_imputed.pivot_table(index=['Year', 'Loc'], values=trait, aggfunc='mean').reset_index()
    corr_matrix = corr_data.pivot(index='Loc', columns='Year', values=trait).corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(f'Correlation Heatmap for {trait}')
    plt.savefig(f'plots/{trait}_correlation_heatmap.pdf', format='pdf', bbox_inches='tight')
    plt.close()

# Calculate Mean, SD, and missing data for each trait before and after imputation
traits_stats = pd.DataFrame()
traits_stats['Trait'] = traits
traits_stats['Mean Before Imputation'] = data.iloc[:, 5:].mean().values
traits_stats['SD Before Imputation'] = data.iloc[:, 5:].std().values
traits_stats['Missing % Before Imputation'] = missing_percentages.values
traits_stats['Mean After Imputation'] = data_imputed.iloc[:, 5:].mean().values
traits_stats['SD After Imputation'] = data_imputed.iloc[:, 5:].std().values
traits_stats['Missing % After Imputation'] = data_imputed.iloc[:, 5:].isnull().mean().values

# Save calculated statistics to a CSV file
traits_stats.to_csv('traits_statistics.csv', index=False)
print("Trait statistics saved to CSV file.")
