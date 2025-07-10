import streamlit as st
from db import init_db

def delete_device():
    st.title("🗑 Delete Device")

    conn = init_db()

    devices = conn.execute("SELECT service_tag, employee_id FROM devices").fetchall()

    if not devices:
        st.info("ℹ No devices found to delete.")
        return

    service_tags = [d[0] for d in devices]
    selected_tag = st.selectbox("Select Service Tag to Delete", service_tags)

    if st.button("Delete Device"):
        try:
            # Get employee_id for this service_tag
            employee_id = conn.execute("SELECT employee_id FROM devices WHERE service_tag = ?", (selected_tag,)).fetchone()
            if employee_id:
                employee_id = employee_id[0]

                # Delete from devices table
                conn.execute("DELETE FROM devices WHERE service_tag = ?", (selected_tag,))

                # Delete from users table
                conn.execute("DELETE FROM users WHERE employee_id = ?", (employee_id,))

                st.success(f"✅ Device '{selected_tag}' and user with Employee ID '{employee_id}' deleted successfully.")
            else:
                st.error("❌ Could not find Employee ID for selected device.")
        except Exception as e:
            st.error(f"❌ Error deleting device or user: {e}")
