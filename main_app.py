import pandas as pd
import numpy as np
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
from hugchat_api import HuggingChat
import os
import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import requests
import tabulate
import openai
import classes
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

 

with st.sidebar:
    ti=st.title("Welcome to 😃AllTalK💬!")
    st.write('Developed By [Jordana](https://www.linkedin.com/in/manye-jordana-0315731b1)')
    st.markdown('For any enquiries contact me [here](https://myportfolio.com)!')
page=st.selectbox("WHAT I OFFER !",("Select","AI ChatBot","AI Summarizer","AI Visualizer"))


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

    def visualizer():
        st.title("😊 AllVisuals 📈")
        st.markdown('''
        - Hey there i'm AllVisuals 📈, your new AI Exploratory data analyst 😊.
        - I produce answers and stunning visuals from the data you give me.
        - Just Upload your dataset and ask your questions 💡 !
        ''')
        
        def load_csv(input_csv):
            df = pd.read_csv(input_csv)
            with st.expander('See DataFrame'):
                st.write(df)
            return df

        # Generate LLM response
        def generate_response(csv_file, input_query):
            llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.2, openai_api_key=openai_api_key)
            df = load_csv(csv_file)
            # Create Pandas DataFrame Agent
            agent = create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS)
            # Perform Query using the Agent
            response = agent.run(input_query)
            return st.success(response)

        # Input widgets
        uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])
        question_list = [
            'How many rows are there ?',
            'What is the datatype of each column ?',
            'Are they missing values ?',
            'Other']
        query_text = st.selectbox('Select an example query:', question_list, disabled=not uploaded_file)
        openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_file and query_text))

        # App logic
        if query_text == 'Other':
            query_text = st.text_input('Enter your query:', placeholder = 'Enter query here ...', disabled=not uploaded_file)
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        if openai_api_key.startswith('sk-') and (uploaded_file is not None):
            st.header('Output')
            generate_response(uploaded_file, query_text)


    def summarizer():
        st.title("😊 AllSummary 💬")
        st.markdown('''
        - Hey there i'm AllSummary 🧾, my name says it all, I summarize everything 😊.
        - text, pdf's, just write or upload your document and let me do the rest !
        - I'm trained to help you the best i can and soon with more training i'll be a knowItAll !
        - Stick with me until then to have everything before everyone 💡 ! 
         ''')

        def generate_response(txt):
            # Instantiate the LLM model
            llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
            # Split text
            text_splitter = CharacterTextSplitter()
            texts = text_splitter.split_text(txt)
            # Create multiple documents
            docs = [Document(page_content=t) for t in texts]
            # Text summarization
            chain = load_summarize_chain(llm, chain_type='map_reduce')
            return chain.run(docs)

        # Text input
        txt_input = st.text_area('Enter your text', '', height=200)

        # Form to accept user's text input for summarization
        result = []
        with st.form('summarize_form', clear_on_submit=True):
            openai_api_key = st.text_input('OpenAI API Key', type = 'password', disabled=not txt_input)
            submitted = st.form_submit_button('Submit')
            if submitted and openai_api_key.startswith('sk-'):
                with st.spinner('Calculating...'):
                    response = generate_response(txt_input)
                    result.append(response)
                    del openai_api_key

        if len(result):
            st.info(response)

        def setup_documents(pdf_file_path,chunk_size,chunk_overlap):
            loader = PyPDFLoader(pdf_file_path)
            docs_raw = loader.load()
            docs_raw_text = [doc.page_content for doc in docs_raw]
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                        chunk_overlap=chunk_overlap)
            docs = text_splitter.create_documents(docs_raw_text)
            
            return docs
            


        def custom_summary(docs, llm, custom_prompt, chain_type, num_summaries):
            custom_prompt = custom_prompt + """:\n {text}"""
            COMBINE_PROMPT = PromptTemplate(template=custom_prompt, input_variables = ["text"])
            MAP_PROMPT = PromptTemplate(template="Summarize:\n{text}", input_variables=["text"])
            if chain_type == "map_reduce":
                chain = load_summarize_chain(llm,chain_type=chain_type,
                                            map_prompt=MAP_PROMPT,
                                            combine_prompt=COMBINE_PROMPT)
            else:
                chain = load_summarize_chain(llm,chain_type=chain_type)
            
            summaries = []
            for i in range(num_summaries):
                summary_output = chain({"input_documents": docs}, return_only_outputs=True)["output_text"]
                summaries.append(summary_output)
            
            return summaries

        @st.cache_data
        def color_chunks(text: str, chunk_size: int, overlap_size: int) -> str:
            overlap_color = "#808080"
            chunk_colors = ["#a8d08d", "#c6dbef", "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2"] # Different shades of green for chunks
            
            colored_text = ""
            overlap = ""
            color_index = 0
            for i in range(0, len(text), chunk_size-overlap_size):
                chunk = text[i:i+chunk_size]
                if overlap:
                    colored_text += f'<mark style="background-color: {overlap_color};">{overlap}</mark>'
                chunk = chunk[len(overlap):]
                colored_text += f'<mark style="background-color: {chunk_colors[color_index]};">{chunk}</mark>'
                color_index = (color_index + 1) % len(chunk_colors)
                overlap = text[i+chunk_size-overlap_size:i+chunk_size]

            return colored_text

        def main():
            st.set_page_config(layout="wide")
            st.title("Custom Summarization App")
            llm = st.sidebar.selectbox("LLM",["ChatGPT", "GPT4", "Other (open source in the future)"])
            chain_type = st.sidebar.selectbox("Chain Type", ["map_reduce", "stuff", "refine"])
            chunk_size = st.sidebar.slider("Chunk Size", min_value=20, max_value = 10000,
                                        step=10, value=2000)
            chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=5, max_value = 5000,
                                        step=10, value=200)
            
            if st.sidebar.checkbox("Debug chunk size"):
                st.header("Interactive Text Chunk Visualization")

                text_input = st.text_area("Input Text", "This is a test text to showcase the functionality of the interactive text chunk visualizer.")

                # Set the minimum to 1, the maximum to 5000 and default to 100
                html_code = color_chunks(text_input, chunk_size, chunk_overlap)
                st.markdown(html_code, unsafe_allow_html=True)

                
            else:
                user_prompt = st.text_input("Enter the custom summary prompt")
                pdf_file_path = st.text_input("Enther the pdf file path")
                
                temperature = st.sidebar.number_input("Set the ChatGPT Temperature",
                                                    min_value = 0.0,
                                                    max_value=1.0,
                                                    step=0.1,
                                                    value=0.5)
                num_summaries = st.sidebar.number_input("Number of summaries",
                                                        min_value = 1, 
                                                        max_value = 10,
                                                        step = 1,
                                                        value=1)
            if pdf_file_path != "":
                docs = setup_documents(pdf_file_path, chunk_size, chunk_overlap)
                st.write("PDF loaded successfully")
            
                if llm=="ChatGPT":
                    llm = ChatOpenAI(temperature=temperature)
                elif llm=="GPT4":
                    llm = ChatOpenAI(model_name="gpt-4",temperature=temperature)
                else:
                    st.write("Using ChatGPT while open source models are not implemented!")
                    llm = ChatOpenAI(temperature=temperature)

            if st.button("Summarize"):
                    result = custom_summary(docs, llm, user_prompt, chain_type, num_summaries)
                    st.write("Summary:")
                    for summary in result:
                        st.write(summary)






    if page == "Select":
        st.write("Please select the services")
    elif page == "AI ChatBot":
        chatbot()
    elif page == "AI Visualizer":
        visualizer()  
    else:
        summarizer()
  
if __name__=='__main__':
    main()
