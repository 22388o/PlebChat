import os
import time
import json
import yaml

import streamlit as st

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


# OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
OPENAI_TTS_MODELS = ["echo", "nova", "onyx"]
TTS_VOICE_CHOICES = ["Male", "Female", "Male (deep)"]



class ChatThread:
    def __init__(self):
        # self.session_start_time = None
        self.session_start_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.description = None
        self.messages: list[ChatMessage] = []
        self.incomplete_stream = None



class ChatAppVars:
    def __init__(self):
        self.username = st.session_state.username

        self.api_key_mistral = None
        self.api_key_openai = None
        self.api_key_assemblyai = None
        self.get_api_keys()

        self.client = MistralClient(self.api_key_mistral)

        # make sure the runlog directory exists
        self.runlog_dir = os.path.join(os.getcwd(), "runlog", self.username)
        os.makedirs(self.runlog_dir, exist_ok=True)

        # self.session_start_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())

        self.chat = ChatThread()

        # SETTINGS
        self.debug = os.getenv("DEBUG", False)
        self.mistral_models = ['mistral-medium', 'mistral-small', 'mistral-tiny']
    

    
    def get_api_keys(self):
        with open("./auth.yaml") as file:
            config = yaml.load(file, Loader=yaml.loader.SafeLoader)

        # TODO find a better way?
        try:
            self.api_key_openai = config["credentials"]["usernames"][self.username]["api_key_openai"]
        except KeyError:
            self.api_key_openai = None

        try:
            self.api_key_mistral = config["credentials"]["usernames"][self.username]["api_key_mistral"]
        except KeyError:
            # This can't be none
            # self.api_key_mistral = None
            raise Exception("Mistral API key not found")

        try:
            self.api_key_assemblyai = config["credentials"]["usernames"][self.username]["api_key_assemblyai"]
        except KeyError:
            self.api_key_assemblyai = None
        
        print(f"api_key_openai: {self.api_key_openai}")
        print(f"api_key_mistral: {self.api_key_mistral}")
        print(f"api_key_assemblyai: {self.api_key_assemblyai}")


    def get_client(self):
        if self.debug:
            output = [
                DeltaContentChunk("hello "),
                DeltaContentChunk("world! "),
                DeltaContentChunk("I am"),
                DeltaContentChunk(" a chatbot.")
            ]
            for o in output:
                time.sleep(0.5)
                yield o
        else:
            yield self.client.chat_stream(
                model=self.mistrel_model, #TODO NOPE THIS WON'T WORK
                messages=self.messages,
                safe_mode=self.mistrel_safemode
            )
    
    def new_thread(self):
        self.chat = ChatThread()













def load_convo(runlog):
    """ Load a previous conversation from a runlog file"""

    st.toast(f"Loading {runlog}...")

    # load the runlog file
    with open(os.path.join(st.session_state.runlog_dir, runlog), "r") as f:
        file_contents = json.load(f)

        messages = file_contents["messages"]
        st.session_state.messages = [deserialize_messages(m) for m in messages]

        st.session_state["session_start_time"] = file_contents["session_start_time"]
        st.session_state["description"] = file_contents["description"]



def delete_this_chat():
    """ Delete the current chat history """

    runlog_file = os.path.join(st.session_state.runlog_dir, f'{st.session_state["session_start_time"]}.txt')
    os.remove(runlog_file)

    # setup()
    st.session_state.appstate.new_thread()



def get_description():
    # call the API to get the description

    client = MistralClient(api_key=st.session_state.api_key_mistral)

    messages = [
        ChatMessage(
            role="user",
            content=f"List at most 5 key words from the following: `{st.session_state.messages[0].content}`\nReply should be no more than 5 words."
        )
    ]

    chat_response = client.chat(
        model="mistral-small",
        messages=messages,
    )
    print(chat_response)
    # st.stop()
    return chat_response.choices[0].message.content


def save_chat_history():
    """ Save the chat history to a file """

    if st.session_state['description'] == None:
        desc = get_description()


    # serialize the messages
    messages = [serialize_messages(m) for m in st.session_state.messages]

    # save the chat history to a file
    runlog_file = os.path.join(st.session_state.runlog_dir, f'{st.session_state["session_start_time"]}.txt')
    with open(runlog_file, "w") as f:
        json.dump(
            {
                "description": desc,
                "session_start_time": st.session_state["session_start_time"],
                "messages": messages
            },
            f,
            indent=4
        )







# def get_api_key(key: API_KEY):
#     with open("./auth.yaml") as file:
#         config = yaml.load(file, Loader=SafeLoader)
    
#     try:
#         ret = config["credentials"]["usernames"][st.session_state["username"]][key]
#         if ret == "":
#             return None
#         else:
#             return ret
#     except KeyError:
#         return None





class Content:
    def __init__(self, word_chunk):
        self.content = word_chunk

class Delta:
    def __init__(self, word_chunk):
        self.delta = Content(word_chunk)

class DeltaContentChunk:
    def __init__(self, word_chunk):
        self.choices = [
                Delta(word_chunk),
            ]



def serialize_messages(msg: ChatMessage):
    s = {
            "role": msg.role,
            "content": msg.content
        }
    return s


def deserialize_messages(msg):
    d = ChatMessage(role=msg["role"], content=msg["content"])
    return d
