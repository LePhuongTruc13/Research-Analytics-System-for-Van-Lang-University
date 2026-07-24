import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",  
    "user": "postgres",
    "password": "123456"
}

DATABASE_NAME = "vanlang_analysis"


def create_database():

    conn = psycopg2.connect(**DB_CONFIG)

    conn.autocommit = True

    cursor = conn.cursor()

    # Check database exists
    cursor.execute(
        """
        SELECT 1
        FROM pg_database
        WHERE datname = %s
        """,
        (DATABASE_NAME,)
    )

    exists = cursor.fetchone()

    if exists:

        print(f"Database '{DATABASE_NAME}' already exists.")

    else:

        cursor.execute(
            f'CREATE DATABASE "{DATABASE_NAME}"'
        )

        print(f"Database '{DATABASE_NAME}' created successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":

    try:

        create_database()

    except Exception as e:

        print("Error creating database:")
        print(e)