"""gets stellar data from the NASA exoplanet archive
and updates the corrosponding dataframe.

's' shorthand refers to stellar"""

import pandas as pd

from database_helpers import (
    upsert_stellar_data,
    update_stellar_spectypes
)
from helpers import (
    get_user_confirm,
    tap_request, clean_data,
    show_cleaning, print_last_updated,
    render_figlet
)

# *******
def main():
    """collect updated data from archive and update the local database"""
    render_figlet("Stellar Data Request Program...")

    service_url = "https://exoplanetarchive.ipac.caltech.edu/TAP"

    update_stellar_schema(service_url)

    update_stellarhosts_table(service_url)

    update_sh_table_spectype(service_url)

    # print max last updated value from stellar table
    print_last_updated("stellar")

    print("Stellar Data requests and updates complete")
# *******


# *******
def update_stellar_schema(service_url: str) -> None:
    """get stellar hosts table schema"""

    if not get_user_confirm("request schema, Y/N? "):
        return
    
    schema = request_stellar_schema(service_url)
    save_schema(schema)

    print("Finished fetching schema")
    return


def request_stellar_schema(service_url: str) -> pd.DataFrame:
    """request stellar hosts table schema"""

    query = """
        SELECT *
        FROM TAP_SCHEMA.columns
        WHERE table_name
        LIKE 'stellarhosts'
    """

    print("Fetching schema...")
    return tap_request(
        service_url=service_url,
        query=query,
        sync_type="sync"
    )

def save_schema(schema: pd.DataFrame) -> None:
    schema.to_csv('stellar_hosts_schema.csv', index=False)
# *******


# *******
def update_stellarhosts_table(service_url: str) -> None:
    """request stellarhosts table and upsert relevant data
    to stellarhosts table in local database
    """
    
    df = get_stellar_data(service_url)

    df = clean_gathered_data(df)

    # append new data to stellar_hosts table in database and update existing if changes
    upsert_stellar_data(df)


def get_stellar_data(service_url: str) -> pd.DataFrame:
    query = """
        SELECT
            sy_name,
            hostname
        FROM stellarhosts
    """

    # get stellar hosts table data
    print("Fetching requested 'stellar hosts' table data...")
    return tap_request(
        service_url=service_url,
        query=query,
        sync_type="async"
    )


def clean_gathered_data(df: pd.DataFrame) -> pd.DataFrame:
    """show dataframe cleaning and clean data"""

    sort_column = 'hostname'
    # clean data and show data before and after clean
    show_cleaning(df, df.hostname, sort_column)
    df = clean_data(df, sort_column)
    show_cleaning(df, df.hostname, sort_column)
    return df
# *******


# *******
def update_sh_table_spectype(service_url: str) -> None:
    """request spectype from NASA stellarhosts table
    sort data and asign to corrosponding hostname in
    local stellarhosts table
    """
    df = get_spectypes(service_url)

    df = clean_spectypes_df(df)

    update_stellar_spectypes(df)


def get_spectypes(service_url: str) -> pd.DataFrame:
    query = """
        SELECT
            hostname,
            st_spectype
        FROM stellarhosts
    """

    print("Fetching 'stellarhosts' spectral data...")
    # get stellar hosts spectral types
    return tap_request(
        service_url=service_url,
        query=query,
        sync_type="async"
    )


def clean_spectypes_df(df: pd.DataFrame) -> pd.DataFrame:
    print(f"after collection: {df.count()}")

    df = df.dropna()
    print(f"after drop na: {df.count()}")

    df = df.drop_duplicates(subset=['hostname'], keep='first')
    print(f"after drop dups: {df.count()}")
    return df
# *******

if __name__ == '__main__':
    main()
