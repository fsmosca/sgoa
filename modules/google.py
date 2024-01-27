"""Manages Google Users' authentication.

1. Register our App in google at https://console.cloud.google.com/. We
   need to create a project, etc.
2. Get the url from google, that will be used to prompt the users to log
   into our App. A web page will be shown to the users to grant our App to
   access the users account info, such as name and email, and more depending
   on the scope that our App needs in order for it to function as intended.
3. Once the users have logged in, our App can now access the users info.
"""


import requests
import streamlit as st


REDIRECT_URI = 'https://risoftcontact.streamlit.app/auth'
GOOGLE_CLIENT_ID = st.secrets["CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


def get_google_provider_cfg():
    """Gets Google's OpenID Connect configuration."""
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def get_auth_url(client):
    """Gets the url to prompt the users to log in."""
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    return client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=REDIRECT_URI,
        scope=["openid", "email", "profile"],
    )


def exchange_code(code, client):
    """Exchange authorization code for user's access token."""
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Construct the full redirect URI
    full_redirect_uri = REDIRECT_URI + '?code=' + code

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=full_redirect_uri,
        redirect_url=REDIRECT_URI,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    tokens = token_response.json()
    return tokens


def get_user_info(token):
    """The users' token allow this app to get the users' info."""
    google_provider_cfg = get_google_provider_cfg()
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    userinfo_response = requests.get(
        userinfo_endpoint,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    return userinfo_response.json()
