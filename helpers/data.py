from io import StringIO

from astroquery.utils.tap.core import TapPlus
import pandas as pd

from helpers import get_last_csv, get_user_confirm
from plots import save_figures
from save import save_dated_data_csv

def main():
    tap_service = TapPlus(url="https://exoplanetarchive.ipac.caltech.edu/TAP")
    schema_query = "SELECT * FROM TAP_SCHEMA.columns WHERE table_name LIKE 'stellarhosts'"
    stellar_hosts_query = "SELECT sy_name, sy_snum, sy_pnum FROM stellarhosts"

    if get_user_confirm("request schema, Y/N? "):
        stellar_hosts_schema = tap_request(tap_service=tap_service, query=schema_query, sync_type="sync")
        stellar_hosts_schema.to_csv('stellar_hosts_schema.csv', index=False)
        print("Finished fetching schema")
    
    print("Fetching requested stellar hosts table data...")
    stellar_hosts_df = tap_request(tap_service=tap_service, query=stellar_hosts_query, sync_type="async")
    print("Finished fetching stellar hosts data")

    stellar_hosts_df = clean_data(stellar_hosts_df, show_data=True)

    stellar_hosts_df.to_csv('stellar_hosts.csv', index=False)
    if is_data_different():
        save_dated_csv(stellar_hosts_df)

        # create data frames for figures
        systems_df = create_systems_df(stellar_hosts_df)
        star_series = create_star_series(systems_df)
        planet_to_star_df = create_planet_to_star_df(systems_df)

        save_figures(systems_df=systems_df, star_series=star_series, planet_to_star_df=planet_to_star_df)

    else:
        print("Data has not changed from last call")
    print("Ending program...")


def tap_request(tap_service: TapPlus, query: str, sync_type: str):
    if not sync_type in ["async", "sync"]:
        raise ValueError("sync_type must be 'async' or 'sync'")
    
    if sync_type == "async":
        job = tap_service.launch_job_async(query)
    else:
        job = tap_service.launch_job(query)

    result_csv = job.get_results().to_pandas().to_csv(index=False)
    return pd.read_csv(StringIO(result_csv))

def clean_data(data: pd.DataFrame, show_data: bool = False) -> pd.DataFrame:
    """organise data alphabetaically
    :param show_data: if True will print data info before and after cleaning"""
    data = organise_data(data)

    if show_data:
        show_duplicate_data(data)
    data = drop_duplicate_data(data)
    if show_data:
        show_duplicate_data(data)
    
    return data


def organise_data(data):
    return data.sort_values(by=['sy_name'])

def show_duplicate_data(data):
    print(f"Rows in data: {data.sy_name.count().sum()}\n")
    duplicates = data.duplicated(subset=['sy_name'], keep='first')
    print(f"Number of non-duplicate systems: {data.sy_name.count().sum() - duplicates.sum()}")
    print(f"Number of duplicate systems: {duplicates.sum()}")
    print(f"Columns with null values:\n{data.isnull().sum()}")

def drop_duplicate_data(data):
    return data.drop_duplicates()


def is_data_different() -> bool:
    """checks if data is different from the last time it was gathered"""
    last = pd.read_csv(get_last_csv("stellar_hosts", "static/"))
    new = pd.read_csv("stellar_hosts.csv")

    if new.equals(last):
        return False
    return True
    
def save_dated_csv(data: pd.DataFrame) -> None:
    print("creating new folder")
    save_dated_data_csv(data, "stellar_hosts")

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