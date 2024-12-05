import pandas as pd
import numpy as np
import random

# Load and structure the data
df = pd.read_csv('ms_data.csv')
df = df.drop_duplicates() # remove dupes
df['visit_date'] = pd.to_datetime(df['visit_date'])
df = df.sort_values(by=['patient_id', 'visit_date'])

# Add insurance information
insurance_types = pd.read_csv('insurance.lst', header=None)[0].values

# -- sort by unique id, map insurance types, then apply them back to data frame
unique_patient_ids = df['patient_id'].unique()
insurance_map = {i: random.choice(insurance_types) for i in unique_patient_ids}
df['insurance_type'] = df['patient_id'].map(insurance_map)

# -- set up function for costs using insurance type and distribution
def get_cost(insurance_type):
    if insurance_type == 'Basic':
        return np.random.normal(100, 10)
    elif insurance_type == 'Average':
        return np.random.normal(150, 15)
    elif insurance_type == 'Plus':
        return np.random.normal(200, 20)
    else: 
        return np.random.normal(300, 30)

# -- apply function back to data set
df['visit_cost'] = df['insurance_type'].apply(get_cost)

# Calculate summary statistics
mean_speed = df.groupby('education_level')['walking_speed'].mean()
print("Mean Walking Speed by Education Level:\n", mean_speed)

mean_costs = df.groupby('insurance_type')['visit_cost'].mean()
print("\nMean Visit Costs by Insurance Type:\n", mean_costs)

age_effect = df.groupby('age')['walking_speed'].mean()
print("\nAge Effects on Walking Speed:\n", age_effect)

df['age_group'] = pd.cut(df['age'], bins=[18, 30, 40, 50, 60, 100], labels=['18-30', '30-40', '40-50', '50-60', '60+'])
mean_walking_speed_age = df.groupby('age_group')['walking_speed'].mean()
print("\nAge Effects on Walking Speed by Group:\n", mean_walking_speed_age)

# Save new df for further processing
df.to_csv('ms_data_with_insurance.csv', index=False)

# Checkpoint
insurance_consistency = df.groupby('patient_id')['insurance_type'].nunique()
inconsistent_patients = insurance_consistency[insurance_consistency > 1]

# If there are any inconsistent patients, print them
if not inconsistent_patients.empty:
    print("\nInconsistent insurance types found for the following patients:")
    print(inconsistent_patients)
else:
    print("\nAll patients have consistent insurance type listed.")