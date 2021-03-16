"""
This program calculates the CO2 emission based on the data provided by
Fingrid and Energy Star. 
"""

import requests
import json
import datetime


"""
Get the data from the API Link
    :param link: str,
        The link of the API
    :param header: dict,
        The header of the API link
    :return json:
        The JSON of the data
"""
def get_data(link, header):
    response = requests.get(link, headers=header)
    json = response.json()
    return json


"""
Find the appropriate data from Energy Star according to the model number
    :param model_number: str,
        The model number of the computer
    :return json:
        The JSON of the data
"""
def find_model_number(model_number):
    # Create the API link
    link = "https://data.energystar.gov/resource/j7nq-iepp.json"
    filtered_model_link = f"{link}?model_number={model_number}"

    # Get the data
    header = {'x-api-key': '50ggs7j2zhy8zcsf0nzghec44'}
    json = get_data(filtered_model_link, header)

    return json


"""
Decide the category of the computer according to Energy Star and return the
corresponding typical energy consumption (TEC)
    :param energy_star_data_json:
        The JSON of the data of the product that has been found with the model number
    :return tec: float,
        The typical energy consumption of the product
"""
def tec_of_product(energy_star_data_json):
    # Decide the category of the computer according to Energy Star
    category = energy_star_data_json[0]['comp_cat_for_tec_typical_energy_consumption_criteria']
    field_list = [f"comp_cat_i{category}_tec_of_model_kwh", f"category_{category}_tec_of_model_kwh", 
                        f"comp_cat_d{category}_tec_of_model_kwh"]

    # Get the TEC (typical energy consumption)
    for field in field_list:
        try:
            tec = float(energy_star_data_json[0][field])
            break
        except KeyError:
            pass
    
    return tec


"""
Calculate the average CO2 emission of the product and print the
result message
    :param avg_emi_con: float,
        The average emission of electricity consumption
    :param tec: float,
        The typical energy consumption of the product
    :param time:
        The time of update of the avaerage emission of electricity consumption
"""
def calculate_emission(avg_emi_con, tec, time):
    # The CO2 emission will be calculated using the equation:
    # CO2 emission = TEC(kWh) * average emission of energy consumption(gCO2/kWh)
    result = tec * avg_emi_con

    # Print the message
    print()
    print("The CO2 emission is calculated using the equation:")
    print("CO2 emission = typical energy consumption (kWh) * average emission of energy consumption (gCO2/kWh)")
    print()
    print(f"The average emission of electricity consumption in Finland, according to Fingrid, updated at {time} is {avg_emi_con} gCO2/kWh.")
    print(f"The typical energy consumption of your computer, according to Energy Star, is {tec} kWh.")
    print()
    print(f"The CO2 emission of your computer is {result:.2f} grams of CO2.")
    print()


# Process the data for average emisson of electricity consumption in Finland from Fingrid

# Get the data
header_fingrid = {'x-api-key': '0F7Lvj4uQT9qjVQzs23SH57x0ynbM8AB8hrHpaWe'}
fingrid_data_json = get_data("https://api.fingrid.fi/v1/variable/265/event/json", header_fingrid)

# Get the time stamp of the data
time_string = fingrid_data_json['start_time']
time = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S%z")

# Get the value of the data
avg_emi_con = float(fingrid_data_json['value'])


# Process the data for total energy consumption of computers from Energy Star

while True:
    # Get the model number from the user
    print("The model numbers can be found at https://www.energystar.gov/productfinder/product/certified-computers")
    model_number = input("Enter model number of your computer, or enter QUIT to quit: ")

    if (model_number.upper() == "QUIT"):
        break

    # Get the data
    energy_star_data_json = find_model_number(model_number)

    # Calculate the result
    if (energy_star_data_json == []):
        print("Model number invalid")
    else:
        # Decide the category of the computer according to Energy Star
        tec = tec_of_product(energy_star_data_json)
        # Calculate the CO2 emission of the product according to the 2 database, print the result message
        calculate_emission(avg_emi_con, tec, time)
        




