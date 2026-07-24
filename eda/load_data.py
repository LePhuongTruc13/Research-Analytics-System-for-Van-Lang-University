import pandas as pd

from utils.database import get_connection


def load_papers():
    """
    Load papers table from PostgreSQL.
    """

    conn = get_connection()

    query = """
        SELECT *
        FROM papers
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_authors():
    """
    Load authors table from PostgreSQL.
    """

    conn = get_connection()

    query = """
        SELECT *
        FROM authors
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_institutions():
    """
    Load institutions table from PostgreSQL.
    """

    conn = get_connection()

    query = """
        SELECT *
        FROM institutions
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_paper_author():
    """
    Load paper_author table from PostgreSQL.
    """

    conn = get_connection()

    query = """
        SELECT *
        FROM paper_author
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_author_institution():
    """
    Load author_institution table from PostgreSQL.
    """

    conn = get_connection()

    query = """
        SELECT *
        FROM author_institution
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df