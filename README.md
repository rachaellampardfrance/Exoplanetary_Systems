# PLANETARY SYSTEM QUERY DATA
#### Video Demo: <URL HERE>
#### Description:
#### Summary:
This program makes a syncronus TAP request to NASA'a database for the schema on one of it's tables called 'stellarhosts', it then creates an asyncronus request for the large amount of data from the specific collumns of data we want from the 'stellarhosts' database.

Then the data is cleaned and organised so that the program can create a figure containing two bar plots, representing the frequency of planets in a system in respect to the frequency of stars.

#### Program:
This program written in 'Jupyter Note Books' in Python and Markdown. The program is designed to make a request to NASA's astronimical Database using a TAP Plus request (Similar to an API request but the TAP protocol is a standard for the astronomical community).

Firstly a TapPlus class instance is created to carry out the TAP request to NASA's database. A query variable is made with an SQL string. Then a syncronus job is carried out as a function on the Tap class instance, with the SQL query passed in as an argument. This makes the SQL request and returns a job object with a VOTable table format.

For the first request it gets the schema of the database we are intrested in getting data from, as there are over 100 columns to the 'Stellar Hosts' database the information is truncated. For this reason the program saves the table as a .csv file we can read so that we can search through to find the columns of data we will be intrested in.
> This request is syncronus as it is a smaller request of information. Asyncronus requests are made for larger amounts of data otherwise it would not recive all of the data

<https://youtu.be/tRKeLrwfUgU?t=698>

Then the data is sorted alphabetically and any duplicate data is removed by system (as the database has a lot of repeated systems)

A Panada dataframe is created from the database and a new dataframe created grouping the data by system star count and system planet count by size and assosiated to one another.

Then a figure is created to house 2 bar plots

TODO

[!WARNING]
!! PROGRAM IS CURRENTLY INCORRECT !!