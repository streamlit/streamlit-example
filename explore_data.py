
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# %matplotlib inline

import os
import string
import re

stop_words = set(stopwords.words('french') + stopwords.words('english'))
mots_vides = ["x", "cm", "mm", "h", "g", "peut", "être", 'e',"l'",'x','p','re', 'li','x','b','d','h', 'pla','br','id','al','ra','pla','sine','r','g','v','u','f']
stop_words.update(mots_vides)


def word_split(text):
    """split text into words, remove non alphabetic tokens and stopwords"""
    
    # suppression de la ponctuation
    table = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    text = text.translate(table)
    
    # séparation des textes en listes de mots
    tokens = word_tokenize(text)
    
    # conversion en minuscule
    tokens = [w.lower() for w in tokens]
    
    # restriction aux charactères alphabétiques
    words = [word for word in tokens if word.isalpha()]

    # filtrage des stopwords
    words = [w for w in words if not w in stop_words]
    
    return words

def affiche_head(df):
    
    st.table(df.head(3))
    st.caption("<FONT color=green size=+4> Tableau 1. Premières lignes du fichier X_train_update.csv</FONT>", unsafe_allow_html=True )


def affiche_head2(image_df):

    st.table(image_df.head())
    st.caption("<FONT color=green size=+4> Tableau 2. Images et tailles</FONT>", unsafe_allow_html=True )


def var_expli(df,target):


    desi = df.designation
    df[desi.isin(desi[desi.duplicated()])].sort_values("designation").head(10)
    descri = df.description
  
    mots_desi = df['designation'].apply(lambda x : str(x))
    mots_desi = mots_desi.apply(lambda x : len(x.split(" ")))

    mots_desc = df['description'].apply(lambda x : str(x))
    mots_desc = mots_desc.apply(lambda x : len(x.split(" ")))

    temp = df.merge(target, how='left', on='ID')


    fig= plt.figure(figsize=(15, 10))

    plt.subplot(221)
    sns.countplot(x='prdtypecode', data=temp[temp['description'].isna()], 
                order=temp[temp['description'].isna()].prdtypecode.value_counts().index) 
    plt.xticks(rotation=60)
    plt.ylabel('count description vide')
    plt.title ("Distribution du nombre de valeurs manquantes dans la variable 'description'")
    plt.grid()
    plt.subplot(222)
    sns.countplot(x='prdtypecode', data=temp[mots_desc>1000],
                order=temp[mots_desc>1000].prdtypecode.value_counts().index)
    plt.xticks(rotation=60)
    plt.ylabel('count description longue (> 1000 mots)')
    plt.title ("Distribution des descriptions longues (> 1000 mots)")
    plt.grid()

    plt.tight_layout(pad=5.0)

    plt.subplot(223)
    mots_desi.hist(bins= 40)
    plt.title ("Distribution du nombre de mot dans la variable 'designation'")
    plt.xlabel('Nombre de mots')
    plt.ylabel('redondances')
    plt.subplot(224)
    mots_desc.hist(bins= 40)
    plt.title ("Distribution du nombre de mot dans la variable 'description'")
    plt.xlabel('Nombre de mots')
    plt.ylabel('redondances')
    st.pyplot(fig)
    st.caption("<FONT color=green size=+4> Figure 1 - Distributions des mots</FONT>", unsafe_allow_html=True )

    
    st.markdown("""

    On peut voir sur les deux graphiques ci-dessus que les designation et description des différents produits varient grandement
    d'un produit à l'autre. Une designation ou une description succincte et claire aidera le modèle à apprendre à classer 
    les différentes catégories de produit. À l'inverse, si cette designation / description est trop longue, cela sera trop 
    spécifique pour en tirer quelque-chose.
    """)

def distrib_produit(target):

    code_bar = pd.DataFrame(target.prdtypecode.value_counts()).reset_index()
    code_bar.columns = ['prdtypecode', 'count']
    fig = plt.figure(figsize = (10,5))
    sns.barplot(data= code_bar, x= 'prdtypecode', y= 'count', order= code_bar.sort_values('count', ascending= False).prdtypecode)
    plt.xticks(rotation=45)
    plt.title("Répartition des produits par modalité");

    st.pyplot(fig)
    st.caption("<FONT color=green size=+4> Figure 2 - Distributions des produits par modalité (voir Annexe 1 rapport)</FONT>", unsafe_allow_html=True )

    st.markdown("""
    On remarque une grande différence dans les ordres de grandeur des proportions de chacune des
    modalités. Cela pourrait poser problème lors de la prédiction des modalités les moins représentées.
    """)


def box_plot(df):

    fig = plt.figure(figsize=(15,5))
    sns.boxplot(x='prdtypecode',y='image_size',data=df)
    plt.title("Distribution des tailles d'image en fonction du code produit")
    st.pyplot(fig)
    st.caption("<FONT color=green size=+4> Figure 3 - Distribution des tailles d'image en fonction du code produit</FONT>", unsafe_allow_html=True )

    st.markdown("""
    On remarque une grande différence dans les ordres de grandeur des proportions de chacune des
    modalités. Cela pourrait poser problème lors de la prédiction des modalités les moins représentées.
    """)


def affich_im(image_path,df):
    code_prd = df.prdtypecode.unique().tolist()
    code_prd = code_prd[:3]
    for code in code_prd:
        #print(category)
        f, axarr = plt.subplots(1,5,figsize=(10,5),subplot_kw = dict(xticks=[], yticks=[])) 

        img_list = df[df['prdtypecode'] == code]['image'].head(5).tolist()
        i=0

        for img in img_list:
            plot = plt.imread(image_path + img);
            #axarr[i].axis('off')
            axarr[i].set_ylabel(code)
            axarr[i].imshow(plot);
            i +=1
    
        st.pyplot(f)
    st.caption("<FONT color=green size=+4> Figure 4 - Exemple d’image produit des catégories 1301 Accessoires gaming</FONT>", unsafe_allow_html=True )

def affiche_word(df):
    
    dict_cat = {'Livres':[10, 2280, 2403, 2522, 2705],
            'Jeux':[40, 50, 60, 2462, 2905],
            'Jouets & figurines':[1140, 1160, 1180, 1280, 1281, 1300, 1302],
            'Meubles':[1560, 2582],
            'Equipements divers':[1320, 2220, 2583, 2585],
            'Deco':[1920, 2060],
            'Autres':[1301, 1940]}

    for key, value in dict_cat.items():
        df.loc[df['prdtypecode'].isin(value), 'prdcat'] = key

   
    for categorie in dict_cat.keys():
        text = " ".join(w for text in df[df.prdcat == categorie]['designation_description'] for w in text)
        print ( ("Il y a {} mots dans la categorie "+categorie).format(len(text)))

        word_count = Counter(text.split(" "))
        mots = [m[0] for m in word_count.most_common(15)]
        freq = [m[1] for m in word_count.most_common(15)]

        wordcloud = WordCloud(max_font_size=50, max_words=100, stopwords=stop_words, background_color="white").generate(text)

        fig = plt.figure(figsize=(15, 3))
        plt.subplot(121)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title('Word Cloud - '+categorie)
        plt.subplot(122)
        sns.barplot(x=mots, y=freq)
        plt.title('15 mots les plus fréquents dans la catégorie '+categorie)
        plt.xticks(rotation=45)
        plt.ylabel('Occurence de mots')
        plt.grid()

        st.pyplot(fig)
    st.caption("<FONT color=green size=+4> Figure 4 - Exemple d’image produit de la catégorie 1301 “Accessoires gaming</FONT>", unsafe_allow_html=True )
