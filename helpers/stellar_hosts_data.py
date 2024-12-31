"""gets stellar hosts data from the NASA exoplanet archive
and updates the corrosponding dataframe.

'sh' shorthand refers to stellar hosts"""

import pandas as pd

from database_helpers import upsert_stellar_hosts_data
from helpers import (
    get_user_confirm,
    tap_request, clean_data,
    show_cleaning, print_last_updated,
    render_figlet
)
# from plots import save_figures

def main():
    """collect updated data from archive and update the local database"""
    render_figlet("Stellar Hosts Data Request Program...")
    
    service_url = "https://exoplanetarchive.ipac.caltech.edu/TAP"
    sh_schema_query = """
        SELECT *
        FROM TAP_SCHEMA.columns
        WHERE table_name
        LIKE 'stellarhosts'
    """
    sh_query = """
        SELECT
            sy_name,
            sy_snum,
            sy_pnum
        FROM stellarhosts
    """
    sort_column = 'sy_name'

    if get_user_confirm("request schema, Y/N? "):
        sh_schema = tap_request(
            service_url=service_url,
            query=sh_schema_query,
            sync_type="sync"
        )
        # check if schema has changed since the last pull
            # report if updated and save
        print("Fetching schema...")
        sh_schema.to_csv('stellar_hosts_schema.csv', index=False)
        print("Finished fetching schema")

    print("Fetching requested 'stellar hosts' table data...")
    sh_df = tap_request(
        service_url=service_url,
        query=sh_query,
        sync_type="async"
    )

    # clean data and show data before and after clean
    show_cleaning(sh_df, sh_df.sy_name, sort_column)
    sh_df = clean_data(sh_df, sort_column)
    show_cleaning(sh_df, sh_df.sy_name, sort_column)

    # append new data to stellar_hosts table in database and update existing if changes
    upsert_stellar_hosts_data(sh_df)

    # print max last updated value from stellar_hosts table
    print_last_updated("stellar_hosts")


if __name__ == '__main__':
    main()
