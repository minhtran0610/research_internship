import googlemaps
import pandas as pd
import numpy as np
import re


"""
Get the API key from the file provided by the user.
:param filename: str,
    The name of the file
:return api_key: str,
    The API key
"""
def get_api_key(filename):
    try:
        file = open(filename, mode='r')
        api_key = ""
        for line in file:
            api_key = line.rstrip()

        return api_key
    
    except IOError:
        print("Cannot open file")


"""
Find the rows that has the same value in a specified column
:param database: pandas.Dataframe,
    The database to filter the rows
:param column: str,
    The name of the column
:param value: str,
    The value of the column to filter the rows
:return new_database: pandas.Dataframe,
    The new database containing the rows
"""
def find_rows(database, column, value):
    return database.loc[database[column] == value]


"""
Print the unique values of a columns
:param database: pandas.Dataframe,
    The car database
:param column: str,
    The name of the column
"""
def print_unique_column(database, column):
    # Get the unique values
    value_list = database[column].unique().tolist()

    for value in value_list:
        print(value)


"""
Let the user find their car in the database using the brand name,
model name, version name, and model year
:param database: pandas.Dataframe,
    The car database
:return: float,
    The CO2 emission of the car entered by the user
"""
def get_car_emission(database):
    while True:
        # Get the brand name from the user
        brand_name = input("Please enter the brand name of your car: ").upper()

        # Find the rows that corresponds to the brand name
        brand_df = find_rows(database, 'merkkiSelvakielinen', brand_name)

        # Check if the brand name is valid. The brand name is valid when the
        # new database is not empty
        if brand_df.empty:
            print("The brand name is invalid. Please try again.")
        else:
            # Print the models available with the brand
            print("The models which are available with your car brands:")
            print_unique_column(brand_df, 'kaupallinenNimi')


            # Take the car model from the user
            model_name = input("Enter your model name: ").upper()

            # Filter the database using the model
            model_df = find_rows(brand_df, 'kaupallinenNimi', model_name)

            # Check if the model name is valid
            if model_df.empty:
                print("The model name is invalid. Please try again.")
            else:
                print("The versions which are available with your model:")
                print_unique_column(model_df, 'mallimerkinta')


                # Take the version name from the user
                version_name = input("Enter your version name: ").upper()

                # Filter the database using the version name
                version_df = find_rows(model_df, 'mallimerkinta', version_name)

                # Check if the version is valid
                if version_df.empty:
                    print("The version name is invalid. Please try again.")
                else:
                    print("The model years which are available for your car:")
                    print_unique_column(version_df, 'ensirekisterointipvm')


                    # Get the registration year by the user
                    year = int(input("Enter the registration year of your car: "))

                    # Filter the data using the registration year
                    # year_df = find_rows(version_df, 'ensirekisterointipvm', year)
                    year_df = find_rows(version_df, 'ensirekisterointipvm', year)

                    #  Check if the registration year is valid. If does, return the CO2 emission.
                    if year_df.empty:
                        print("Model year is invalid. Please try again")
                    else:
                        return year_df.iloc[0]['Co2']
                    

"""
Find the place with the keyword given by the user
:param gmaps: Google Maps Client Object,
    The Google Maps Client provide by Google
:return: str,
    The address of the search result the user chooses
"""
def find_place(gmaps):
    while True:
        # Take the keyword from the user
        keyword = input('Enter keyword: ')

        # Find the place using the Google Maps object
        results = gmaps.places(keyword)['results']

        # Print the result
        for i in range(len(results)):
            print(f"{i+1}. {results[i]['name']}: {results[i]['formatted_address']}")

        # Get the choice from the user. The user can enter the index of their choice
        # to choose a result, or enter AGAIN to try again
        while True:
            choice = input("Enter your choice by entering the index next to the result. If you want to try again, enter AGAIN: ")

            if choice.isnumeric():
                choice = int(choice)
                if choice > len(results):
                    print("Invalid choice.")
                else:
                    return results[choice-1]['formatted_address']
            elif choice.upper() == 'AGAIN':
                break
            else:
                print("Invalid choice.")


"""
Get the distance of the 2 places using the APIs from Google
:param gmaps: Google Maps Client object,
    The Google Maps Client provided by Google
:param origin: str,
    The origin's address
:param destination: str,
    The destination's address
:return: float,
    The distance in kilometers.
"""
def get_distance(gmaps, origin, destination):
    # Using Google Maps to calculate the distance
    result = gmaps.distance_matrix(origin, destination, 'driving')

    # Get the distance as meters
    distance = result['rows'][0]['elements'][0]['distance']['value']

    return distance/1000


"""
Calculate the distance of the trip by letting the user enter
the origin and destination, and return the distance in kilometers
:param gmaps: Google Maps Client object,
    The Google Maps Client provided by Google
:return: float,
    The distance in kilometers
"""
def calculate_distance_trip(gmaps):
    # Get the address of the origin
    print("Origin.")
    origin = find_place(gmaps)
    print()

    # Get the address of the destination
    print("Destination.")
    destination = find_place(gmaps)
    print()

    # Return the distance
    return get_distance(gmaps, origin, destination)


"""
Remove the HTML tags from a string.
:param text: str,
    The string to remove the HTML tags
:return: str,
    The string whose HTML tags has been cleared
Reference: Galvis, J. (2020, September 19). How to strip html tags from a string in Python.
Medium. https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44. 
"""
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


"""
Get directions from Google Maps and return the directions in
HTML format.
:param gmaps: googlemaps.Client,
    The Client object for the Google Maps API.
:param origin: str,
    The origin place in string format.
:param destination: str,
    The destination in str format.
:return steps_html: list,
    The list containing the steps in HTML format.
"""
def get_direction(gmaps, origin, destination):
    # Retrieve the result
    googlemaps_results = gmaps.directions(origin, destination, 'driving')[0]['legs'][0]['steps']

    # Filter the result
    steps_html = []
    for item in googlemaps_results:
        steps_html.append(item['html_instructions'])
    
    return steps_html


"""
Print the information of the car according to Traficom
:param database: pandas.Dataframe,
    The car database from Traficom
"""
def print_car_emission(database):
    # Get the CO2 emission of the car
    print("Choose your car.")
    co2_emission = get_car_emission(database)
    # Print the result 
    print(f"The average CO2 emission of the car, according to Traficom, is: {co2_emission} g/km")
    print()


"""
Let the user input the car and the destinations of the trip.
Calculate the distance, average car emissions and the total
admissions of the trip.
:param database: pandas.DataFrame,
    The database for the cars from Traficom
:param gmaps: googlemaps Client,
    The Google Maps client for the APIs
"""
def print_emission_trip(database, gmaps):
    # Get the CO2 emission of the car
    print("First, choose your car.")
    co2_emission = get_car_emission(database)
    # Print the result 
    print(f"The average CO2 emission of the car, according to Traficom, is: {co2_emission} g/km")
    print()
    
    # Get the distance of the trip
    print("Second, choose the places of the trip.")
    distance = calculate_distance_trip(gmaps)
    # Print the result
    print(f"The distance of the trip, according to Google Maps, is: {distance} km")
    print()

    # Print the result
    result = co2_emission * distance
    print(f"The total CO2 emission of the trip is: {result:.2f} g")
    print()


"""
Print the direction
"""
def print_direction(gmaps):
    # Get the address of the origin
    print("Origin.")
    origin = find_place(gmaps)
    print()

    # Get the address of the destination
    print("Destination.")
    destination = find_place(gmaps)
    print()

    # Process the result and print the directions
    steps_html = get_direction(gmaps, origin, destination)

    last_steps = steps_html.pop()
    last_steps_separation = last_steps.split('<div style="font-size:0.9em">')
    for step_html in last_steps_separation:
        steps_html.append(step_html)
    
    steps_str = []
    for step_html in steps_html:
        steps_str.append(remove_html_tags(step_html))

    # Print the result
    for step in steps_str:
        print(step)
    print()


"""
Print the lists of commands
"""
def print_commands():
    command_list = ["CAR INFORMATION", "CO2 CALCULATOR", "DIRECTION", "HELP", "QUIT"]
    command_abbreviation_list = ["CI", "CC", "D", "H", "Q"]
    command_function = [
        "Print the car's average emission according to Traficom",
        "Calculate the CO2 emission according to the places of the trip and the car's average emission",
        "Give directions for the desired origins and destinations",
        "Print the commands of the program",
        "Quit the program"
    ]

    for i in range(len(command_list)):
        print(f"{command_list[i]} or {command_abbreviation_list[i]}: {command_function[i]}")
    print()
    
    
def main():
    # Get the API key
    api_key = get_api_key("google_api_key.txt")

    # Retrieve the Google Maps object
    gmaps = googlemaps.Client(key=api_key)

    # Retrieve the car database from Traficom. The database has been filtered
    # to ensure the perfomance of the program
    traficom_database = pd.read_csv("filtered_data_traficom.csv")

    while True:
        command = input("Enter command. To see the list of commands, enter HELP: ")

        if command.upper() == "CAR INFORMATION" or command.upper() == "CI":
            print_car_emission(traficom_database)

        elif command.upper() == "CO2 CAlCULATOR" or command.upper() == "CC":
            print_emission_trip(traficom_database, gmaps)

        elif command.upper() == "DIRECTION" or command.upper() == "D":
            print_direction(gmaps)

        elif command.upper() == "HELP" or command.upper() == "H":
            print_commands()
        
        elif command.upper() == "QUIT" or command.upper() == "Q":
            break

        else:
            print("Invalid command")


if __name__ == "__main__":
    main()