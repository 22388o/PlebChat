import os
import streamlit as st

import yaml
from yaml.loader import SafeLoader

import logging
log = logging.getLogger()

from src.VERSION import VERSION






def show_api_keys_entry():
    with open("./auth.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)


    with st.expander("API Keys"):
        try:
            key = config["credentials"]["usernames"][st.session_state["username"]]["api_key_openai"]
        except KeyError:
            key = ""
        st.text_input("OpenAI", key="api_key_openai", value=key)

        try:
            key = config["credentials"]["usernames"][st.session_state["username"]]["api_key_assemblyai"]
        except KeyError:
            key = ""
        st.text_input( "Assembly AI", key="api_key_assemblyai", value=key)

        try:
            key = config["credentials"]["usernames"][st.session_state["username"]]["api_key_mistral"]
        except KeyError:
            key = ""
        st.text_input( "Mistral", key="api_key_mistral", value=key)

        st.button("Save API Keys", on_click=save_api_keys)


def save_api_keys():
    with open("./auth.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    log.debug(config["credentials"]["usernames"])

    current_user = st.session_state["username"]
    config["credentials"]["usernames"][current_user]["api_key_openai"] = st.session_state["api_key_openai"]
    config["credentials"]["usernames"][current_user]["api_key_assemblyai"] = st.session_state["api_key_assemblyai"]
    config["credentials"]["usernames"][current_user]["api_key_mistral"] = st.session_state["api_key_mistral"]

    with open("./auth.yaml", "w") as file:
        yaml.dump(config, file)

    st.toast("API keys saved!", icon="🔑")



def settings_page():
    # st.write("## API Keys")
    show_api_keys_entry()

    st.markdown("---")
    st.caption(f"running version {VERSION}")
    # st.info("Work in progress", icon="⚠️")
    if os.getenv("DEBUG", False):
        st.warning("Running in debug mode.")
    else:
        st.caption("Running in production mode.")
