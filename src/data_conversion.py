import os
import warnings

#data conversion to integer number from associated strings
gender_map = {
    'Male': 0,
    'Female': 1,
    'Other': 2
}

ever_married_map = {
    'No': 0,
    'Yes': 1
}

work_type_map = {
    'Private': 0,
    'Self-employed': 1,
    'Govt_job': 2,
    'children': 3,
    'Never_worked': 4
}

residence_type_map = {
    'Urban': 0,
    'Rural': 1
}

smoking_status_map = {
    'formerly smoked': 0,
    'never smoked': 1,
    'smokes': 2,
    'Unknown': 3 
}


