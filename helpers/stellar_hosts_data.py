"""gets stellar hosts data from the NASA exoplanet archive
and updates the corrosponding dataframe.

'sh' shorthand refers to stellar hosts"""

import pandas as pd

from helpers import (
    get_last_csv, get_user_confirm,
    tap_request, clean_data,
    show_cleaning, is_data_different,
    date_data_pull
)
from database_helpers import update_database
from plots import save_figures
from save import save_dated_data_csv

def main():
    service_url = "https://exoplanetarchive.ipac.caltech.edu/TAP"
    schema_query = "SELECT * FROM TAP_SCHEMA.columns WHERE table_name LIKE 'stellarhosts'"
    stellar_hosts_query = "SELECT sy_name, sy_snum, sy_pnum FROM stellarhosts"
    db_path = "database.db"
    db_table = "stellar_hosts"
    sort_column = 'sy_name'

    if get_user_confirm("request schema, Y/N? "):
        sh_schema = tap_request(service_url=service_url, query=schema_query, sync_type="sync")
        # check if schema has changed since the last pull
            # report if updated and save
        sh_schema.to_csv('stellar_hosts_schema.csv', index=False)
        print("Finished fetching schema")
    
    print("Fetching requested 'stellar hosts' table data...")
    sh_df = tap_request(service_url=service_url, query=stellar_hosts_query, sync_type="async")

    show_cleaning(sh_df, sh_df.sy_name, sort_column)
    sh_df = clean_data(sh_df, sort_column)
    show_cleaning(sh_df, sh_df.sy_name, sort_column)

    sh_df = date_data_pull(sh_df)
    # updates database only by new 'sy_name' does not update old 
    update_database(db_path, db_table, sh_df, sort_column)

    sh_df.to_csv('stellar_hosts.csv', index=False)

#     last = get_last_csv("stellar_hosts", "static/")
#     if is_data_different(last, "stellar_hosts.csv"):
#         save_dated_csv(sh_df)

#         # create data frames for figures
#         systems_df = create_systems_df(sh_df)
#         star_series = create_star_series(systems_df)
#         planet_to_star_df = create_planet_to_star_df(systems_df)

#         save_figures(systems_df=systems_df, star_series=star_series, planet_to_star_df=planet_to_star_df)

#     else:
#         print("Data has not changed from last call")
#     print("Ending program...")

    
# def save_dated_csv(data: pd.DataFrame) -> None:
#     print("creating new folder")
#     save_dated_data_csv(data, "stellar_hosts")

def create_systems_df(data: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(data)

def create_star_series(data: pd.DataFrame) -> pd.DataFrame:
    # group df by sy_snum size all instances of the same star count are combined
    # this allows us to see the occurance of systems that contain any amount of planets
    star_srs = data.groupby('sy_snum').size()
    # see the series
    print(star_srs)
    # see series index values
    print(star_srs.index.values)
    # see sum of data
    print(star_srs.sum())

    return star_srs

def create_planet_to_star_df(data):
    #df when grouping by sy_snum and sy_pnum by size() and unstacked(make missing data == 0 for table)
    planet_to_star_df = data.groupby(['sy_snum', 'sy_pnum']).size().unstack(fill_value=0)

    # see visual dataframe representation
    print(planet_to_star_df)

    return planet_to_star_df


if __name__ == '__main__':
    main()