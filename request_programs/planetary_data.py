"""gets planetary systems data from the NASA exoplanet archive
and updates the corrosponding dataframe.

'ps' shorthand refers to planetary systems"""

from database_helpers import (
    upsert_planetary_data,
    print_table_updated_count
)
from helpers import (
    get_user_confirm, tap_request,
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
            LIKE 'pscomppars'
    """
    ps_query = """
        SELECT
            pl_name,
            hostname,
            cb_flag,
            pl_controv_flag,
            discoverymethod,
            disc_instrument,
            pl_orbper,
            pl_masse,
            pl_rade,
            pl_insol,
            pl_eqt,
            disc_pubdate
        FROM ps
    """

    if get_user_confirm("request 'Planetary System Composite Data' schema, Y/N? "):
        ps_schema = tap_request(
            service_url=service_url,
            query=ps_schema_query,
            sync_type="sync"
        )

        print("Fetching schema...")
        ps_schema.to_csv("planets_schema.csv", index=False)
        print("Finished fetching schema.")

    print("Fetching requested 'Planetary System Composite Data' table data...")
    ps_df = tap_request(
        service_url=service_url,
        query=ps_query,
        sync_type="async"
    )

    # append new data to planets table in database and update existing if changes
    upsert_planetary_data(ps_df)

    # print max last updated value from planets table
    print_last_updated("planets")
    print_table_updated_count("planets")





if __name__ == '__main__':
    main()
