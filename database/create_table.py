from pathlib import Path

from utils.database import get_connection


SCHEMA_FILE = Path(__file__).parent / "schema.sql"


def create_tables():
    """
    Create all database tables from schema.sql.
    """

    conn = get_connection()
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        sql = f.read()

    cursor.execute(sql)

    conn.commit()

    cursor.close()
    conn.close()

    print("=" * 50)
    print("All tables created successfully.")
    print("=" * 50)


if __name__ == "__main__":

    try:
        create_tables()

    except Exception as e:
        print("Failed to create tables.")
        print(e)