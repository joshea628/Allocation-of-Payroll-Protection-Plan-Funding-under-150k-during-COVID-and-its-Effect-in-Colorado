import pandas as pd 
import matplotlib.pyplot as plt 
from clean_data import *

plt.style.use('fivethirtyeight')

def split_ethnicities(ethnicities):
    '''
    Splits main dataframe into separate dataframes for each ethnicity included in data

    Returns: List of dataframes
    '''
    dataframes = [df_with_counties[df_with_counties['RaceEthnicity'] == name] for name in ethnicities]
    return dataframes


def avg_loan_by_ethnicity(ethnicities, ethnicity_dfs):
    '''
    Computes average loan amount for each dataframe in inputted list.

    Returns: Dictionary of averages for each ethnicity in the form of ethnicity:average
    '''
    avg_loan = {eth:round(df['LoanAmount'].mean(),2) for eth, df in zip(ethnicities, ethnicity_dfs)}
    return avg_loan


def total_loan_by_ethnicity(ethnicities, ethnicity_dfs):
    '''
    Computes average loan amount for each dataframe in inputted list.

    Returns: Dictionary of averages for each ethnicity in the form of ethnicity:average
    '''
    total_loan = {eth:df['LoanAmount'].sum() for eth, df in zip(ethnicities, ethnicity_dfs)}
    return total_loan



def graph_average_loan_ethnicity(ethnicity_avg_loan, chart_colors, save_loc):
    '''
    Graphs the Average Loan Amount by Ethnicity

    Returns: None
    '''
    fig, ax = plt.subplots(1, figsize=(12,4), dpi=700)
    keys = ethnicity_avg_loan.keys()
    averages = ethnicity_avg_loan.values()
    bar = ax.bar(keys, averages)
    for i in range(len(ethnicity_avg_loan)):
        bar[i].set_color(chart_colors[i])
    plt.xticks(rotation=45, fontsize=12, horizontalalignment='right')
    ax.set_xlabel('Ethnicity', fontsize= 16)
    ax.set_ylabel('Average Loan Amount in $', fontsize= 16)
    ax.set_title('Average Loan Amount by Ethnicity in Colorado', fontsize=18)
    plt.savefig(save_loc, bbox_inches='tight')


def graph_total_loan_ethnicity(ethnicity_total_loan, chart_colors, save_loc):
    '''
    Graphs the total Loan Amount by Ethnicity

    Returns: None
    '''
    fig, ax = plt.subplots(1, figsize=(12,4), dpi=700)
    keys = ethnicity_total_loan.keys()
    totals = ethnicity_total_loan.values()
    bar = ax.bar(keys, totals)
    for i in range(len(ethnicity_total_loan)):
        bar[i].set_color(chart_colors[i])
    plt.xticks(rotation=45, fontsize=12, horizontalalignment='right')
    #ax.set_yscale('log') #not sure if the scaling is welcome here or not...
    ax.set_xlabel('Ethnicity', fontsize= 16)
    ax.set_ylabel('Total Loan Amount in $', fontsize= 16)
    ax.set_title('Total Loan Amount by Ethnicity in Colorado', fontsize=18)
    plt.savefig(save_loc, bbox_inches='tight')



def top_zip(ethnicity_dfs, ethnicities):
    '''
    Counts the number of loans for each Ethnicity group, sorts by top 5.

    Returns: Dictionary where Keys are the Ethnicities and values are a dataframe of top 5
    zipcodes and the count of loans from each zip.
    '''
    top_dict = {}
    for eth, df in zip(ethnicities, ethnicity_dfs):
        count_zips = df.groupby(['Zip']).count()['LoanAmount']
        sort_zip = count_zips.sort_values(ascending=False).head(5)
        top_dict[eth]= sort_zip
    return top_dict



def graph_top_zips(top_zips, chart_colors, saveloc):
    '''
    Graphs up to the top 5 zip codes for each ethnicity (not used in README)

    Returns: None
    '''
    zips = pd.DataFrame(top_zips)
    zips.fillna(0, inplace=True)
    zips['total'] = zips['White'] + zips['American Indian or Alaska Native'] + zips['Asian'] + zips['Black or African American']+ zips['Puerto Rican'] + zips['Hispanic']
    zips = pd.DataFrame(zips).sort_values('total')    
    zips.drop('total', axis=1,inplace=True)

    ax = zips.plot(kind='barh', stacked=True, color=chart_colors)
    plt.yticks(fontsize = 12)
    ax.set_xlabel('Number of Loans')
    ax.set_title('Top 5 Zip Codes for Count of Loans')
    plt.savefig(saveloc, bbox_inches='tight')


def top_county(ethnicity_dfs, ethnicities):
    '''
    Counts the number of loans for each Ethnicity group, sorts by top 5.

    Returns: Dictionary where Keys are the Ethnicities and values are a dataframe of top 5
    zipcodes and the count of loans from each zip.
    '''
    top_dict = {}
    for eth, df in zip(ethnicities, ethnicity_dfs):
        count_counties = df.groupby(['county']).count()['LoanAmount']
        sort_counties = count_counties.sort_values(ascending=False).head(5)
        top_dict[eth]= sort_counties
    return top_dict


def graph_top_counties(top_county, chart_colors, saveloc):
    counties = pd.DataFrame(top_county)
    counties.fillna(0, inplace=True)
    counties['total'] = counties['White'] + counties['American Indian or Alaska Native'] + counties['Asian'] + \
        counties['Black or African American']+ counties['Puerto Rican'] + counties['Hispanic']
    counties = pd.DataFrame(counties).sort_values('total')    
    counties.drop('total', axis=1,inplace=True)

    ax = counties.plot(kind='barh', stacked=True, color=chart_colors)
    plt.yticks(fontsize = 12)
    ax.set_xlabel('Number of Loans')
    ax.set_title('Top 5 Counties for Loans')
    plt.savefig(saveloc, bbox_inches='tight')



def top_county_sum(ethnicity_dfs, ethnicities):
    '''
    Counts the number of loans for each Ethnicity group, sorts by top 5.

    Returns: Dictionary where Keys are the Ethnicities and values are a dataframe of top 5
    zipcodes and the count of loans from each zip.
    '''
    top_dict = {}
    for eth, df in zip(ethnicities, ethnicity_dfs):
        count_counties = df.groupby(['county']).sum()['LoanAmount']
        sort_counties = count_counties.sort_values(ascending=False).head(5)
        top_dict[eth]= sort_counties
    return top_dict


def graph_demographics(total_demographics, ethnicities, saveloc):
    '''
    Graphs the total population for each ethnicity in Colorado.

    Returns: None
    '''
    fig, ax = plt.subplots(1,figsize=(12,4))
    ethnicities_dem = ethnicities[:-1]
    ethnicities_dem=np.append(ethnicities_dem, 'Other')
    plt.bar(ethnicities_dem, total_demographics, color=chart_colors)
    plt.xticks(rotation=45, fontsize=12)
    ax.set_yscale('log')
    ax.set_xlabel('Ethnicity', fontsize=16)
    ax.set_ylabel('Millions of People', fontsize=16)
    ax.set_title('Distribution of Ethnicity in Colorado', fontsize=18)
    plt.savefig(saveloc, bbox_inches='tight')


def graph_demographics_top_counties(demographics_top_8, chart_colors, saveloc):
    '''
    Graphs the demographics for each of the 8 Top Counties for Loans from the PPP

    Returns: None
    '''
    ax = demographics_top_8[['White', 'Hispanic', 'American Indian or Alaska Native', 'Asian','Black or African American','Other']].plot(kind='barh', stacked=True, color=chart_colors, figsize=(10,6))
    y_axis = ax.yaxis
    y_axis.label.set_visible(False)
    ax.set_title('Demographics of Top 8 Counties for Loans', fontsize=18)
    ax.set_xlabel('Number of People', fontsize=16)
    plt.yticks(fontsize = 14)
    plt.savefig(saveloc, bbox_inches='tight')


def graph_job_loanamount(loan_by_ethnicity, jobs_retained_by_ethnicity, avg_loan_by_ethnicity, avg_jobs_retained_by_ethnicity, chart_colors, ethnicities, saveloc):
    '''
    Graphs the Loan Amount vs Jobs Retained as a Scatter Plot, color coded for ethnicity.

    Returns: None
    '''
    fig, ax = plt.subplots(1, figsize=(10,6))

    for i in range(len(loan_by_ethnicity)):
        ax.scatter(loan_by_ethnicity[i], jobs_retained_by_ethnicity[i], color=chart_colors[i], label=ethnicities[i])
    for i in range(len(avg_loan_by_ethnicity)):
        ax.scatter(avg_loan_by_ethnicity[i],avg_jobs_retained_by_ethnicity[i],color=chart_colors[i], marker='x', linewidths=20)
    ax.set_ylabel('Jobs Retained', fontsize=16)
    ax.set_xlabel('Amount of Loan in USD', fontsize=16)
    ax.set_title('Loan Amount vs Jobs Retained by Ethnicity', fontsize=18)
    plt.ylim([0,125])
    plt.legend()
    plt.savefig(saveloc, bbox_inches='tight')



if __name__ == '__main__':
   
    #colors for bar charts
    chart_colors = ['#003f5c', '#58508d', '#bc5090', '#dd5182','#ff6361', '#ffa600']
   
   #List all unique ethnicities
    ethnicities = df_with_counties['RaceEthnicity'].unique()
    
    #unpack dataframes
    white_df, hispanic_df, am_indian_alaska_df, asian_df, black_df, puerto_rican_df = split_ethnicities(ethnicities)
    ethnicity_dfs = [white_df, hispanic_df, am_indian_alaska_df, asian_df, black_df, puerto_rican_df]

    #calculations:
    ethnicity_avg_loan = avg_loan_by_ethnicity(ethnicities, ethnicity_dfs)
    ethnicity_total_loan = total_loan_by_ethnicity(ethnicities, ethnicity_dfs)
    top_zips = top_zip(ethnicity_dfs, ethnicities)
    top_county = top_county(ethnicity_dfs, ethnicities)
    top_county_sum = top_county_sum(ethnicity_dfs, ethnicities)

    #calculate demographic population
    demographic_eth_cols = ['NH Whites','Hispanic','NH Am Indian/Native','NH Asian','NH Afr Am']
    total_demographics = [sum(demographics_18[x]) for x in demographic_eth_cols]
    other = sum(demographics_18['NH Two or more']) + sum(demographics_18['NH Native Hawaiian/other'])
    total_demographics.append(other)

    #calculate demographics for top 8 counties
    demographics_top_8 = demographics_18[(demographics_18['CTYNAME'] == 'Denver County') | (demographics_18['CTYNAME'] == 'El Paso County') |(demographics_18['CTYNAME'] == 'Jefferson County') |(demographics_18['CTYNAME'] == 'Arapahoe County') | (demographics_18['CTYNAME'] == 'Larimer County')|(demographics_18['CTYNAME'] == 'Adams County') | (demographics_18['CTYNAME'] == 'Douglas County') | (demographics_18['CTYNAME'] == 'Weld County')]
    demographics_top_8['Other'] = demographics_top_8['NH Native Hawaiian/other'] + demographics_top_8['NH Two or more']
    demographics_top_8 = demographics_top_8.set_index('CTYNAME').sort_values(['TOT_POP'],ascending=True)
    demographics_top_8 = demographics_top_8.rename(columns={'NH Whites':'White','NH Afr Am': 'Black or African American','NH Am Indian/Native':'American Indian or Alaska Native','NH Asian':'Asian'})

    #calculations for amount of loan compared to jobs retained by ethnicity
    loan_by_ethnicity = [list(x['LoanAmount'].values) for x in ethnicity_dfs_job_comparison]
    jobs_retained_by_ethnicity = [list(x['JobsRetained'].values) for x in ethnicity_dfs_job_comparison]
    avg_loan_by_ethnicity = [round(x['LoanAmount'].mean(),2) for x in ethnicity_dfs_job_comparison]
    avg_jobs_retained_by_ethnicity = [round(x['JobsRetained'].mean(),3) for x in ethnicity_dfs_job_comparison]

    #graphs
    graph_total_loan_ethnicity(ethnicity_total_loan, chart_colors, '../images/total_loan_ethnicity.png')
    graph_average_loan_ethnicity(ethnicity_avg_loan, chart_colors, '../images/avg_loan_ethnicity.png')
    graph_top_zips(top_zips, chart_colors, '../images/top_zip_loancount.png')
    graph_top_counties(top_county, chart_colors, '../images/top_county_loancount.png')
    graph_top_counties_sum(top_county_sum, chart_colors, '../images/top_county_loansum.png')
    graph_demographics(total_demographics, ethnicities, '../images/demographics.png')
    graph_demographics_top_counties(demographics_top_8, chart_colors, '../images/top_county_loancount_demographic.png')
    graph_job_loanamount(loan_by_ethnicity, jobs_retained_by_ethnicity, avg_loan_by_ethnicity, avg_jobs_retained_by_ethnicity, chart_colors, ethnicities, '../images/loan_vs_jobs_retained.png')
