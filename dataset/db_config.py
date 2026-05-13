from sqlalchemy import create_engine

# Centralized connection details
DB_USER = "newuser"
DB_PASS = "tarit"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "testdb"

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_engine():
    return create_engine(DB_URL)


