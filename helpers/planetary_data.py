"""gets planetary systems data from the NASA exoplanet archive
and updates the corrosponding dataframe.

'ps' shorthand refers to planetary systems"""

import pandas as pd

from helpers import (
    get_user_confirm, tap_request,
    clean_data, show_cleaning,
    get_last_csv, is_data_different,
    date_data_pull
)
from database_helpers import update_database
from save import save_dated_data_csv

def main():
    service_url = "https://exoplanetarchive.ipac.caltech.edu/TAP"
    schema_query = "SELECT * FROM TAP_SCHEMA.columns WHERE table_name LIKE 'ps'"
    planetary_systems_query = "SELECT pl_name, hostname, sy_snum, sy_pnum, cb_flag FROM ps"
    db_path = "database.db"
    db_table = "planetary_systems"
    sort_column = 'pl_name'

    if get_user_confirm("request schema, Y/N? "):
        planetary_systems_schema = tap_request(service_url=service_url, query=schema_query, sync_type="sync")
        
        # check if schema has changed since the last pull
            # report if updated and save
        planetary_systems_schema.to_csv("planetary_systems_schema.csv", index=False)
        
        print("Finished fetching schema")
    
    print("Fetching requested 'planetary systems' table data...")
    ps_df = tap_request(service_url=service_url, query=planetary_systems_query, sync_type="async")

    show_cleaning(ps_df, ps_df.pl_name, sort_column)
    ps_df = clean_data(ps_df, sort_column)
    show_cleaning(ps_df, ps_df.pl_name, sort_column)

    ps_df = date_data_pull(ps_df)
    # updates database only by new 'pl_name' does not update old 
    update_database(db_path, db_table, ps_df, sort_column)

    ps_df.to_csv("planetary_systems.csv", index=False)

    last = get_last_csv("planetary_systems", "static/")
    if is_data_different(last, "planetary_systems.csv"):
        save_dated_data_csv(ps_df, "planetary_systems")

        # planets_df = pd.DataFrame(planetary_systems)
        
        # create logic for saving new planet info to a database? or request

    else:
        print("Data has not changed from last call")

if __name__ == '__main__':
    main()