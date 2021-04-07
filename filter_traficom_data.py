import pandas as pd
import numpy as np
import datetime

# Wanted columns for the CSV file
wanted_columns = ['ajoneuvoluokka', 'ensirekisterointipvm', 'merkkiSelvakielinen', 'mallimerkinta', 'kaupallinenNimi', 'Co2']
names = ['class', 'make', 'model', 'commercial_model_name', 'co2']

# Convert data type for better perfomance
data_type_conversion = {
    'ajoneuvoluokka': 'category',
    'ensirekisterointipvm': str,
    'merkkiSelvakielinen': 'category',
    'mallimerkinta': 'category',
    'kaupallinenNimi': 'category',
    'Co2': np.float16
}

# Read the file
traficom_data = pd.read_csv('TieliikenneAvoinData_5_13.csv', sep=';',
                            usecols=wanted_columns, dtype=data_type_conversion)

# Filter the database

# First, keep the year and keep only the consumer cars
traficom_data['ensirekisterointipvm'] = traficom_data['ensirekisterointipvm'].str[:4]
personal_car_database = traficom_data.query('ajoneuvoluokka == "M1" | ajoneuvoluokka == "M1G"')

# Process the entries without the CO2 value by converting them to NaN and
# remove the rows with NaN
personal_car_database['Co2'] = personal_car_database['Co2'].replace(0, np.nan)
personal_car_database.dropna(inplace=True)
personal_car_database.reset_index(drop=True, inplace=True)

# Convert the car makers, models and versions to uppercase
personal_car_database['merkkiSelvakielinen'] = personal_car_database['merkkiSelvakielinen'].str.upper()
personal_car_database['kaupallinenNimi'] = personal_car_database['kaupallinenNimi'].str.upper()
personal_car_database['mallimerkinta'] = personal_car_database['mallimerkinta'].str.upper()

# Convert the year column to integer
personal_car_database['ensirekisterointipvm'] = pd.to_numeric(personal_car_database['ensirekisterointipvm'])

# Remove all the duplicate datas
personal_car_database = personal_car_database.drop_duplicates()

# Safe the filtered data to a new database
personal_car_database.to_csv('filtered_data_traficom.csv', index=False)

