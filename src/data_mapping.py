import os
import warnings
import numpy as np
import pandas as pd
import data_conversion

def dataMapping(data):
	
    data['gender'] = data['gender'].map(data_conversion.gender_map, na_action='ignore')
    data['ever_married'] = data['ever_married'].map(data_conversion.ever_married_map, na_action='ignore')
    data['work_type'] = data['work_type'].map(data_conversion.work_type_map, na_action='ignore')
    data['Residence_type'] = data['Residence_type'].map(data_conversion.residence_type_map, na_action='ignore')
    data['smoking_status'] = data['smoking_status'].map(data_conversion.smoking_status_map, na_action='ignore')

    #Assigning integer values to BMIs after separating them into ranged bins
    #https://www.bmi-chart.info/bmi-table
    data.loc[data['bmi'] <= 18.5, 'bmi'] = 0 #124 lbs or less
    data.loc[(data['bmi'] > 18.5) & (data['bmi'] <= 24.9), 'bmi'] = 1 #125 lbs to 168 lbs
    data.loc[(data['bmi'] > 24.9) & (data['bmi'] <= 29.9), 'bmi'] = 2 #169 lbs to 202 lbs
    data.loc[(data['bmi'] > 29.9) , 'bmi'] = 3 #203 lbs or more

    #Assigning integer values to age after separating them into ranged bins
    data.loc[data['age'] <= 18, 'age'] = 0  
    data.loc[(data['age'] > 18) & (data['age'] <= 35), 'age'] = 1 
    data.loc[(data['age'] > 35) & (data['age'] <= 65), 'age'] = 2 
    data.loc[(data['age'] > 65) , 'age'] = 3 
    data['age'] = data['age'].astype('int')

    # Turn certain glucose ranges into ranged bins, according to public health ratings from web
    #https://www.healthline.com/health/estimated-average-glucose#target-range
    data.loc[data['avg_glucose_level'] <= 114, 'avg_glucose_level'] = 0 # normal
    data.loc[(data['avg_glucose_level'] > 114) & (data['avg_glucose_level'] <= 140), 'avg_glucose_level'] = 1 # pre-diabetes
    data.loc[(data['avg_glucose_level'] > 140), 'avg_glucose_level'] = 2 # diabetes
    data['avg_glucose_level'] = data['avg_glucose_level'].astype('int')

