import streamlit as st
from db import init_db
import random

def generate_unique_employee_id(conn, role):
    
    existing_ids = conn.execute("SELECT employee_id FROM users").fetchall()
    used_ids = {row[0] for row in existing_ids if row[0] is not None}

    if role == "admin":
        possible_ids = {f"A{str(i).zfill(3)}" for i in range(1, 21)}
    else:
        possible_ids = {str(i).zfill(3) for i in range(1, 21)}

    available_ids = list(possible_ids - used_ids)

    return random.choice(available_ids) if available_ids else None

def signup():
    st.title("📝 Signup")

    conn = init_db()

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
                return

            
            user_exists = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user_exists:
                st.error("❌ Username already exists.")
                return

            
            emp_id = generate_unique_employee_id(conn, role)
            if not emp_id:
                st.error("❌ No more Employee IDs available for this role.")
                return

            
            conn.execute(
                "INSERT INTO users (username, email, password, role, employee_id) VALUES (?, ?, ?, ?, ?)",
                (username, email, password, role, emp_id)
            )
            conn.commit()
            st.success("✅ Account created successfully. Please log in.")
