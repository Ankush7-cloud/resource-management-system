import duckdb

def init_db():
    conn = duckdb.connect("app_data.db")

    # Create users table (initial definition)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT,
            password TEXT,
            role TEXT CHECK(role IN ('admin', 'user'))
        )
    """)

    # Check and add 'employee_id' to users table if not present
    try:
        user_columns = conn.execute("PRAGMA table_info(users);").fetchall()
        user_column_names = [col[1] for col in user_columns]
        if "employee_id" not in user_column_names:
            conn.execute("ALTER TABLE users ADD COLUMN employee_id TEXT;")
            print("✅ Added 'employee_id' column to users table.")
    except Exception as e:
        print(f"❌ Failed to add 'employee_id' column: {e}")

    # Create devices table without is_shared first
    conn.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            service_tag TEXT PRIMARY KEY,
            employee_id TEXT,
            device_type TEXT,
            memory TEXT
        )
    """)

    # Check and add 'is_shared' to devices table if not present
    try:
        device_columns = conn.execute("PRAGMA table_info(devices);").fetchall()
        device_column_names = [col[1] for col in device_columns]
        if "is_shared" not in device_column_names:
            conn.execute("ALTER TABLE devices ADD COLUMN is_shared TEXT;")
            print("✅ Added 'is_shared' column to devices table.")
    except Exception as e:
        print(f"❌ Failed to add 'is_shared' column: {e}")
        
    return conn
