import streamlit as st
from db import init_db
import pandas as pd

def admin_dashboard():
    st.title("Admin Dashboard - Device Inventory")
    conn = init_db()

    # Fetch all devices including is_shared column
    try:
        rows = conn.execute("SELECT * FROM devices").fetchall()
        df = pd.DataFrame(rows, columns=["Service Tag", "Employee ID", "Device Type", "Memory", "Is Shared"])
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading devices table: {e}")
