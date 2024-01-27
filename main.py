import os

import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from assets.data.sample import data


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

if 'df' not in ss:
    ss.df = pd.DataFrame(data, columns=['Name', 'Email', 'Phone Number'])

if 'search_df' not in ss:
    ss.search_df = pd.DataFrame(columns=['Name', 'Email', 'Phone Number'])

if not ss.is_login:
    st.switch_page('./pages/login.py')


def log_out_cb():
    """Clears the query params and session states."""
    st.query_params.clear()
    for key in list(ss.keys()):
        del ss[key]


def search_contacts(df, search_text):
    df = df.astype(str)
    if search_text == '':
        return pd.DataFrame(columns=['Name', 'Email', 'Phone Number'])
    return df[df.apply(lambda row: row.str.contains(
        search_text, case=False, na=False, regex=True)).any(axis=1)]


def main():
    st.title('Yttri Contact')

    st.markdown('''
        Welcome to **Yttri Contact App** - your gateway to **effortless
        connectivity**!
    ''')

    # Menu
    with st.sidebar:
        # Logout
        st.write(f"Welcome {ss.login_user_name}.")
        st.button('Log Out', on_click=log_out_cb)

    # Content
    with st.container(border=True):
        st.markdown('<h3 style="color: blue;">Contacts</h3>', unsafe_allow_html=True)
        st.dataframe(ss.df, hide_index=True, use_container_width=True)


if __name__ == '__main__':
    main()
