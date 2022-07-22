
# ______________________________________________________________________________________________________
# Import des bibliothèques
# ______________________________________________________________________________________________________

import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# ______________________________________________________________________________________________________
# Configuration du site
# ______________________________________________________________________________________________________

st.set_page_config(page_title="JAD'Up",  layout='wide', page_icon='https://raw.githubusercontent.com/amelievert/streamlit-example/master/Agence%20de%20Marketing.ico')

st.sidebar.title("Sommaire")
st.sidebar.image('https://raw.githubusercontent.com/amelievert/streamlit-example/master/Agence%20de%20Marketing.ico')

pages = ["Introduction au jeu de données",
         "Analyse",
         "Preprocessing",
         "Challenge de modèles",
         "Pour aller plus loin"]

page = st.sidebar.radio("Aller vers", pages) 


# ______________________________________________________________________________________________________
# Import du jeu de données
# ______________________________________________________________________________________________________

df = pd.read_csv('bank.csv', sep = ',')
#https://github.com/amelievert/streamlit-example/blob/862f21e357b88331e8f0d63567a5e76d95b6958c/bank.csv

# ______________________________________________________________________________________________________
# Préparation des jeux de données à utiliser
# ______________________________________________________________________________________________________

df2 = df.copy()

# Creation de tranches d'âges
df2['t_age'] = pd.cut(x = df2['age'], bins = [17, 30, 40, 50, 65, 96], labels = ['18-30', '30-40','40-50', '50-65','65-95'])

# Creation de tranches de solde compte bancaire = balance
df2['t_balance'] = pd.qcut(x=df2["balance"], q=4, labels=[1,2,3,4])

# Creation de tranches de durée de contact = duration
df2['t_duration'] = pd.qcut(df2["duration"], q=4, labels=[1,2,3,4])

# Creation de tranches de durée de contact = duration
df2['t_duration'] = pd.qcut(df2["duration"], q=4, labels=[1,2,3,4])

# Creation de tranches de nombre de contact = campaign > Corrige le problème de valeurs abbérantes et limite à 4 contacts
df2['t_campaign'] = pd.cut(x = df2['campaign'], bins = [0, 1, 2, 3, 99], labels = [1, 2, 3, 4])

# Création d'une catégorie pour contact campagne précédente oui/non
df2['contact_last_campaign'] = np.where(df2['pdays']>=0, 'yes', 'no')

# Création de tranches en fonction du délai écoulé
df2['t_pdays'] = pd.cut(x = df2['pdays'], bins = [-2, 0, 200, 999], labels = ['NON CONTACTE', 'MOINS DE 200J', 'PLUS DE 200J'])

# Creation de tranches de nombre de contact avant la campagne
df2['previous'] = pd.cut(x = df2['previous'], bins = [0, 1, 2, 3, 99], labels = [1, 2, 3, 4])

# Suppression des colonnes dummies"ées"
drop_cols=['age','balance','duration','campaign','pdays','previous']
df2 = df2.drop(drop_cols, axis=1)

# Création de dummies
var=['marital','education','poutcome','contact','t_age','t_balance','t_duration','t_campaign','t_pdays','month']
df2= df2.join(pd.get_dummies(df2[var], prefix=var))
df2 = df2.drop(df2[var], axis=1)

# Transformation en numérique
le = LabelEncoder()
df2['job2']= le.fit_transform(df2['job'])
df2 = df2.drop(['job'], axis=1)

# Remplace yes/no par 1/0
var = ["default", "housing","loan","deposit","contact_last_campaign"]
df2[var] = df2[var].replace(('yes', 'no'), (1, 0))


# ______________________________________________________________________________________________________
# 1/ Introduction au jeu de données
# ______________________________________________________________________________________________________

if page==pages[0]: 

  st.title("Description du jeu de données")

  st.write("Ce jeu de données est composé de données personnelles sur des clients d’une banque qui ont été “télémarketés” pour souscrire à un produit que l’on appelle un 'dépôt à terme'.")
  st.write("Lorsqu’un client souscrit à ce produit, il place une quantité d’argent dans un compte spécifique et ne pourra pas toucher ces fonds avant l’expiration du terme.")
  st.write("En échange, le client reçoit des intérêts de la part de la banque à la fin du terme.")
  st.write("Le jeu de données est téléchargeable au lien suivant: ")
  st.write("https://www.kaggle.com/janiobachmann/bank-marketing-dataset")


# ---------- Les chiffres clés -----------

  st.header("Les chiffres clés :")
  col1, col2, col3, col4, col5 = st.columns(5)
  col1.write('')
  col2.metric("Nombre de clients", "11 162")
  col3.metric("Nombre de features", "17")
  col4.metric("Proportion des cibles", "47%")
  col5.write('')

# ---------- les variables  -----------

  st.header("Description des variables :")

  var = pd.DataFrame({"Nom des variables": ["age","job","marital","education","default","balance","housing","loan","contact","day","month","duration","campaign","pdays","previous","poutcome","deposit"],
    "Description": ["Age du client","Profession","Statut marital","Niveau d'études","Défaut de paiement","Solde du compte","Prêt immo","Prêt perso",
    "Type de contact","Dernier jour de contact","Dernier mois de  contact","Durée du contact (secondes)","Nombre de contacts","Nb jours écoulés depuis le dernier contact","Nb de contacts",
    "Résultat de la campagne précédente","Résultat de la campagne en cours"]
    })

  st.write(var)

# ---------- Aperçu -----------

  st.header("Aperçu du jeu de données :")
  st.write(df)

# ---------- Ce qu'il faut comprendre -----------

  st.header("Ce qu'il faut retenir :")
  st.write("On remarque que certaines variables sont la résultante de la campagne en cours : ")
  st.write("* contact")
  st.write("* day")
  st.write("* month")
  st.write("* duration")
  st.write("* campaign")
  st.write("La variable [deposit] est notre variable cible.")
  st.write("47% des clients ont répondu favorablement à la campagne (deposit=yes)")

         
# ______________________________________________________________________________________________________
# 2/ Analyse du jeu de données
# ______________________________________________________________________________________________________

if page==pages[1]: 

  st.title("Analyse du jeu de données")

# ---------- Fonction de description -----------

  def describe_df(df):
      """
      Fonction améliorée de description des colonnes, elle permet d'identifier :
      le type de la colonne , le nb de valeur vide (nan), le nb de valeurs uniques, le pourcentage de répartition des valeurs
      INPUT : le dataframe
      OUTPUT : tableau d'analyse
      """
      res = pd.DataFrame(index=["Name","Type", "Nan", "Unique","Min","Max","Values","Pourcentage"])
      for col in df.columns:
          df_col = df[col]
          res[col] = [
              df_col.name,
              df_col.dtype,
              df_col.isnull().sum(),
              len(df_col.unique()),
              df_col.min(),
              df_col.max(),
              df_col.unique(),
              (df_col.value_counts(ascending=False, normalize=True) * 100)
                  .apply(int)
                  .to_json(),
          ]
      return res.T

# ---------- Affichage de la description détaillée -----------

  st.header("Description détaillée des variables")
  st.dataframe(describe_df(df).astype(str))


# ---------- Les correlations -----------

  st.header("Analyse des corrélations")
  tab1, tab2, tab3 = st.tabs(["▩ Matrice", "📈 Chart", "％ Coefficients"])
         
# Matrice de correlation

  col1, col2 = tab1.columns(2)

  le = LabelEncoder()
  df2=df.copy()
  for col in df2.columns:
    df2[col]= le.fit_transform(df2[col])
  
  tab1.subheader("Matrice de corrélation")
  fig = plt.figure(figsize=(20,15))
  sns.heatmap(df2.corr(), annot=True, cmap='RdBu_r', center=0)
  col1.pyplot(fig)
  col2.write('')

# Corrélations directes

  col3, col4 = tab2.columns(2)

  tab2.subheader("Graphiques des corrélations directes")
  corr=pd.DataFrame(df2.corr()["deposit"])
  corr=corr.sort_values("deposit",ascending=False, key=abs)
  fig = plt.figure(figsize=(20,15))
  sns.barplot(data=corr, y=corr.index, x="deposit")
  col3.pyplot(fig)
  col4.write('')

# Corrélations coefficients

  tab3.subheader("Coefficients de corrélation avec la variable cible")
  coef=df2.corr()["deposit"]
  tab3.write(coef)

# ---------- Les distributions par type de variables -----------

  st.subheader("Les distributions par type de variables")
         
  col1, col2 = st.columns(2)
  df2 = df.copy()
  numerics = df2.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).columns
  categoricals= df2.select_dtypes(include=['object','category']).columns

# variables numériques

  tab1, tab2 = col1.tabs(["📈 Chart", "🗃 Describe"])

  option = tab1.selectbox("Choix une variable numérique :",numerics)
  hist = px.histogram(df2,x=option,color="deposit",barmode="group")
  tab1.plotly_chart(hist)
         
  describe= df2[numerics].describe().transpose()
  tab2.write(describe)

  if option=="age":
    col1.write("Les âges extrêmes semblent avoir une plus forte adhérence avec la campagne.")
  elif option=="balance":
    col1.write("RAS")
  elif option=="day":
    col1.write("RAS")
  elif option=="duration":
    col1.write("On remarque que plus la durée de contact augmente et plus les clients semblent souscrire à la campagne.")
  elif option=="campaign":
    col1.write("RAS")
  elif option=="pdays":
    col1.write("RAS")
  elif option=="previous":
    col1.write("RAS")

  st.header("Observations")
  st.write("On remarque que 8 324 clients n'ont pas été contactés lors de la campagne précédente.")
  st.write("Lorsque PREVIOUS = 0 alors PDAYS = -1")

# variables catégorielles

  tab3, tab4 = col2.tabs(["📈 Chart", "🗃 Describe"])

  option = tab3.selectbox("Choix une variable :", categoricals)
  hist = px.histogram(df2,x=option,color="deposit")
  tab3.plotly_chart(hist)
         
  describe= df2[categoricals].describe().transpose()
  tab4.write(describe)

         
