import streamlit as st
from db import init_db

def login():
    st.title("Login")
    conn = init_db()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    selected_role = st.selectbox("Login As", ["admin", "user"])

    if st.button("Login"):
        result = conn.execute(
            "SELECT role FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        if result:
            actual_role = result[0]
            if selected_role == actual_role:
                st.session_state["username"] = username
                st.session_state["role"] = actual_role
                # Navigate to the right page directly
                if actual_role == "admin":
                    st.session_state["page"] = "Dashboard"
                else:
                    st.session_state["page"] = "Resource Management"
                st.success(f"Login successful as {actual_role}!")
            else:
                st.error(f"Access denied. You are registered as '{actual_role}', not '{selected_role}'.")
        else:
            st.error("Invalid credentials")
