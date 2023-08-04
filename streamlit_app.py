import streamlit as st
import pickle
import os


def main():
    st.write("Prediction Examples:")
    st.markdown("<span style='color:green'>Green:</span> correct prediction – TP", unsafe_allow_html=True)
    st.markdown("<span style='color:red'>Red:</span> Wrong prediction. Wherever there are square brackets (e.g. [.]), these square brackets represent the punctuation in the text, and the punctuation without brackets represents the prediction. If there is only punctuation within brackets and no punctuation without the brackets, then the prediction was BLANK (no punctuation), or, alternately, if there is no punctuation with brackets, and only punctuation without brackets, then there was no punctuation in the original text (only in the prediction). For example:", unsafe_allow_html=True)
    st.markdown("[.] - original text punctuation", unsafe_allow_html=True)
    st.markdown(". [,] - the original is ‘,’ and the prediction is ‘.’", unsafe_allow_html=True)
    st.markdown(". - the prediction is ‘.’ and there was no punctuation in the original text", unsafe_allow_html=True)
    
    file_list = os.listdir('test_files')
    file_name = st.selectbox('Select File', file_list)

    with open('test_files/' + file_name, 'rb') as file:
        data = pickle.load(file)
    text = data['text']
    html = f'<div style="direction: rtl; text-align: right;">{text}</div>'
    st.markdown(f"<div style='direction: rtl; text-align: right;'>{html}</div></br>", unsafe_allow_html=True)
    

if __name__ == '__main__':
    main()
