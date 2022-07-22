
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

from sklearn.metrics import accuracy_score, plot_confusion_matrix, roc_curve, roc_auc_score, auc, precision_score, recall_score, classification_report
from sklearn import linear_model, neighbors, svm, tree, ensemble
from sklearn.model_selection import GridSearchCV, train_test_split

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


# ______________________________________________________________________________________________________
# 1/ Introduction au jeu de données
# ______________________________________________________________________________________________________

if page==pages[0]: 

  st.title("Description du jeu de données")

  st.markdown(
           "Ce jeu de données est composé de données personnelles sur des clients d’une banque qui ont été “télémarketés” pour souscrire à un produit "
           "que l’on appelle un 'dépôt à terme'. "
           "Lorsqu’un client souscrit à ce produit, il place une quantité d’argent dans un compte spécifique et ne pourra pas toucher ces fonds avant l’expiration "
           "du terme."
           "En échange, le client reçoit des intérêts de la part de la banque à la fin du terme.  \n" 
           "Le jeu de données est téléchargeable au lien suivant :"
           "https://www.kaggle.com/janiobachmann/bank-marketing-dataset")
         
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
  st.image("Describe.png")

  #var = pd.DataFrame({"Nom des variables": ["age","job","marital","education","default","balance","housing","loan","contact","day","month","duration","campaign","pdays","previous","poutcome","deposit"],
  #  "Description": ["Age du client","Profession","Statut marital","Niveau d'études","Défaut de paiement","Solde du compte","Prêt immo","Prêt perso",
  #  "Type de contact","Dernier jour de contact","Dernier mois de  contact","Durée du contact (secondes)","Nombre de contacts","Nb jours écoulés depuis le dernier contact","Nb de contacts",
  #  "Résultat de la campagne précédente","Résultat de la campagne en cours"]
  #  })

  #st.write(var)

# ---------- Aperçu -----------

  describe = st.checkbox("Aperçu du jeu de données")
  if describe:
    st.write(df)

# ---------- Ce qu'il faut comprendre -----------

  st.header("Ce qu'il faut retenir :")
  st.markdown(
           "On remarque que certaines variables sont la résultante de la campagne en cours : \n"
           "* contact \n"
           "* day \n"
           "* month \n"
           "* duration \n"
           "* campaign \n"
           "La variable **deposit** est notre variable cible.")
         
# ______________________________________________________________________________________________________
# 2/ Analyse du jeu de données
# ______________________________________________________________________________________________________

if page==pages[1]: 

  st.title("Analyse du jeu de données")
  st.markdown(
           "L’analyse descriptive est le terme donné à l’analyse des données permettant de décrire et de résumer des données historiques de manière significative "
           "afin que des **insights** en ressortent.\n"
           "L’analyse descriptive de notre jeu de données va nous fournir les informations de base sur les variables, leur répartition, et leurs relations potentielles. \n"
           "Nous allons pouvoir observer - _à première vue_ - les éléments qui ont favorisé, ou à l'inverse défavorisé, la performance de la campagne commerciale.")

# ---------- Les distributions par type de variables -----------

  st.subheader("Les distributions par type de variables")
         
  col1, col2 = st.columns(2)
  col1.subheader("Variables numériques")
  col2.subheader("Variables catégorielles")
  df2 = df.copy()
  numerics = df2.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).columns
  categoricals= df2.select_dtypes(include=['object','category']).columns

# variables numériques

  tab1, tab2 = col1.tabs(["📈 Chart", "📋 Describe"])
         
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

# variables catégorielles

  tab3, tab4 = col2.tabs(["📈 Chart", "📋 Describe"])

  option = tab3.selectbox("Choix une variable catégorielle :", categoricals)
  hist = px.histogram(df2,y=option,color="deposit",barmode="group")
  tab3.plotly_chart(hist)
         
  describe= df2[categoricals].describe().transpose()
  tab4.write(describe)


# ---------- Les correlations -----------

  st.header("Analyse des corrélations")
  tab1, tab2 = st.tabs(["▩ Matrice", "📈 Chart"])
         
# Matrice de correlation

  col1, col2 = tab1.columns((2, 1))

  le = LabelEncoder()
  df2=df.copy()
  for col in df2.columns:
    df2[col]= le.fit_transform(df2[col])
  
  fig = plt.figure(figsize=(15,10))
  sns.heatmap(df2.corr(), annot=True, cmap='RdBu_r', center=0)
  col1.pyplot(fig)
  col2.write('')

# Corrélations directes

  col3, col4 = tab2.columns((3, 1))

  corr=pd.DataFrame(df2.corr()["deposit"])
  corr=corr.sort_values("deposit",ascending=False, key=abs)
         
  fig = plt.figure(figsize=(10,5))
  df2.corr()['deposit'].sort_values().drop('deposit').plot(kind='bar', cmap='viridis')
  col3.pyplot(fig)

# Corrélations coefficients

  coef=df2.corr()["deposit"]
  col4.write(coef)


# ---------- Les observations -----------

  st.header("Observations")
  st.info(
           "On remarque que 8 324 clients n'ont pas été contactés lors de la campagne précédente. \n"
           "Lorsque PREVIOUS = 0 alors PDAYS = -1")
  st.info(
           "Dans l'ordre, les variables les plus corrélées (valeur absolue) avec la target _[deposit]_ sont \n"
           "* **_duration_** = Durée du contact (en secondes) \n"
           "* **_contact_** = Type de contact \n"
           "* housing = Prêt immo \n"
           "* previous = Nb contacts au cours de la campagne précédente \n"
           "* housing = pdays = Nb jours écoulés depuis le dernier contact de la campagne précédente \n"
           "* previous = balance = Solde compte bancaire \n"
           "**Attention** , les **_deux variables_** correspondent à des données non connues à priori (avant lancement de la campagne)")
         
# ______________________________________________________________________________________________________
# 3/ Préprocessing
# ______________________________________________________________________________________________________

if page==pages[2]: 

  st.title("Préprocessing - Modèles prédictifs")


# ---------- Le préprocessing, ça sert à quoi -----------

  expander1 = st.expander("Le préprocessing, ça sert à quoi ?")

  expander1.markdown(
           "Le préprocessing est une de composante essentielle de la data science. "
           "Cette étape décrit toutes les **transformations** effectuées sur le jeu de données initial et indispensables à la création du modèle d'apprentissage fiable et robuste. "
           "Les algorithmes d'apprentissage automatique fonctionnent mieux lorsque les données sont présentées dans un format qui met en évidence les aspects pertinents requis pour résoudre un problème. "
           "Les fonctions de préprocessing consistent à **restructurer** les données brutes sous une forme adaptée à des types particuliers d'algorithmes. Les étapes sont : "
           "/n"
           "* la transformation des données, \n"
           "* la réduction des données, \n"
           "* la sélection des variables \n"
           "* et à la mise à l'échelle \n")
  
  expander1.image('preprocessing.JPG', caption='Les étapes de préprocessing')     


# ---------- Les étapes de préprocessing -----------

  st.header("Les étapes de préprocessing appliquées :")

# Variables numériques

  st.subheader("Le traitement des variables numériques")
  code = ''' 
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
    '''
  st.code(code, language='python')

# Variables catégorielles

  st.subheader("Le traitement des variables catégorielles")
  code = ''' 
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
    '''
  st.code(code, language='python')

         
# ---------- Jeu de données final -----------

  st.header("Le jeu de données final :")
  st.write(df2)
         
# ---------- Arbre de correlations après preprocessing -----------

  st.header("Arbre de correlations après preprocessing :")

  fig = plt.figure(figsize=(20,8))
  df2.corr()['deposit'].sort_values().drop('deposit').plot(kind='bar', cmap='viridis')
  st.pyplot(fig)
         


# ---------- Les enseignements -----------

  st.header("Les observations :")
  st.info(
           "On voit clairement que la feature **[duration]** impacte positivement la campagne dès lors que la valeur est élevée (temps de contact)."
           "\n Egalement, les clients ayant répondu favorablement à la campagne précédente **[poutcome]** semblent être les plus susceptibles de renouveler leur action."
           "\n Les mois de mars et octobre [month] semblent être les meilleurs mois pour optimiser les leads.")


# ______________________________________________________________________________________________________
# 4/ Challenge de modèles
# ______________________________________________________________________________________________________

if page==pages[3]: 

  st.title("Modèles prédictifs")
     

# ---------- Initialisation du jeu de données -----------

  df3=df2.copy()

# ---------- Split jeu entrainement et jeu de test -----------

  # Isoler les features de la target
  target = df3['deposit']
  feats = df3.drop(['deposit'], axis=1)

  # Séparation des données en jeu d'entraînement et de test
  from sklearn.model_selection import train_test_split
  X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.25)

  # Normaliser les données - MinMaxScaler
  scaler = MinMaxScaler()
  X_train = scaler.fit_transform(X_train)
  X_test = scaler.transform(X_test)

  # Sauvegarde des résulats de chacun des modèles
  models=[]
  scores =[]
  precision=[]
  rappel=[]
  roc=[]

# ---------- Les 3 modèles -----------

  col1, col2, col3, col4 = st.columns(4)

# Régression logistique -----------------------------------------------------------------------

  with col1:
    expander = st.expander("Modèle RLC")
    rlc = linear_model.LogisticRegression(C=10)
    rlc.fit(X_train, y_train)
        
    expander.metric("Score train", "{:.2%}".format(rlc.score(X_train, y_train)))
    expander.metric("Score test", "{:.2%}".format(rlc.score(X_test, y_test)))
    expander.metric("Precision Score", "{:.2%}".format(precision_score(y_test, rlc.predict(X_test))))

    y_pred = rlc.predict(X_test)
    expander.write("Matrice de confusion :")
    expander.write(pd.crosstab(y_test, y_pred, rownames=['Classe réelle'], colnames=['Classe prédite']))

    # Sauvegarde des résultats
    models.append("Regression logistique")
    scores.append(rlc.score(X_test, y_test))
    precision.append(precision_score(y_test, rlc.predict(X_test)))
    rappel.append(recall_score(y_test, rlc.predict(X_test)))
    roc.append(roc_auc_score(y_test, rlc.predict(X_test)))
    probs_rlc = rlc.predict_proba(X_test)

# K plus proche voisins -----------------------------------------------------------------------

  with col2:
    expander = st.expander("Modèle KNN")

    knn = neighbors.KNeighborsClassifier(n_neighbors=39)
    knn.fit(X_train, y_train)
      
    expander.metric("Score train", "{:.2%}".format(knn.score(X_train, y_train)))
    expander.metric("Score test", "{:.2%}".format(knn.score(X_test, y_test)))
    expander.metric("Precision Score", "{:.2%}".format(precision_score(y_test, knn.predict(X_test))))

    y_pred = knn.predict(X_test)
    expander.write("Matrice de confusion :")
    expander.write(pd.crosstab(y_test, y_pred, rownames=['Classe réelle'], colnames=['Classe prédite']))

    # Sauvegarde des résultats
    models.append("K plus proches voisins")
    scores.append(knn.score(X_test, y_test))
    precision.append(precision_score(y_test, knn.predict(X_test)))
    rappel.append(recall_score(y_test, knn.predict(X_test)))
    roc.append(roc_auc_score(y_test, knn.predict(X_test)))
    probs_knn = knn.predict_proba(X_test)

# Arbre de décision -----------------------------------------------------------------------

  with col3:
    expander = st.expander("Modèle DTC")

    dtc = tree.DecisionTreeClassifier(max_depth=9)
    dtc.fit(X_train, y_train)  
        
    expander.metric("Score train", "{:.2%}".format(dtc.score(X_train, y_train)))
    expander.metric("Score test", "{:.2%}".format(dtc.score(X_test, y_test)))
    expander.metric("Precision Score", "{:.2%}".format(precision_score(y_test, dtc.predict(X_test))))

    y_pred = dtc.predict(X_test)
    expander.write("Matrice de confusion :")
    expander.write(pd.crosstab(y_test, y_pred, rownames=['Classe réelle'], colnames=['Classe prédite']))

    # Sauvegarde des résultats
    models.append("Decision Tree")
    scores.append(dtc.score(X_test, y_test))
    precision.append(precision_score(y_test, dtc.predict(X_test)))
    rappel.append(recall_score(y_test, dtc.predict(X_test)))
    roc.append(roc_auc_score(y_test, dtc.predict(X_test)))
    probs_dtc = dtc.predict_proba(X_test)

# Random Forest -----------------------------------------------------------------------

  with col4:
    expander = st.expander("Modèle RFC")

    rfc = ensemble.RandomForestClassifier(n_jobs=1) 
    rfc.fit(X_train, y_train)
    
    expander.metric("Score train", "{:.2%}".format(rfc.score(X_train, y_train)))
    expander.metric("Score test", "{:.2%}".format(rfc.score(X_test, y_test)))
    expander.metric("Precision Score", "{:.2%}".format(precision_score(y_test, rfc.predict(X_test))))

    y_pred = rfc.predict(X_test)
    expander.write("Matrice de confusion :")
    expander.write(pd.crosstab(y_test, y_pred, rownames=['Classe réelle'], colnames=['Classe prédite']))

    # Sauvegarde des résultats
    models.append("Random Forest")
    scores.append(rfc.score(X_test, y_test))
    precision.append(precision_score(y_test, rfc.predict(X_test)))
    rappel.append(recall_score(y_test, rfc.predict(X_test)))
    roc.append(roc_auc_score(y_test, rfc.predict(X_test)))
    probs_rfc = rfc.predict_proba(X_test)


# Comparaison des résultats -----------------------------------------------------------------------

  st.header("Comparaison des 4 modèles")

  # Recap des scores
  compare = pd.DataFrame(models)
  compare.columns = ['model']
  compare["accuracy"]=scores
  compare["precision"]=precision
  compare["rappel"]=rappel
  compare["roc"]=roc

  #Graphique de comparaison des résultats         
  #fig = plt.figure(figsize=(20,10))
  #compare.plot.bar(x = 'model', y=['accuracy', 'precision', 'rappel','roc'],stacked=False, rot=90)
  #plt.ylim([0.5, 1])
  #plt.axhline(y=0.80, color='k', linewidth=2, linestyle='--')
  #plt.title("Compare Models")
  #st.pyplot(fig)

  fig = plt.figure(figsize=(20,10))
  bar = px.bar(compare, x="model", y=['accuracy', 'precision', 'rappel','roc'], barmode='group')
  bar.add_trace(px.line(compare,x = 'model', y=0.8))
  st.plotly_chart(bar)     

  # Comparaison avec l'indice des ROC
  fig = plt.figure(figsize=(20,10))

  # Regression logistique
  fpr, tpr, seuils = roc_curve(y_test, probs_rlc[:,1])
  roc_auc = auc(fpr, tpr)
  plt.plot(fpr, tpr, color='green', lw=2, label='Modèle RLC (auc = %0.2f)' % roc_auc)

  # K plus proches voisins
  fpr, tpr, seuils = roc_curve(y_test, probs_knn[:,1])
  roc_auc = auc(fpr, tpr)
  plt.plot(fpr, tpr, color='blue', lw=2, label='Modèle KNN (auc = %0.2f)' % roc_auc)

  # Decision Tree
  fpr, tpr, seuils = roc_curve(y_test, probs_dtc[:,1])
  roc_auc = auc(fpr, tpr)
  plt.plot(fpr, tpr, color='orange', lw=2, label='Modèle DTC (auc = %0.2f)' % roc_auc)

  # Random Forest
  fpr, tpr, seuils = roc_curve(y_test, probs_rfc[:,1])
  roc_auc = auc(fpr, tpr)
  plt.plot(fpr, tpr, color='red', lw=2, label='Modèle RFC (auc = %0.2f)' % roc_auc)

  plt.plot([0, 1], [0, 1], color='black', lw=2, linestyle='--', label='Aléatoire (auc = 0.5)')
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('Taux faux positifs')
  plt.ylabel('Taux vrais positifs')
  plt.title('Courbe ROC pour modèle Random Forest')
  plt.legend(loc="lower right")
  st.pyplot(fig)

  st.write("Le modèle Random Forest semble le plus équilibré. Il permet de maximiser les positifs.")
