import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import f_oneway

# -- import data
# preset = subprocess.run(['python', 'analyze_visits.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# if preset.returncode == 0:
#     print("Imported data")  # it worked
# else:
#     print("Data needed")  # either file doesn't exist or analyze_visits.py needs checking
df = pd.read_csv('ms_data_with_insurance.csv')

# Analyze walking speed
model = sm.OLS.from_formula('walking_speed ~ education_level + age', data=df).fit()
print(model.summary())

# Analyze costs
# insurance_groups = [df[df['insurance_type'] == typ]['visit_cost'] for typ in df['insurance_type'].unique()]
# anova_result = f_oneway(*insurance_groups)
anova_result = sm.stats.anova_lm(model, typ=2)
print(f"ANOVA p-value: {anova_result}")

# Visual check
plt.figure()
df.boxplot(column='visit_cost', by='insurance_type')
plt.title('Cost of Visit by Insurance Type')
plt.ylabel('Cost of Visit')
plt.xlabel('Insurance Type')
plt.show()

# Advanced analysis
model_2 = sm.OLS('walking_speed ~ education_level * age', data=df).fit()
print(model_2.summary())
