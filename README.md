<a id='top'></a>

# 🌌 EXOPLANETARY SYSTEMS

<a id='table_of_contents'></a>

## Table of Contents
<details open>
<summary>Contents</summary>

1. [📖 About The Project](#about_the_project)
    - [📋 Summary](#summary)
    - [🔧 built With](#built_with)
2. [❔ Getting Started](#getting_started)
    - [🖥️ Installation](#installation)
3. [🛰️ Usage](#usage)
    - 📈 [Data Sets](#data_sets)
    - 📉 [Plotted Graphs](#plotted_graphs)
        - 🌍 [Occurance Of Exoplanetary Systems By Star System Type](#plot1)
        - 🌏 [Exoplanet Systems by Star Count](#plot2)
        - 🌎 [Most Common Exoplanet Systems](#plot3)
4. [🗃️ Folder Automation](#folder_automation)
5. [📡 Acknowledgements](#acknowledgements)
6. [📧 Contact](#contact)

<!-- 🌠☄️👩‍🚀👩‍💻👩‍🔬💬💭🥼📻🔍📷📃📝✒️📊📆🗃️🪐 -->
</details>

<a id='about_the_project'></a>

## 📖 About The Project
<a id='summary'></a>

### 📋 Summary:
This program is intended to get star system data from NASA's 'stellar hosts' database via TAP request using ADQL. Then the data is organised and cleaned down to the unique star systems required Ready for analysis, the data is then organised into new data frames to plot various visual graphs...

<a id='built_with'></a>

### 🔧Built with

- 🌌 [Astropy & Astroquery](https://astroquery.readthedocs.io/en/latest/index.html)
    - ADQL 
- 🪐 [Jupyter Notebooks](https://docs.jupyter.org/en/stable/install.html)
- 📊 [Matplotlib](https://matplotlib.org/stable/install/index.html)
- 🔢 [Numpy](https://numpy.org/install/)
- 🐼 [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- 🐍 [Python](https://www.python.org/downloads/)
- 💠 Visual Studio Code

<a id='getting_started'></a>

## ❔ Getting Started

<a id='installation'></a>

### 🖥️ Installation

<details open>
<summary>Installation steps</summary>

1. Install [Python](https://www.python.org/downloads/)
    - Download Python3
2. Install [Jupyter Notebooks](https://docs.jupyter.org/en/stable/install.html)

        $pip install jupyter
3. Fork this repository
    - git clone https://github.com/rachaellampardfrance/Exoplanetary_Systems
4. Install requirements.txt

        $pip install -r requirements.txt
</details>

<!-- <a id='installation'></a>

### Installation
how to install the program...

    $ git clone   -->

<a id='usage'></a>

## 🛰️ Usage

<details open>
<summary>Usage</summary>

This program is written in 'Jupyter NoteBooks' in Python and Markdown. The program is designed to make a request to NASA's astronomical Database using a TAPPlus request (TAP protocol is a standard for the astronomical community).


Firstly a TapPlus class instance is created to carry out the TAP request to NASA's database. A query variable is made with an ADQL string. Then a synchronous job is carried out as a function on the TapPlus class instance, with the ADQL query passed in as an argument. This makes the ADQL request and returns a job object with a VOTable table format.


For the first request it gets the schema of the database we are interested in getting data from, as there are over 100 columns to the 'Stellar Hosts' database the information is truncated. For this reason the program saves the table as a .csv file we can read so that we can search through to find the columns of data we will be interested in.
> This request is synchronous as it is a smaller request of information. Asynchronous requests are made for larger amounts of data otherwise it would not receive all of the data


Then the data is sorted alphabetically and any duplicate data is removed by system (as the database has a lot of repeated systems as it records individual stellar bodies within the systems)


Once the data is cleaned three data sets are created...


<a id='data_sets'></a>

### 📈 data sets
<a id='system_df'></a>
- **system_df:**
    - A large pandas dataframe containing all systems names, star number and planet number within the system.  
    - Created from the cleaned data from NASA's 'Stellar Hosts' database
   
<a id='star_srs'></a>
- **star_srs:**
    - A small pandas series with the 'system star count' as the index and the occurrence that exoplanets have been observed in the system type *(not all exoplanets - the occurrence of a system containing exoplanets)*.
    - Created from the 'system_df'

<a id='planet_to_star_df'></a>
- **planet_to_star_df:**
    - A small pandas dataframe with the 'system star count' as the index and divided into additional 'exoplanet count' columns by system, the data relates to observed occurrences.
    - Created from the 'system_df'

Once the data required is organised three plots are visualised using the data...

</details>


<a id='plotted_graphs'></a>

### 📉 Plotted Graphs
<details open>
<summary>Plots</summary>
The program creates three plot figures...

<a id='plot1'></a>

#### 🌍**1. Occurance Of Exoplanetary Systems By Star System Type:**


Intent:
A pie chart representation of what type of systems exoplanets most commonly occur in relation to how many stars are within the system.

Contents:
- Figure
    - Pie chart - *represents data of what systems exoplanets most commonly occur in, related to how many stars are in the system.*
    - Legend - *displays how many stars are in each system on the pie chart related by color.*
    - Additional exoplanet discovery data - *extra data displayed on the figure represents how many confirmed exoplanet systems have been discovered as well as individual exoplanets.*

<p align="center">
<img src='static\occurance_of_exoplanetary_systems_by_star_system_type.png' alt='"occurance of exoplanetary systems by star system type" pie chart' width='600'>
</p>

<a id='plot2'></a>

#### 🌏**2. Exoplanet Systems by Star Count:**

Intent:
A figure containing two nested bar charts that represent all observations of exoplanet systems, nested by how many exoplanets occur in each system and organised by how many stars are in the system. This is intended to show the frequency in which exoplanets/multiplanetary systems occur in relation to singular star and binary star systems.

The same data is shown in two formats: scale and log. 'Scale' helps visualise the actual occurrence of exoplanetary systems whereas 'log' is intended to help visualise small frequencies.

Contents:
- Figure
    - Nested bar chart - *represents all observations of exoplanet systems, nested by how many exoplanets occur in each system and organised by how many stars are in the system.*
    - Nested bar chart LOG - *represents the same data as above but in a log format to help visualise small data*

<p align="center">
<img src='static/exoplanet_systems_by_star_count.png' alt='exoplanet systems by star count figure image' width='900'>
</p>


<a id='plot3'></a>

#### 🌎**3. Most Common Exoplanet Systems:**

Intent:
A collection of pie charts which are independent of one another, each corresponding to a type of star/binary star system. Each pie chart represents which is the most common type of exoplanet systems in relation to the star system.

>[!NOTE] These pie charts do not include any exoplanet systems that would fall in less than 1% of the overall data (this is to prevent small data crowding the data: as this is a visual generalisation)
>
>Additionally note that data that falls in less than the 1% is completely left out of the data.


Contents:
- Figure
    - Pie charts - *Each pie chart represents which is the most common types of exoplanet systems in relation to it's systems star count*
    - Legend - *The legend visualises the planet count by color and applies to all pie charts*

<p align="center">
<img src='static/most_common_exoplanet_systems.png' alt='Most common exoplanet systems pie charts figure' width='900'>
</p>

</details>

<a id='folder_automation'></a>

## 🗃️ Folder Automation

This program has been designed so that when a new figure is created it attempt to create a folder within static named with the current date, and save the figure within this folder with the addition of a datestamp in the file name. The figure will also be saved to the top level of 'static/' without a date stamp and will overwrite the existing figure so that the figures remain up to date for this README. 
- if a folder with the current date already exists the folder creation step will be skipped
- if a file with the same name already exists in this folder the user will be asked if they want to overwrite the file.

<a id='acknowledgements'></a>

## 📡 Acknowledgements

- 🚀 [NASA's Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu): All data is gathered from NASA's 'Stellar Hosts' database 
    - **DOI: 10.26133/NEA40**

- 🔭 [Astroquery](https://ui.adsabs.harvard.edu/abs/2019AJ....157...98G/abstract)


<a id='contact'></a>

## 📧 Contact

###  Creator: Rachael Lampard-France

<!-- [![Linkedin Logo](linkedin.png)](https://www.linkedin.com/in/rachael-lampard-france-a5995b195/) -->

<a href='https://www.linkedin.com/in/rachael-lampard-france-a5995b195/'><img src='static/linkedin.png' alt='Linkedin Logo' width='100'></a>

Project Link - https://github.com/rachaellampardfrance/Exoplanetary_Systems

[return to top](#top)
