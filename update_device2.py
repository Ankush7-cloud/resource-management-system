import streamlit as st
from db import init_db

def update_device():
    st.title("🛠 Update Device Info")

    conn = init_db()

    
    service_tags = conn.execute("SELECT service_tag FROM devices").fetchall()
    service_tags = [tag[0] for tag in service_tags]

    if not service_tags:
        st.warning("⚠ No devices available to update.")
        return

    selected_tag = st.selectbox("Select Service Tag to Update", service_tags)

    
    device = conn.execute("SELECT employee_id, device_type, memory, is_shared FROM devices WHERE service_tag = ?", (selected_tag,)).fetchone()

    if device:
        employee_id = st.text_input("Employee ID", value=device[0])
        device_type = st.selectbox("Device Type", ["Desktop", "GPU"], index=["Desktop", "GPU"].index(device[1]))
        memory = st.text_input("Memory", value=device[2])
        is_shared = st.selectbox("Is Shared?", ["Yes", "No"], index=["Yes", "No"].index(device[3]) if device[3] else 1)

        if st.button("Update Device"):
            conn.execute("""
                UPDATE devices
                SET employee_id = ?, device_type = ?, memory = ?, is_shared = ?
                WHERE service_tag = ?
            """, (employee_id, device_type, memory, is_shared, selected_tag))

            st.success("✅ Device updated successfully.")
    else:
        st.error("Device not found.")
