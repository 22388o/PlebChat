import yaml

import streamlit as st
import streamlit_authenticator as stauth

import logging
log = logging.getLogger()

from src.mistral_wrapper import mistral_wrapper




def main():
    log.debug("Starting main()")

    st.set_page_config(
        page_title="Pleb AI demos", layout="centered", initial_sidebar_state="auto"
    )

    with open("./auth.yaml") as file:
        config = yaml.load(file, Loader=yaml.loader.SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )

    # https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/
    # https://github.com/mkhorasani/Streamlit-Authenticator?ref=blog.streamlit.io
    authenticator.login("ACCESS RESTRICTED", "main")

    if st.session_state["authentication_status"]:
        mistral_wrapper()


    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")

    # elif st.session_state["authentication_status"] is None:
        # st.warning("Please enter your username and password")




    #     st.caption(f'Logged in as `{st.session_state["username"]}`')
    #     cols = st.columns((1, 1, 1))
    #     with cols[0]:
    #         authenticator.logout("Logout", "main")
    #     with cols[1]:
    #         st.button(SETTINGS_PAGE.name, on_click=launch_app, args=(SETTINGS_PAGE,))
    
    #     st.caption(f"running version {VERSION}")
    # else:

    #     show_navigation(st.session_state.running_app.name)
    #     st.session_state.running_app.callback()
