"""gets planetary systems data from the NASA exoplanet archive
and updates the corrosponding dataframe.

'ps' shorthand refers to planetary systems"""

from database_helpers import (
    upsert_planetary_data,
    print_table_updated_count
)
from helpers import (
    get_user_confirm, tap_request,
    clean_data, show_cleaning,
    print_last_updated, render_figlet
)

def main():
    """collect updated data from archive and update the local database"""
    render_figlet("Planetary Data Request Program...")

    service_url = "https://exoplanetarchive.ipac.caltech.edu/TAP"
    ps_schema_query = """
        SELECT *
        FROM TAP_SCHEMA.columns
        WHERE table_name
            LIKE 'ps'
    """
    ps_query = """
        SELECT
            pl_name,
            hostname,
            sy_snum,
            sy_pnum,
            cb_flag,
            disc_pubdate
        FROM ps
    """
    sort_column = 'pl_name'

    if get_user_confirm("request schema, Y/N? "):
        ps_schema = tap_request(
            service_url=service_url,
            query=ps_schema_query,
            sync_type="sync"
        )

        print("Fetching schema...")
        ps_schema.to_csv("planets_schema.csv", index=False)
        print("Finished fetching schema.")

    print("Fetching requested 'planetary systems' table data...")
    ps_df = tap_request(
        service_url=service_url,
        query=ps_query,
        sync_type="async"
    )

    # clean data and show data before and after clean
    show_cleaning(ps_df, ps_df.pl_name, sort_column)
    ps_df = clean_data(ps_df, sort_column)
    show_cleaning(ps_df, ps_df.pl_name, sort_column)

    # append new data to planets table in database and update existing if changes
    upsert_planetary_data(ps_df)

    # print max last updated value from planets table
    print_last_updated("planets")
    print_table_updated_count("planets")


if __name__ == '__main__':
    main()
