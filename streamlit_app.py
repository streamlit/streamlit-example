import streamlit as st
from langchain.llms import OpenAI
import os
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate

from langchain import OpenAI, LLMChain
from langchain.tools import DuckDuckGoSearchRun 

from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re
import langchain
import random
import time

# .streamlit/secrets.toml
OPENAI_API_KEY = "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"

import openai
import streamlit as st

st.title("ChatGPT-like clone")

openai.api_key = "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"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
