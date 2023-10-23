import streamlit as st
import pandas as pd
import seaborn as sns
from collections import Counter
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os
from intro import intro, conclusion, perspective, donnees
from explore_data import affiche_head, affiche_head2, var_expli, distrib_produit, affich_im, affiche_word, word_split



###################################################
df = pd.read_csv('../data/X_train_update.csv')
df = df.rename(columns={ df.columns[0]: "ID" })

image_path = r'../data/images/image_train/'
images_list = os.listdir(image_path)


target = pd.read_csv('../data/Y_train_CVw08PX.csv')
target = target.rename(columns={ target.columns[0]: "ID" })

st_size_list = []
image_name_list = []
info_list = []

with os.scandir(image_path) as directory:
    for element in directory:
        info = element.stat()
        info_list.append(info)
        st_size_list.append(info.st_size)
        image_name_list.append(element.name)

st_size_df = pd.DataFrame(st_size_list,columns=['image_size'])
image_name_df = pd.DataFrame(image_name_list,columns=['image'])

image_df = pd.concat([st_size_df,image_name_df],axis=1)
df1 = df.copy()
df1['image'] = 'image'+'_'+df1['imageid'].astype(str)+'_'+'product'+'_'+df1['productid'].astype(str)+'.jpg'
df1 = df1.merge(image_df, how='left', on='image')
df1 = df1.merge(target, how='left', on='ID')
df1 = df1.set_index('ID')
df1['designation_description'] = df1['designation'] +" "+ df1['description']
df1['designation_description'].loc[df1['description'].isna()] = df1['designation']
df1['designation_description'] = df1['designation_description'].apply(word_split)


######################################################
with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)



st.sidebar.image("logo1.png", width=256)
#st.sidebar.image("logo2.png", width=256)
st.sidebar.header("Table des matières")


with st.sidebar:
    add_radio = st.radio(
        "menu",
        ("Le projet Rakuten", 
        "Analyse exploratoire", 
        "Méthodologie", 
        "Modélisation",
        "Prédiction (démo)",
        "Conclusion & Perspectives")
    )



with st.sidebar:    
    st.success("""
    Projet DS - Promotion Bootcamp Octobre 2022.\n
    Participants : \n
    Ben Adel\n 
    Romain Krawcryk\n 
    Xiao WEI\n 
    Guy Nyamsi
    """)
 

st.image("logo3.png", width=700)

if add_radio == "Le projet Rakuten":
    intro()

if add_radio == "Analyse exploratoire":
    donnees()
    affiche_head(df)
    affiche_head2(image_df)
    var_expli(df,target)
    distrib_produit(target)
    affich_im(image_path,df1)
    affiche_word(df1)


if add_radio == "Conclusion & Perspectives":
    conclusion()
    perspective()

