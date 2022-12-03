import openai
import os


class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns


# Method to get answer from OpenAI API and return the answer as a string
def get_answer_from_openai(query, tables):
    # Generate a prompt for OpenAI to translate the query to SQL in the following format:
    # "### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# "
    # "Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query "
    # "to list the names of the departments which employed more than 10 employees in the last 3 "
    # "months\nSELECT"

    query_prompt = '### Postgres SQL tables, with their properties:\n#\n'

    # Concatenate the tables and columns
    for table in tables:
        columns = ', '.join(table.columns)
        query_prompt += '# Table: ' + table.name + '(' + columns + ')\n'

    # Add the query
    query_prompt += '#\n###  ' + query + '\n#\nSELECT'

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=query_prompt,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )
    return 'SELECT ' + response.choices[0].text
