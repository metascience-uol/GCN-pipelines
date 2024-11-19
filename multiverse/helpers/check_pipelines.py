import pandas as pd


file_path = 'Data/Database_clean.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Combined use
count_combination = df.apply(lambda row: 'F-motion_regression' in row.values and 'F-Global_signal' in row.values, axis=1).sum()

# Individual use
count_motion_regression = df.apply(lambda row: 'F-motion_regression' in row.values, axis=1).sum()
count_global_signal = df.apply(lambda row: 'F-Global_signal' in row.values, axis=1).sum()

print(count_combination, count_motion_regression, count_global_signal)
