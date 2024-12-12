import sqlite3
import pandas as pd

def update_database(db_path: str, table: str, df: pd.DataFrame, column_name: str) -> None:
    """
    :param db_path: 'str' path to database
    :param table: 'str' name for table within database
    :param df: 'pd.DataFrame' of data to check and append to database table
    :param column_name: 'str' name of column to search by
    """
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        if _table_exists(cursor, table):
            existing: list = _get_all_column_values(cursor, column_name)
            updates_df = _only_updates_df(df, existing)
            _commit_update_database(connection, table, updates_df)
        else:
             _commit_update_database(connection, table, df)

def _table_exists(cursor, table):
    cursor.execute("SELECT name FROM sqlite_master WHERE type= 'table' AND name = ?", (table,))
    existing_table = cursor.fetchone()
    if existing_table:
         return True
    return False

def _get_all_column_values(cursor: str, column_name: str) -> list:
    """:returns: 'list' of column values"""
    cursor.execute("""SELECT {} FROM planetary_systems""".format(column_name))
    names = cursor.fetchall()

    return [name[0] for name in names]

def _only_updates_df(df: pd.DataFrame, existing_db_values: list) -> pd.DataFrame:
        """:returns: 'pd.DataFrame' from df with only new data'"""
        return df[~df['pl_name'].isin(existing_db_values)]

def _commit_update_database(connection: sqlite3.Connection, table: str, updates_df: pd.DataFrame) -> None:
    """updates specified table with updated data, at specified database path"""
    updates_df.to_sql(table, connection, if_exists='append', index=False)

# for new_data: if in """SELECT * from planetary_systems WHERE pl_name = {new_data['pl_name']}"""
    #  if datas not the same (pl_name, cb_flag (all but datepull))
        # update
    # else if: new_data['pl_name'] not in db, add to db