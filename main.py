from dotenv import load_dotenv

load_dotenv()
from typing import Set

import streamlit as st
from streamlit_chat import message

from backend.core import run_llm


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


st.header("Ritwik - Your AI Assistant")
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""


def submit_message():
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=st.session_state.input_text, chat_history=st.session_state["chat_history"]
        )

        formatted_response = generated_response['answer']

        st.session_state["user_prompt_history"].append(st.session_state.input_text)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", st.session_state.input_text))
        st.session_state["chat_history"].append(("ai", generated_response["answer"]))
        st.session_state.input_text = ""  # Clear the input text


# Callback function to handle Enter key press
def on_enter():
    if st.session_state.input_text.strip():
        submit_message()


# Text input with dynamic key and on_change callback
st.text_input("", placeholder="Ask me anything about Sri Mandir and their services...", key="input_text", on_change=on_enter)

# Submit button
if st.button("Submit"):
    if st.session_state.input_text.strip():
        submit_message()

# Display the chat history and responses
if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
            reversed(st.session_state["chat_answers_history"]),
            reversed(st.session_state["user_prompt_history"]),
    ):
        message(generated_response)
        message(user_query, is_user=True)
