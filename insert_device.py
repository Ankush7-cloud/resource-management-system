import streamlit as st
from db import init_db

def insert_device():
    st.title("Insert New Device")
    conn = init_db()

    service_tag = st.text_input("Service Tag")
    employee_id = st.text_input("Employee ID")
    device_type = st.selectbox("Device Type", ["GPU", "Desktop"])
    memory = st.text_input("Memory")
    is_shared = st.radio("Is Shared", ["Yes", "No"])

    if st.button("Insert Device"):
        if not service_tag or not employee_id or not memory:
            st.warning("Please fill in all the fields.")
        else:
            try:
                conn.execute(
                    "INSERT INTO devices (service_tag, employee_id, device_type, memory, is_shared) VALUES (?, ?, ?, ?, ?)",
                    (service_tag, employee_id, device_type, memory, is_shared)
                )
                st.success("✅ Device inserted successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
