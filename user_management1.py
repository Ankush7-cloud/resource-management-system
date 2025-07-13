import streamlit as st
from db import init_db
import random

def get_all_used_ids(conn):
    
    ids = conn.execute("SELECT employee_id FROM users").fetchall()
    return {i[0] for i in ids if i[0]}

def generate_unique_employee_id(conn, role):
    
    used_ids = get_all_used_ids(conn)
    if role == 'admin':
        possible_ids = {f"A{str(i).zfill(3)}" for i in range(1, 21)}
    else:
        possible_ids = {str(i).zfill(3) for i in range(1, 21)}

    available_ids = list(possible_ids - used_ids)
    return random.choice(available_ids) if available_ids else None

def user_management():
    st.title("👥 User Management")

    conn = init_db()

    if 'username' not in st.session_state or 'role' not in st.session_state:
        st.warning("⚠ Please log in to view this page.")
        return

    current_user = st.session_state['username']
    current_role = st.session_state['role']

    
    result = conn.execute("SELECT employee_id FROM users WHERE username = ?", (current_user,)).fetchone()
    current_emp_id = result[0] if result else None

    
    if not current_emp_id:
        new_id = generate_unique_employee_id(conn, current_role)
        if new_id:
            conn.execute("UPDATE users SET employee_id = ? WHERE username = ?", (new_id, current_user))
            conn.commit()
        else:
            st.error("❌ No available Employee IDs left for your role.")

    st.subheader("📋 Registered Users")

    if current_role == 'admin':
        
        rows = conn.execute("SELECT username, email, employee_id, role FROM users").fetchall()
        data = [
            {
                "Username": r[0],
                "Email ID": r[1],
                "Employee ID": r[2],
                "Role": r[3]
            } for r in rows
        ]
        st.dataframe(data, use_container_width=True)
    else:
        
        row = conn.execute("SELECT username, email, employee_id, role FROM users WHERE username = ?", (current_user,)).fetchone()
        if row:
            data = [{
                "Username": row[0],
                "Email ID": row[1],
                "Employee ID": row[2],
                "Role": row[3]
            }]
            st.dataframe(data, use_container_width=True)
        else:
            st.error("❌ Failed to load your data.")
