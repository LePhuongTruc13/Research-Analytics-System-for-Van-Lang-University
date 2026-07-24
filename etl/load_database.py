from pathlib import Path

import pandas as pd

from utils.database import get_connection
from utils.path import TRANSFORMED_DATA_DIR


TABLE_FILES = {
    "papers": "papers.csv",
    "authors": "authors.csv",
    "institutions": "institutions.csv",
    "paper_author": "paper_author.csv",
    "author_institution": "author_institution.csv"
}


def load_table(conn, table_name, csv_file):
    """
    Load one CSV file into a PostgreSQL table.
    """

    file_path = TRANSFORMED_DATA_DIR / csv_file

    df = pd.read_csv(file_path)

    cursor = conn.cursor()

    columns = ",".join(df.columns)

    placeholders = ",".join(["%s"] * len(df.columns))

    sql = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
    """

    cursor.executemany(
        sql,
        df.values.tolist()
    )

    conn.commit()

    cursor.close()

    print(f"Loaded {len(df)} rows into '{table_name}'.")


def main():

    conn = get_connection()

    for table, file in TABLE_FILES.items():

        load_table(conn, table, file)

    conn.close()

    print("\nAll CSV files loaded successfully.")


if __name__ == "__main__":

    main()