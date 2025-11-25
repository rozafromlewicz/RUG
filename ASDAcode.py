import pandas as pd 
import os

#NEIGHBORHOOD SOCIOECONOMIC VALUE DETERMINATION 

file_path= os.path.join ('C:' , 'asdaproject', 'vscodeproject', 'burtwijksocioecon_clean.csv')

df = pd.read_csv('burtwijksocioecon_clean.csv')

df = df.transpose()

new_header = df.iloc[0]  
df = df[1:]
df.columns = new_header

df.reset_index(inplace=True, drop=True)

df.replace(['.', '#VALUE!'], pd.NA, inplace=True)

df['owner_occupied_homes'] = pd.to_numeric(df['owner_occupied_homes'], errors='coerce')
df['labor_participation'] = pd.to_numeric(df['labor_participation'], errors='coerce')
df['low_income_households'] = pd.to_numeric(df['low_income_households'], errors='coerce')
df['households_social_minimum'] = pd.to_numeric(df['households_social_minimum'], errors='coerce')
df['income_per_house'] = pd.to_numeric(df['income_per_house'], errors='coerce')
df['higher_education_percent'] = pd.to_numeric(df['higher_education_percent'], errors='coerce')
df['social_aid_percent'] = pd.to_numeric(df['social_aid_percent'], errors='coerce')
print(df.head(10))


#Functions categorizing the variables into 3 categories: high, middle and low. The interval of
# each category determined based on individual characteristics of the data.
# 3= best socioeconomic condition, 2= average condition, 1= worst condition


def home_ownership(row):
    if row['owner_occupied_homes'] < 51:
        return '1'
    elif row['owner_occupied_homes'] < 76:
        return '2'
    else:
        return '3'
df['Home ownership index'] = df.apply(home_ownership, axis=1)

#print(df[['Home ownership index']].head(10))

def labor_participation(row):
    if row['labor_participation'] > 65:
        return '3'
    elif row['labor_participation'] > 55:
        return '2'
    else:
        return '1'
df['Labor partcipation index'] = df.apply(labor_participation, axis=1)

#print(df[['Labor partcipation index']].head(10))


def low_income_households(row):
    if row['low_income_households'] > 9:
        return '3'
    elif row['low_income_households'] > 5:
        return '2'
    else:
        return '1'
df['Low income households index'] = df.apply(low_income_households, axis=1)


def households_around_minimum(row):
    if row['households_social_minimum'] > 20:
        return '1'
    elif row['households_social_minimum'] > 8:
        return '2'
    else:
        return '3'
df['Households around social minimum index'] = df.apply(households_around_minimum, axis=1)


#for household_income difficult defining boundaries of categories due to a lot of missing data
def household_income(row):
    if row['income_per_house'] < 25:
        return '1'
    elif row['income_per_house'] < 28:
        return '2'
    else:
        return '3'
df['Household income index'] = df.apply(household_income, axis=1)

# indexing for the rows that needed conversion from absolute values to percentages to normalize the data
def higher_education(row):
    if row['higher_education_percent'] < 35:
        return '1'
    elif row['higher_education_percent'] < 47:
        return '2'
    else:
        return '3'
df['Higher education index'] = df.apply(higher_education, axis=1)

def social_welfare_aid(row):
    if row ['social_aid_percent'] <6:
        return '3'
    elif row['social_aid_percent'] <15:
        return '2'
    else:
        return '1'
df['Social welfare aid index'] = df.apply(social_welfare_aid, axis=1)

#print(df[['Social welfare aid index']].head(10))


# Printing as new table, copy the population as a row and codes of neighborhoods as columns, 
# append all of the indicator values. 

result_df = pd.DataFrame()
result_df['Code'] = df['Code']

result_df['Home ownership index'] = df.apply(home_ownership, axis=1)
result_df['Labor participation index'] = df.apply(labor_participation, axis=1)
result_df['Low income households index'] = df.apply(low_income_households, axis=1)
result_df['Households around social minimum index'] = df.apply(households_around_minimum, axis=1)
result_df['Household income index'] = df.apply(household_income, axis=1)
result_df['Higher education index'] = df.apply(higher_education, axis=1)
result_df['Social welfare aid index'] = df.apply(social_welfare_aid, axis=1)

result_df.to_csv('socioecon_values.csv', index=False)

print(result_df.head(10))

#Indexing neighborhood value into 5 categories of socioeconomic condition
#max possible score per neighborhood is 21, minimum is 7 

df = pd.read_csv('socioecon_values.csv')

def assign_neighborhood_category(total_sum):
    if total_sum >18:
        return '5'
    elif total_sum >16:
        return '4'
    elif total_sum >13:
        return '3'
    elif total_sum >10:
        return '2'
    else:
        return '1'
df['Sum'] = df[['Home ownership index', 'Labor participation index', 'Low income households index', 'Households around social minimum index', 'Household income index', 'Higher education index', 'Social welfare aid index']].sum(axis=1)
df['Category'] = df['Sum'].apply(assign_neighborhood_category)

df.to_csv('socioecon_values_with_categories.csv', index=False)



# FINAL PRODUCT: a .csv with neighbohoods as either columns or rows (check the layer) 
# and crime amounts, crime /1000, socioeconomic index. Formatted in excel for simplicity. 
