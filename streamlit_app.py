import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from py2neo import Graph
import openai

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Set your OpenAI API key
openai.api_key = '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'

# Create a Streamlit interface to input a natural language query
natural_language_query = st.text_input('Enter your natural language query here')

if natural_language_query:
    # Use OpenAI's API to generate a Cypher query from the natural language query
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": natural_language_query}
        ]
    )
    cypher_query = response['choices'][0]['message']['content']

    st.write(cyper_query)

    # Execute the Cypher query against the Neo4j database
    #results = graph.run(cypher_query).data()

    # Display the results in the Streamlit app
    #st.write(results)