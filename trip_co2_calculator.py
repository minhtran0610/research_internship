import googlemaps
import pandas as pd
import numpy as np


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


def main():
    # Get the API key
    api_key = get_api_key("google_api_key.txt")

    # Retrieve the Google Maps object
    gmaps = googlemaps.Client(key=api_key)

    # Retrieve the car database from Traficom. The database has been filtered
    # to ensure the perfomance of the program
    traficom_database = pd.read_csv("filtered_data_traficom.csv")

    # Get the CO2 emission of the car
    print("First, choose your car.")
    co2_emission = get_car_emission(traficom_database)
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


if __name__ == "__main__":
    main()