import pandas as pd
import numpy as np
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
from hugchat_api import HuggingChat
import os

with st.sidebar:
    ti=st.title("Welcome to 😃AllTalK💬!")
    st.write('Developed By [Jordana](https://www.linkedin.com/in/manye-jordana-0315731b1)')
    st.markdown('For any enquiries contact me [here](https://myportfolio.com)!')
page=st.selectbox("WHAT I OFFER !",("Select","AI ChatBot","AI Summarizer","AI Visualsuer"))


def main():
    def chatbot():
        st.title("😊 AllTalK 💬")
        st.markdown('''
        - Hey there i'm AllTalk 💬, your new AI friend 😊.
        - I may produce inacurate information about people, places, or facts
        - I have limited knowledge of the world and events after 2021 but i'm trained to help you the best i can and soon with more training i'll be a knowItAll !
        - Stick with me until then to be aware of everything before everyone 💡 ! 
         ''')
            
        EMAIL = st.secrets["DB_EMAIL"]
        PASSWD = st.secrets["DB_PASS"]
        COOKIE_STORE_PATH = "./usercookies"

        #HUG= HuggingChat(max_thread=1)

        #sign=HUG.getSign(EMAIL,PASSWD)
        #try:
        #    cookies=sign.login(save=True,cookie_dir_path=COOKIE_STORE_PATH)
        #except Exception as e:
        #    st.error(f"An error occurred during login: {str(e)}")
        #    st.stop()
        #cookies=sign.loadCookiesFromDir(cookie_dir_path=COOKIE_STORE_PATH)

        # Store LLM Generated responses
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]


        # Display  chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        # Funtion genrating LLM response
        def generate_response(dialogue_history):
            #Hugging face login
            sign = Login(EMAIL, PASSWD)
            cookies = sign.login()
            # Create ChatBot
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            return chatbot.chat(dialogue_history)
        
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
        if st.session_state.messages[-1]["role"] != "assistant":
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
                
    if page == "Select":
        st.write("Please select the services")
    elif page == "AI ChatBot":
        chatbot()
    else:
        summarizer()
    #else:
    #    chatbot()  
  
if __name__=='__main__':
    main()
