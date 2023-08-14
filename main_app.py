
import pandas as pd
import numpy as np
import streamlit as st

###Chatbot Imports###
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
from hugchat_api import HuggingChat
import os
import streamlit as st
import pandas as pd
from typing import Text
from google_trans_new import google_translator

###Visualizer imports###
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.embeddings.openai import OpenAIEmbeddings

###Summarizer imports###
import tempfile
import time
import openai
import torch
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from transformers import pipeline

 

with st.sidebar:
    st.set_page_config(page_title="AllTalK")
    ti=st.title("Welcome to 😃AllTalK💬!")
    st.write('Developed By [Jordana](https://www.linkedin.com/in/manye-jordana-0315731b1)')
    st.markdown('For any enquiries contact me [here](https://myportfolio.com)!')
    
    def load_lottier(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_url_hello = "https://lottie.host/056f7af6-f742-4fd8-84ab-1f77690fe0eb/7HXVl4uGgU.json"
    lottie_url_download = "https://lottie.host/eac077c4-86e8-43b1-b41f-142af05db24d/SrwORZwZZV.json"
    lottie_hello = load_lottier(lottie_url_hello)
    lottie_download = load_lottier(lottie_url_download)

    st_lottie(lottie_hello, key="hello")
page=st.selectbox("WHAT I OFFER !",("Select","AI ChatBot","AI Summarizer","AI Analyst"))


#Hide main menu and footer
hide_default_format = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_default_format, unsafe_allow_html=True)


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


        # Store LLM Generated responses
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]


        # Display  chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown("Hello !")


        # Funtion genrating LLM response
        def generate_response(dialogue_history):
            #Hugging face login
            sign = Login(EMAIL, PASSWD)
            cookies = sign.login()
            # Create ChatBot
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            return chatbot.chat(dialogue_history)
        
        # User-provided prompt
        if prompt := st.chat_input("How can i help ?"):
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
                        #st.chat_input("Follow up question"value=full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})

    def visualizer():
        st.title("😊 AllAnalysis 📈")
        st.markdown('''
        - Hey there i'm AllVisuals 📈, your new AI Exploratory data analyst 😊.
        - I produce answers and stunning visuals from the data you give me.
        - Just Upload your dataset and ask your questions 💡 !
        ''')
        
        #st_lottie(lottie_download, key="chart")

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
        #@st.cache_data()
        def load_summarizer():
            summary = pipeline(task="summarization", model="t5-small", device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
            return summary


        def generate_chunks(inp_str):
            max_chunk = 500
            inp_str = inp_str.replace('.', '.<eos>')
            inp_str = inp_str.replace('?', '?<eos>')
            inp_str = inp_str.replace('!', '!<eos>')
            
            sentences = inp_str.split('<eos>')
            current_chunk = 0 
            chunks = []
            for sentence in sentences:
                if len(chunks) == current_chunk + 1: 
                    if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                        chunks[current_chunk].extend(sentence.split(' '))
                    else:
                        current_chunk += 1
                        chunks.append(sentence.split(' '))
                else:
                    chunks.append(sentence.split(' '))

            for chunk_id in range(len(chunks)):
                chunks[chunk_id] = ' '.join(chunks[chunk_id])
            return chunks


        summarizer = load_summarizer()
        #st.title("Summarize Text")
        sentence = st.text_area('Input your text here:', height=200)
        button = st.button("Summarize")

        max = st.sidebar.slider('Select max', 50, 500, step=10, value=150)
        min = st.sidebar.slider('Select min', 10, 450, step=10, value=50)
        do_sample = st.sidebar.checkbox("Do sample", value=False)
        with st.spinner("Generating Summary.."):
            if button and sentence:
                chunks = generate_chunks(sentence)
                res = summarizer(chunks,
                                max_length=max, 
                                min_length=min, 
                                do_sample=do_sample)
                text = ' '.join([summ['summary_text'] for summ in res])
                # st.write(result[0]['summary_text'])
                st.write(text)

    #PDF Uploader function    
        # Split text using character text split so it should increase token size
        text_splitter = CharacterTextSplitter(
            separator= "\n",
            chunk_size = 800,
            chunk_overlap = 200,
            length_function = len,
        )

        #Creating user interface
        pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

        #Initializing OpenAI and text spliter        
        openai_api_key = st.text_input('OpenAI API Key', type='password')

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')

        #User input for page selection
        page_selection = st.radio("Page selection", ["Single page", "Page range", "Overall Summary", "Question"], disabled=not pdf_file)

        #Single page summarization
        if page_selection == "Single page":
            if pdf_file is not None:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(pdf_file.read())
                    pdf_path = tmp_file.name
                    loader = PyPDFLoader(pdf_path)
                    pages = loader.load_and_split()
                    llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.2, openai_api_key=openai_api_key)
                    page_number = st.number_input("Enter page number", min_value=1, max_value=len(pages), value=1, step=1)
                    view = pages[page_number - 1]
                    texts = text_splitter.split_text(view.page_content)
                    docs = [Document(page_content=t) for t in texts]
                    chain = load_summarize_chain(llm, chain_type="map_reduce")
                    summaries = chain.run(docs)

                    st.subheader("Summary")
                    st.write(summaries)

        elif page_selection == "Page range":
            start_page = st.number_input("Enter start page", min_value=1, max_value=len(pages), value=1, step=1)
            end_page = st.number_input("Enter end page", min_value=start_page, max_value=len(pages), value=start_page, step=1)

            texts = []
            for page_number in range(start_page, end_page+1):
                view = pages[page_number-1]
                page_texts =text_splitter.split_text(view.page_content)
                texts.extend(page_texts)
            docs = [Document(page_content=t)for t in texts]
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            summaries = chain.run(docs)
            st.subheader("Summary")
            st.write(summaries)
        
        elif page_selection == "Overall Summary":
            combined_content = ''.join([p.page_content for p in pages]) #Get entire page data
            texts = text_splitter.split_text(combined_content)
            docs = [Document(page_content=t) for t in texts]
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            summaries = chain.run(docs)
            st.subheader("Summary")
            st.write(summaries)

        #Question andd answering criterion
        elif page_selection =="Question":
            question = st.text_input("Enter your question")
            combined_content = ''.join([p.page_content for p in pages])
            texts = text_splitter.split_text(combined_content)
            embedding = OpenAIEmbeddings(llm)
            document_search = FAISS.from_texts(texts, embedding) #FAISS for efficient search of simlarity and clustering
            chain = load_qa_chain(llm, chain_type="stuff")
            docs = document_search.similarity_search(question)
            summaries = chain.run(input_documents=docs, question=question)
            st.write(summaries)

        else:
            time.sleep(30)
            st.warning("No PDF file uploaded!")




    if page == "Select":
        st.write("Please select the services")
    elif page == "AI ChatBot":
        chatbot()
    elif page == "AI Analyst":
        visualizer()  
    else:
        summarizer()
  
if __name__=='__main__':
    main()
