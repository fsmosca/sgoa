import streamlit as st


REDIRECT_URI = 'http://localhost:8501/callback'
GOOGLE_CLIENT_ID = st.secrets["CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
