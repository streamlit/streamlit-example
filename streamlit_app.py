import streamlit as st
import pickle
import os


def main():
    file_list = os.listdir('test_files')
    file_name = st.selectbox('Select File', file_list)

    with open('test_files/' + file_name, 'rb') as file:
        data = pickle.load(file)
    text = data['text']
    html = f'<div style="direction: rtl; text-align: right;">{text}</div>'
    st.markdown(f"<div style='direction: rtl; text-align: right;'>{html}</div></br>", unsafe_allow_html=True)
    

if __name__ == '__main__':
    main()
