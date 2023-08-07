import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 HugChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [HugChat](https://github.com/Soulter/hugging-chat-api)
    - [OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model
    
    💡 Note: No API key required!
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Jagadeesha](https://www.linkedin.com/in/jagadeesha-gowda-6a30382b)')

# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_text()
# Log in to huggingface and grant authorization to huggingchat
email="manyejordana@gmail.com"
passwd="Analeticia21@"
sign = Login(email, passwd)
cookies = sign.login()

# Save cookies to usercookies/<email>.json
sign.saveCookies()
# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    response = chatbot.chat(prompt)
    return response

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            
            
  #Response--------
import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time

# Load the pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Function to generate a response using the model
def generate_response(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Streamlit App
st.title("Chatbot")

# User input
user_input = st.text_input("User Input")

# Check if user input is provided
if user_input:
    # Generate response using the model
    response_placeholder = st.empty()
    response_placeholder.text("Generated Result: ")

    response = generate_response(user_input)

    # Typewriter effect for the generated response
    words = response.split()
    for word in words:
        response_placeholder.text("Generated Result: " + " ".join(words[:words.index(word) + 1]))
        time.sleep(0.1)  # Adjust the sleep time for the desired typing speed

# Display the user input prompt
st.text_area("User Prompt", value=user_input, height=100)

https://chat.openai.com/share/94495184-6ce3-443d-b397-d94e74fabeb3
    
import streamlit as st
import hug

# Create a Hug chat instance
chat = hug.Chat()

# Define a function to generate the result
def generate_result(text):
  # Get the response from the chatbot
  response = chat._get_response(text)

  # Return the response
  return response

# Set the layout of the app
st.layout = st.container()

# Add a text input field
text_input = st.text_input("Enter your message")

# If the user enters a message, generate the result and display it
if text_input:
  # Get the user's query
  query = text_input

  # Generate the result
  result = generate_result(query)

  # Display the user's query, the result, and the conversation history
  st.write("User query:", query)
  st.write("Result:", result)
  st.write("Conversation history:")
  for message in chat._conversation_history:
    st.write(message)

  # Once the user clicks on enter, remove the query from the prompt box
  st.text_input("Enter your message", key=None)

  # Display the generated response in typewriter effect
  st.write(result, unsafe_allow_html=True, key="generated_response")
  st.markdown("""
  <style>
  #generated_response {
  animation: typewriting 2s infinite;
  }

  @keyframes typewriting {
    0% {
      opacity: 0;
    }
    25% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }
  </style>
  """, unsafe_allow_html=True)