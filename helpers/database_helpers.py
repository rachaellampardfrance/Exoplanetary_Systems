"""Helper functions to read collected data into database tables"""

import sqlite3
import pandas as pd

DB_PATH = "database.db"

def upsert_planetary_data(data_frame: pd.DataFrame) -> None:

    """insert/update new pandas dataframe into the planetary_systems table"""
    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['pl_name'],
            row['hostname'],
            row['sy_snum'],
            row['sy_pnum'],
            row['cb_flag'],
            row['disc_pubdate']
        ))

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany("""
            INSERT INTO planetary_systems (
                pl_name,
                hostname,
                sy_snum,
                sy_pnum,
                cb_flag,
                disc_pubdate,
                last_updated
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, current_timestamp
            )
            ON CONFLICT(pl_name)
            DO UPDATE SET
                hostname = CASE
                    WHEN excluded.hostname != planetary_systems.hostname
                    THEN excluded.hostname
                    ELSE planetary_systems.hostname END,
                sy_snum = CASE
                    WHEN excluded.sy_snum != planetary_systems.sy_snum
                    THEN excluded.sy_snum
                    ELSE planetary_systems.sy_snum END,
                sy_pnum = CASE
                    WHEN excluded.sy_pnum != planetary_systems.sy_pnum
                    THEN excluded.sy_pnum
                    ELSE planetary_systems.sy_pnum END,
                cb_flag = CASE
                    WHEN excluded.cb_flag != planetary_systems.cb_flag
                    THEN excluded.cb_flag
                    ELSE planetary_systems.cb_flag END,
                last_updated = current_timestamp
            WHERE
                planetary_systems.sy_snum != excluded.sy_snum
                OR planetary_systems.sy_pnum != excluded.sy_pnum
                OR planetary_systems.cb_flag != excluded.cb_flag 
                OR planetary_systems.hostname != excluded.hostname;
    """, data_to_insert)

def upsert_stellar_hosts_data(data_frame: pd.DataFrame) -> None:
    """insert/update new pandas dataframe into the stellar_hosts table"""
    
    data_to_insert = []
    for _, row in data_frame.iterrows():
        data_to_insert.append((
            row['sy_name'],
            row['sy_snum'],
            row['sy_pnum'],
        ))

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany("""
            INSERT INTO stellar_hosts (
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
                    WHEN excluded.sy_name != stellar_hosts.sy_name
                    THEN excluded.sy_name
                    ELSE stellar_hosts.sy_name END,
                sy_snum = CASE
                    WHEN excluded.sy_snum != stellar_hosts.sy_snum
                    THEN excluded.sy_snum
                    ELSE stellar_hosts.sy_snum END,
                sy_pnum = CASE
                    WHEN excluded.sy_pnum != stellar_hosts.sy_pnum
                    THEN excluded.sy_pnum
                    ELSE stellar_hosts.sy_pnum END,
                last_updated = current_timestamp
            WHERE
                stellar_hosts.sy_snum != excluded.sy_snum
                OR stellar_hosts.sy_pnum != excluded.sy_pnum;
    """, data_to_insert)
