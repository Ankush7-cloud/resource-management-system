import streamlit as st
from signup1 import signup
from login2 import login
from home import home
from admin_dashboard1 import admin_dashboard
from user_management1 import user_management
from resource_management1 import resource_management
from insert_device import insert_device
from delete_device import delete_device
from update_device2 import update_device

# Set page configuration
st.set_page_config(page_title="Device Management App", layout="wide")

# ✅ Initialize session keys safely
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# ✅ If user is logged in
if st.session_state["username"]:
    st.sidebar.markdown(f"👤 Logged in as: {st.session_state.username}")

    # ✅ Handle logout
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.session_state["page"] = "Home"
        st.stop()

    role = st.session_state["role"]

    if role == "admin":
        menu = st.sidebar.selectbox("Admin Menu", [
            "Dashboard",
            "Insert Device",
            "Delete Device",
            "Update Device",
            "User Management",
            "Resource Management"
        ])
        st.session_state["page"] = menu
    else:
        menu = st.sidebar.selectbox("User Menu", [
            "User Management",
            "Resource Management"
        ])
        st.session_state["page"] = menu

# ✅ If not logged in
else:
    menu = st.sidebar.selectbox("Menu", ["Home", "Signup", "Login"])
    st.session_state["page"] = menu

# ✅ Page routing
page = st.session_state["page"]

if page == "Home":
    home()
elif page == "Signup":
    signup()
elif page == "Login":
    login()
elif page == "Dashboard":
    admin_dashboard()
elif page == "Insert Device":
    insert_device()
elif page == "Delete Device":
    delete_device()
elif page == "Update Device":
    update_device()
elif page == "User Management":
    user_management()
elif page == "Resource Management":
    resource_management()
