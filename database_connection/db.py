import psycopg2

try:
    # Use 'with' for the connection to handle closing automatically
    with psycopg2.connect(
        host="localhost",
        database="testdb",
        user="newuser",     # Ensure this matches the DB user you created
        password="tarit",
        port=5432
    ) as conn:
        
        # Use 'with' for the cursor
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print(f"Connected to: {cur.fetchone()}")

except Exception as e:
    print(f"Error connecting to database: {e}")

# Connection is closed automatically here!