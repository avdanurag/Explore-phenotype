# Explore-phenotype
The script takes multi-year, multi-replication enviorment data as input and does exploratory analyisis (histogram, box plot), calculates baisc statistcs (mean, SD, missingness) and perform imputation (save imputed phenotype)

## Requirements

Make sure you have the following libraries installed:

- pandas
- matplotlib
- seaborn
- plotly
- sys

You can install these libraries using pip:

```bash
pip3 install pandas matplotlib seaborn plotly

```

## Usage

To run the script, use the following command:

```bash
python pheno_analyisis_5.py phenotype_data.csv

```


## Features
- Exploratory Analysis: The script generates histograms and box plots to visualize the distribution of each trait by location and year.

- Missing Data Analysis: It calculates the percentage of missing values for each trait.

- Data Imputation: Missing values are imputed with the mean of the available data for each trait.

- Interactive Plots: The script creates interactive box plots and histograms using Plotly for a more in-depth analysis.

- Correlation Heatmaps: Correlation heatmaps are generated to visualize the relationship between traits for different years and locations.

- Statistical Summary: A summary of statistics, including mean, standard deviation, and missing data percentages, is saved to a CSV file.

## Output
- Plots: The script saves various plots as PDF files, including box plots with spacing between years, histograms, and correlation heatmaps.

- Interactive Plots: Interactive box plots and histograms are saved as HTML files for a more interactive exploration.

- Statistics: A CSV file containing statistical information for each trait before and after imputation is generated.

- Please note that this script is meant for exploratory analysis and data imputation. Additional statistical tests and further data analysis may be required depending on your specific research goals.
