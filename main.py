import string
from typing import Union, List, Set
import re
from dotenv import load_dotenv
import requests
import streamlit as st
from streamlit_chat import message
from langchain.agents import tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool
from langchain.tools.render import render_text_description
from backend.core import run_llm

load_dotenv()


@tool
def get_order_details(order_id: str) -> str:
    """Returns the order details by making an API call"""

    order_id = order_id.strip()
    if len(order_id) != 7:
        ids = order_id.split("=")
        if len(ids) == 2:
            order_id = ids[1].strip()
            order_id = remove_special_chars(order_id)
    url = "https://api.a4b.io/gw1/puja/external/v1/bookings/" + order_id

    try:
        # Send a GET request to the constructed URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the response JSON
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"


def remove_special_chars(s: str) -> str:
    """Removes trailing special characters from a string."""
    special_chars = string.punctuation  # This includes all punctuation characters
    return s.lstrip(special_chars).rstrip(special_chars)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


# Set up Streamlit
st.header("Ritwik - Your AI Assistant")
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

tools = [get_order_details]

template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template=template).partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)

llm = ChatOpenAI(
    temperature=0,
    stop=["\nObservation", "Observation"],
    callbacks=[],
)
intermediate_steps = []
agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
)


def is_booking_related(query: str) -> bool:
    # Define logic to determine if the query is related to booking
    keywords = ["booking", "order", "prasad"]
    return any(keyword in query.lower() for keyword in keywords)


def submit_message():
    with st.spinner("Generating response..."):
        input_text = st.session_state.input_text

        if is_booking_related(input_text):
            agent_step = ""
            while not isinstance(agent_step, AgentFinish):
                agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
                    {
                        "input": input_text,
                        "agent_scratchpad": intermediate_steps,
                    }
                )
                if isinstance(agent_step, AgentAction):
                    tool_name = agent_step.tool
                    tool_to_use = find_tool_by_name(tools, tool_name)
                    tool_input = agent_step.tool_input

                    observation = tool_to_use.func(str(tool_input))
                    intermediate_steps.append((agent_step, str(observation)))

            if isinstance(agent_step, AgentFinish):
                final_answer = agent_step.return_values["output"]
        else:
            generated_response = run_llm(query=input_text, chat_history=st.session_state["chat_history"])
            final_answer = generated_response['answer']

        st.session_state["user_prompt_history"].append(input_text)
        st.session_state["chat_answers_history"].append(final_answer)
        st.session_state["chat_history"].append(("human", input_text))
        st.session_state["chat_history"].append(("ai", final_answer))
        st.session_state.input_text = ""  # Clear the input text


# Callback function to handle Enter key press
def on_enter():
    if st.session_state.input_text.strip():
        submit_message()


# Text input with dynamic key and on_change callback
st.text_input("Question", placeholder="Ask me anything about Sri Mandir and their services ...", key="input_text",
              on_change=on_enter)

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