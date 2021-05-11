# research_internship
This repository contains the 2 programs I have written during the Research Training period at Tampere University. The programs are at the files
fingrid_api_experiment.py and trip_co2_calculator.py. The language I have used for both the 2 programs in Python.

The program filter_traficom_data.py filters the CSV file from Traficom. Because the original CSV file is very huge, I cannot include that to this repository.
If you wish to run that program, please download the original file from https://www.traficom.fi/fi/ajankohtaista/avoin-data?toggle=Ajoneuvojen%20avoin%20data%205.14
and change the name in the program to match that CSV file. Instead I have included a filtered one, which is the result of this program.

The program fingrid_api_experiment.py calculates the emission of using a particular computer. The program uses the data from Energy Star for the energy consumption
of the device, and the real-time data on emission per electricity usage from Fingrid.

The second program is the combination of data sets from Traficom and Google Maps to calculate the emission of a particular car during a particular trip. The program
lets the user choose their car and their desired origin and destinations. Then the program will retrieve data from Google about the distance and calculate the amount
of CO2 based on average emission of the car and the distance of the trip.

