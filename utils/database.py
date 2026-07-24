import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "vanlang_analysis",
    "user": "postgres",
    "password": "123456"
}


def get_connection():
    """
    Create and return a PostgreSQL connection.
    """

    conn = psycopg2.connect(**DB_CONFIG)

    return conn


if __name__ == "__main__":

    try:
        conn = get_connection()

        print("=" * 50)
        print("PostgreSQL connection established successfully!")
        print("=" * 50)

        cursor = conn.cursor()

        cursor.execute("SELECT version();")

        version = cursor.fetchone()[0]

        print(f"Database Version: {version}")

        cursor.close()
        conn.close()

        print("Connection closed.")

    except Exception as e:

        print("=" * 50)
        print("Failed to connect to PostgreSQL.")
        print("=" * 50)
        print(e)