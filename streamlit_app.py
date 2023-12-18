import streamlit as st
import pandas as pd
import random

# Laad je Excel-bestand met de vragen en antwoorden
excel_file_path = 'champion-title.xlsx'  # Vervang dit met het pad naar jouw bestand
df = pd.read_excel(excel_file_path)

# Functie om een willekeurige vraag op te halen
def get_random_question():
    random_row = df.sample(1)
    question = random_row['champ-list__item__title'].values[0]
    answer = random_row['champ-list__item__name'].values[0]
    return question, answer

# Streamlit-applicatie
def main():
    st.title('Vragen en Antwoorden App')

    # Overzichtspagina met knoppen
    page = st.sidebar.selectbox('Selecteer een pagina:', ['Home', 'Vraag 1', 'Vraag 2', 'Vraag 3', 'Vraag 4', 'Vraag 5', 'Vraag 6'])

    if page == 'Home':
        st.header('Welkom op de overzichtspagina!')
        st.write('Kies een vraagcategorie uit de zijbalk.')

        # Knoppen voor verschillende vraagcategorieën
        if st.sidebar.button('Vraag 1', key='1'):
            st.session_state.question, st.session_state.answer = get_random_question()
            st.session_state.show_answer = False
        elif st.sidebar.button('Vraag 2', key='2'):
            st.session_state.question, st.session_state.answer = get_random_question()
            st.session_state.show_answer = False
        # Voeg hier de knoppen voor Vraag 3 tot Vraag 6 toe op dezelfde manier

    elif page.startswith('Vraag'):
        st.header(page)
        st.write('Vraag: ' + st.session_state.question)

        # Knop om antwoord te tonen
        if st.button('Toon antwoord'):
            st.write('Antwoord: ' + st.session_state.answer)
            st.session_state.show_answer = True

        # Knop om terug te gaan naar overzichtspagina
        if st.button('Terug'):
            st.session_state.sync()
            st.experimental_rerun()

    st.session_state.sync()

if __name__ == '__main__':
    main()
