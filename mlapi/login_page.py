# # login_page.py
# # login_page.py
# import streamlit as st
# from auth import register_user, login_user

# def login_page():
#     st.title("🔐 Sign in or Register")

#     tab1, tab2 = st.tabs(["Login", "Register"])

#     with tab1:
#         st.subheader("Login")
#         email = st.text_input("Email", key="login_email")
#         password = st.text_input("Password", type="password", key="login_password")
#         if st.button("Login"):
#             ok, result = login_user(email, password)
#             if ok:
#                 st.session_state["logged_in"] = True
#                 st.session_state["user"] = result
#                 st.success("Login successful")
#                 st.experimental_rerun()
#             else:
#                 st.error(result)

#     with tab2:
#         st.subheader("Register")
#         username = st.text_input("Username", key="reg_username")
#         email_r = st.text_input("Email", key="reg_email")
#         password_r = st.text_input("Password", type="password", key="reg_password")
#         if st.button("Register"):
#             ok, res = register_user(username, email_r, password_r)
#             if ok:
#                 st.success("Registered successfully. Please login.")
#             else:
#                 st.error(res)


# login_page.py
import streamlit as st
from auth import register_user, login_user

def login_page():
    st.title("🔐 Sign in or Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------------- LOGIN TAB ----------------
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            ok, result = login_user(email, password)

            if ok:
                st.session_state["logged_in"] = True
                st.session_state["user"] = result
                st.success("Login successful")

                # FIX: Use st.rerun() (new Streamlit API)
                st.rerun()

            else:
                st.error(result)

    # ---------------- REGISTER TAB ----------------
    with tab2:
        st.subheader("Register")
        username = st.text_input("Username", key="reg_username")
        email_r = st.text_input("Email", key="reg_email")
        password_r = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register"):
            ok, res = register_user(username, email_r, password_r)

            if ok:
                st.success("Registered successfully. Please login.")
            else:
                st.error(res)
