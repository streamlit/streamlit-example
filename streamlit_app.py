from difflib import SequenceMatcher
import streamlit as st

def calcular_similaridade(texto1, texto2):
    # Criar um objeto SequenceMatcher com os textos dos arquivos
    seq_matcher = SequenceMatcher(False, texto1, texto2)

    # Obter a similaridade normalizada entre 0 e 1
    similaridade_ponderada = seq_matcher.ratio()

    return similaridade_ponderada

# Exemplo de uso
st.title('Comparação de textos!')
st.title(':blue[Isis] :sunglasses:')
texto1 =  st.text_input(
    "Entre com o primeiro texto 👇",
)
texto2 =  st.text_input(
    "Entre com o segundo texto 👇",
)

similaridade = calcular_similaridade(texto1, texto2)
st.text('Indice de similaridade entre os textos.')
st.text(similaridade)

