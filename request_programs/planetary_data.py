"""gets planetary systems data from the NASA exoplanet archive
and updates the corrosponding dataframe.

'ps' shorthand refers to planetary systems"""
import pandas as pd
import sqlite3

from database_helpers import (
    print_table_updated_count,
    print_updates
)
from helpers import (
    get_user_confirm, print_last_updated,
    render_figlet, tap_request
)

DB_PATH = "database.db"
SERVICE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP"


def main():
    """collect updated data from archive and update the local database"""
    render_figlet("Planetary Data Request Program...")

    check_request_schema()

    planetary_sys_df = get_pscomppars_data()

    # note planets that no longer occur in NASA PSCompPars table
    mark_declassified_planets(planetary_sys_df)
    # append new data to planets table in database and update existing if changes
    upsert_planetary_data(planetary_sys_df)

    # print max last updated value from planets table
    print_last_updated("planets")
    print_table_updated_count("planets")
    print_updates("planets")

    print("\nPlanetary Data requests and updates complete.\n")


# Check schema request
# ********************************
def check_request_schema() -> None:
    """Get PsCompPars table schema if requested
    """
    if get_user_confirm("request 'Planetary System Composite Data' schema, Y/N? "):

        ps_schema_query = """
            SELECT *
            FROM TAP_SCHEMA.columns
            WHERE table_name
                LIKE 'pscomppars'
        """
        ps_schema = tap_request(
            service_url=SERVICE_URL,
            query=ps_schema_query,
            sync_type="sync"
        )

        print("Fetching schema...")
        ps_schema.to_csv("pscomppars_schema.csv", index=False)
        print("Finished fetching schema.")
# ********************************


# Get data
# ********************************
def get_pscomppars_data() -> pd.DataFrame:
    """make tap request for planetary data and
    return dataframe
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
        FROM pscomppars
    """
    
    print("Fetching requested 'Planetary System Composite Data' table data...")
    
    return tap_request(
        service_url=SERVICE_URL,
        query=ps_query,
        sync_type="async"
    )
# ********************************


# Mark declassified planets
# ********************************
def mark_declassified_planets(data_frame: pd.DataFrame) -> None:
    """Any planets that exist in the local database and are
    not within the planet names gathered from the tap request
    will be marked as declassified
    """
    confirmed_planets, placeholders = get_updated_planet_names(data_frame)
    changes = declassify_planets(confirmed_planets, placeholders)

    if not changes:
        return
    report_declassifications()

def get_updated_planet_names(data_frame: pd.DataFrame) -> tuple:
    """gets a list of names of all planets within the new data"""
    confirmed_planets = []

    for _, row in data_frame.iterrows():
        confirmed_planets.append(
            row['pl_name'],
    )
    return confirmed_planets, ', '.join('?' for _ in confirmed_planets)

def declassify_planets(confirmed_planets: list, placeholders: str) -> int:
    """Declassify any planets in table that are not in confirmed_planets
    and return number of planets declassified
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            UPDATE planets
               SET declassified = 1
             WHERE pl_name NOT IN ({placeholders})
               AND declassified != 1;
        """, confirmed_planets)

        cursor.execute("""
            SELECT changes();
        """)
        changes = cursor.fetchone()[0]

        print(f"Number of planets declassified since update: {changes}")
        return changes

def report_declassifications():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT *
                FROM planets
                WHERE declassified = 1
                    AND DATE(last_updated) = DATE('now');
        """)
        results = cursor.fetchall()
        print(f"Planets declassified today:")
        for result in results:
            print(result)
# ********************************


# Upsert into planets table
# ********************************
def upsert_planetary_data(data_frame: pd.DataFrame) -> None:
    """insert/update new pandas dataframe into the planets table"""
    data_to_insert = get_data_to_insert(data_frame)
    upsert_data(data_to_insert)

def get_data_to_insert(data_frame: pd.DataFrame) -> list:
    """turn dataframe rows into list of tuples"""
    data_to_insert = []

    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['pl_name'],
            row['hostname'],
            row['cb_flag'],
            row['pl_controv_flag'],
            row['discoverymethod'],
            row['disc_instrument'],
            row['pl_orbper'],
            row['pl_masse'],
            row['pl_rade'],
            row['pl_insol'],
            row['pl_eqt'],
            row['disc_pubdate']
        ))

    return data_to_insert

def upsert_data(data_to_insert: list) -> None:
    """carry out upsert"""
    with sqlite3.connect(DB_PATH) as conn:

        conn.executemany("""
            INSERT INTO planets (
                pl_name,
                hostname,
                cb_flag,
                cv_flag,
                disc_method,
                disc_instrument,
                orbit_period,
                mass,
                radius,
                insol_flux,
                equlib_temp,
                disc_pubdate,
                last_updated,
                declassified
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp, 0
            )
            ON CONFLICT(pl_name)
            DO UPDATE SET
                hostname = CASE
                    WHEN excluded.hostname != planets.hostname
                    THEN excluded.hostname
                    ELSE planets.hostname END,
                cb_flag = CASE
                    WHEN excluded.cb_flag != planets.cb_flag
                    THEN excluded.cb_flag
                    ELSE planets.cb_flag END,
                cv_flag = CASE
                    WHEN excluded.cv_flag != planets.cv_flag
                    THEN excluded.cv_flag
                    ELSE planets.cv_flag END,
                orbit_period = CASE
                    WHEN excluded.orbit_period != planets.orbit_period
                    THEN excluded.orbit_period
                    ELSE planets.orbit_period END,
                mass = CASE
                    WHEN excluded.mass != planets.mass
                    THEN excluded.mass
                    ELSE planets.mass END,
                radius = CASE
                    WHEN excluded.radius != planets.radius
                    THEN excluded.radius
                    ELSE planets.radius END,   
                insol_flux = CASE
                    WHEN excluded.insol_flux != planets.insol_flux
                    THEN excluded.insol_flux
                    ELSE planets.insol_flux END,
                equlib_temp = CASE
                    WHEN excluded.equlib_temp != planets.equlib_temp
                    THEN excluded.equlib_temp
                    ELSE planets.equlib_temp END,                                                                                       
                last_updated = current_timestamp,
                declassified = 0
            WHERE
                planets.cb_flag != excluded.cb_flag 
                OR planets.hostname != excluded.hostname
                OR planets.cv_flag != excluded.cv_flag
                OR planets.orbit_period != excluded.orbit_period
                OR planets.mass != excluded.mass
                OR planets.radius != excluded.radius
                OR planets.insol_flux != excluded.insol_flux
                OR planets.equlib_temp != excluded.equlib_temp;
    """, data_to_insert)
# ********************************


if __name__ == '__main__':
    main()
