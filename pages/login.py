import os

import streamlit as st
from streamlit import session_state as ss
from oauthlib.oauth2 import WebApplicationClient
from modules.google import GOOGLE_CLIENT_ID, get_auth_url


# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # allows http for testing


st.set_page_config(
    page_title='Contact App',
    page_icon='./assets/icon/logo.png',
    layout='centered'
)


# Define session variables
if 'login_user_name' not in ss:
    ss.login_user_name = None
if 'is_login' not in ss:
    ss.is_login = False


if ss.is_login:
    st.switch_page('main.py')


client = WebApplicationClient(client_id=GOOGLE_CLIENT_ID)


def main():
    st.title('Login')

    if not ss.is_login:
        auth_url = get_auth_url(client)
        sc = f'''
        <a target="_self" href="{auth_url}">
            <img class="img-fluid" src="https://i.imgur.com/YTxsnUl.png" alt="streamlit">
        </a>
        '''
        with st.container(border=True):
            st.markdown(sc, unsafe_allow_html=True)
            st.markdown('')
            st.markdown('**Yttri Streamlit Contact App** by *YttriSoft Technologies*')


if __name__ == '__main__':
    main()
