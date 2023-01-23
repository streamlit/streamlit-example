import streamlit as st
import openai

st.title('STORY GENERATOR')
st.markdown('I will create short story for you')

title = st.text_input('Tell me story about...', key="text")
prompt = (f"Tell me a fairy tale about {title}")

openai.api_key = AI_TOKEN
if title:
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=0.4,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    st.markdown(body=response.choices[0].text)
