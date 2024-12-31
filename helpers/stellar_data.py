"""gets stellar data from the NASA exoplanet archive
and updates the corrosponding dataframe.

's' shorthand refers to stellar"""

import pandas as pd

from database_helpers import upsert_stellar_data
from helpers import (
    get_user_confirm,
    tap_request, clean_data,
    show_cleaning, print_last_updated
)
# from plots import save_figures

def main():
    """collect updated data from archive and update the local database"""
    service_url = "https://exoplanetarchive.ipac.caltech.edu/TAP"
    s_schema_query = """
        SELECT *
        FROM TAP_SCHEMA.columns
        WHERE table_name
        LIKE 'stellarhosts'
    """
    s_query = """
        SELECT
            sy_name,
            hostname
        FROM stellarhosts
    """
    sort_column = 'hostname'

    if get_user_confirm("request schema, Y/N? "):
        s_schema = tap_request(
            service_url=service_url,
            query=s_schema_query,
            sync_type="sync"
        )
        # check if schema has changed since the last pull
            # report if updated and save
        print("Fetching schema...")
        s_schema.to_csv('stellar_hosts_schema.csv', index=False)
        print("Finished fetching schema")

    print("Fetching requested 'stellar hosts' table data...")
    s_df = tap_request(
        service_url=service_url,
        query=s_query,
        sync_type="async"
    )

    # clean data and show data before and after clean
    show_cleaning(s_df, s_df.hostname, sort_column)
    s_df = clean_data(s_df, sort_column)
    show_cleaning(s_df, s_df.hostname, sort_column)

    # append new data to stellar_hosts table in database and update existing if changes
    upsert_stellar_data(s_df)

    # print max last updated value from stellar table
    print_last_updated("stellar")


if __name__ == '__main__':
    main()
