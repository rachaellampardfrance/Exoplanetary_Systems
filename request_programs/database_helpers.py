"""Helper functions to read collected data into database tables"""

import sqlite3
import pandas as pd

DB_PATH = "database.db"

def mark_declassified_planets(data_frame: pd.DataFrame) -> None:
    """Any planets that exist in the local database and are
    not within the planet names gathered from the tap request
    will be marked as declassified
    """
    classified_planets = []
    for _, row in data_frame.iterrows():
        classified_planets.append(
            row['pl_name'],
    )
    placeholders = ', '.join('?' for _ in classified_planets)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(f"""
            UPDATE planets
            SET declassified = 1
            WHERE pl_name NOT IN ({placeholders});
        """, classified_planets)


def upsert_planetary_data(data_frame: pd.DataFrame) -> None:

    """insert/update new pandas dataframe into the planets table"""
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


def upsert_systems_data(data_frame: pd.DataFrame) -> None:
    """insert/update new pandas dataframe into the systems table"""
    
    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['sy_name'],
            row['sy_snum'],
            row['sy_pnum'],
        ))

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""
            INSERT INTO systems (
                sy_name,
                sy_snum,
                sy_pnum,
                last_updated
            )
            VALUES (
                ?, ?, ?, current_timestamp
            )
            ON CONFLICT(sy_name)
            DO UPDATE SET
                sy_name = CASE
                    WHEN excluded.sy_name != systems.sy_name
                    THEN excluded.sy_name
                    ELSE systems.sy_name END,
                sy_snum = CASE
                    WHEN excluded.sy_snum != systems.sy_snum
                    THEN excluded.sy_snum
                    ELSE systems.sy_snum END,
                sy_pnum = CASE
                    WHEN excluded.sy_pnum != systems.sy_pnum
                    THEN excluded.sy_pnum
                    ELSE systems.sy_pnum END,
                last_updated = current_timestamp
            WHERE
                systems.sy_snum != excluded.sy_snum
                OR systems.sy_pnum != excluded.sy_pnum;
    """, data_to_insert)


def upsert_stars_data(data_frame: pd.DataFrame) -> None:
    """insert/update new pandas dataframe into the systems table"""
    
    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['sy_name'],
            row['hostname'],
        ))

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""
            INSERT INTO stars (
                sy_name,
                hostname,
                last_updated
            )
            VALUES (
                ?, ?, current_timestamp
            )
            ON CONFLICT(hostname)
            DO UPDATE SET
                sy_name = CASE
                    WHEN excluded.sy_name != stars.sy_name
                    THEN excluded.sy_name
                    ELSE stars.sy_name END,
                last_updated = current_timestamp
            WHERE
                stars.sy_name != excluded.sy_name;
    """, data_to_insert)

def update_stars_spectypes(data_frame: pd.DataFrame) -> None:
    """update stars table with new spectral types"""

    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['st_spectype'],
            row['hostname'],
        ))

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""
            UPDATE stars
            SET st_spectype = ?
            WHERE
                stars.hostname == ?;
    """, data_to_insert)


def get_last_updated(table) -> str:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        c.execute("""
            SELECT MAX(last_updated)
            FROM {}
        """.format(table))

        return c.fetchone()

 
def get_systems_db_data():
    with sqlite3.connect(DB_PATH) as conn:
        # c = conn.cursor()
        
        return pd.read_sql_query("SELECT * FROM systems", conn)

def print_table_updated_count(table: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        today = c.execute("SELECT DATE('now')").fetchone()[0]

        c.execute(f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE DATE(last_updated) = '{today}';
        """)

        result = c.fetchone()
        count = result[0] if result else 0

        print(f"Todays new updates to {table}: {count}")