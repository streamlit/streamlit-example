#pip install hugchat

import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
from hugchat_api import HuggingChat

# App title
st.set_page_config(page_title="😊 UsCHAT 💬")

EMAIL = st.secrets["DB_EMAIL"]
PASSWD = st.secrets["DB_PASS"]
COOKIE_STORE_PATH = "./usercookies"

#HUG= HuggingChat(max_thread=1)

# Hugging Face Credentials
with st.sidebar:
    st.title('😊 UsCHAT 💬')
    #st.header('UsCHAT Login')
    #sign = Login(EMAIL, PASSWD)
    #cookies = sign.login()
    #cookies = sign.loadCookiesFromDir(cookie_dir_path=COOKIE_STORE_PATH)
    
    #if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
    #    st.success('HuggingFace Login credentials already provided !', icon='✅')
    #    hf_email = st.secrets['EMAIL']
    #    hf_pass = st.secrets['PASS']
    #else:
    #    hf_email = st.text_input('Enter E-mail:', type='default')
    #    hf_pass = st.text_input('Enter password:', type='password')
    #    if not (hf_email and hf_pass):
    #        st.warning('Please enter your credentials!', icon='⚠')
    #    else:
    #        st.success('Proceed to your chat!', icon='👉')
    st.markdown('Contact me for enquiries [here](https://myportfolio.com)!')


# Store LLM Generated responses
if "messages" not in st.session_state:
    st.session_state.messages = []
    #st.session_state.messages = [{"role": "assistant", "content": "Hey there, how can I help you?"}]


# Display  chat messages
for message in st.session_state.messages():
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Funtion genrating LLM response
def generate_response(dialogue_history):
    #Hugging face login
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login()
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    response = chatbot.chat(dialogue_history, stream=True)
    return response
    #if isinstance(response, str):
        #return response
    #else:
        #return response.delta.get("content", "")
    #return chatbot.chat(prompt_input)


# User-provided prompt
if prompt := st.chat_input("How may I help you ?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Append the dialogue history to the user's prompt
    dialogue_history = "\n".join([message["content"] for message in st.session_state.messages])
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


# Genrate a new response if last message not from the assistant(chatbot)
#if st.session_state.messages[-1]["role"] != "assistant":
with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
        message_placeholder = st.empty()
        full_response = ""

        try:
            for response in generate_response(dialogue_history):
                full_response += response
                message_placeholder.markdown(full_response + " ")
                sleep(0.01)
            message_placeholder.markdown(full_response)

            #checking if there are follow-up questions
            if "?" in prompt:
                #Update the chat history with the bot's response
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                #Clear the chat input box
                st.session_state.prompt = ""
                #set the chat input box value to the assistant's response
                st.chat_input("Follow-up question", value=full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})
            
        #response = generate_response(prompt, hf_email, hf_pass)
        #st.write(response)
    #message = {"role": "assistant", "content": response}
    #st.session_state.messages.append(message)