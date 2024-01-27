import streamlit as st
from streamlit import session_state as ss
from oauthlib.oauth2 import WebApplicationClient
from modules.google import (
    GOOGLE_CLIENT_ID,
    exchange_code, get_user_info
)


if 'login_user_name' not in ss:
    ss.login_user_name = None

if 'is_login' not in ss:
    ss.is_login = False

if ss.is_login:
    st.query_params.clear()
    st.switch_page('main.py')


client = WebApplicationClient(client_id=GOOGLE_CLIENT_ID)

# Get the params in the path
qparams = st.query_params.to_dict()

# If qparams is not empty, this is a redirection from google.
if qparams:
    code = qparams.get("code")
    if code:
        # Retrieve Google account tokens from logged users.
        tokens = exchange_code(code, client)
        access_token = tokens["access_token"]
        user_info = get_user_info(access_token)
        ss.login_user_name = user_info['given_name']
        ss.is_login = True
        st.rerun()  # to redirect to main page when is_login is true

# Else goto login page as this is not a formal redirection.
else:
    st.switch_page('./pages/login.py')
