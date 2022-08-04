# ______________________________________________________________________________________________________
# Import des bibliothèques
# ______________________________________________________________________________________________________

import pandas as pd
import seaborn as sns
import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb
import matplotlib.pyplot as plt
import plotly.express as px

#import joblib
from joblib import dump, load

import xgboost as xgb
from xgboost import XGBClassifier
from xgboost import XGBRegressor
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

st.set_page_config(page_title="JAD'Up",  layout='wide', page_icon='Agence de Marketing.ico')

st.sidebar.title("Sommaire")
st.sidebar.image('Agence de Marketing.ico')

pages = ["📋 Introduction au jeu de données",
         "📊 Analyse",
         "🧪 Preprocessing",
         "🔮 Challenge de modèles",
         "🔍 Interprétabilité",
         "⚙️ Personnaliser votre campagne"]

page = st.sidebar.radio("Aller vers", pages) 


# ______________________________________________________________________________________________________
# Import du jeu de données et des modèles à utiliser
# ______________________________________________________________________________________________________

df = pd.read_csv('bank.csv', sep = ',')
rlc = load('Regression logistique.joblib')
knn = load('K plus proches voisins.joblib')
dtc = load('Decision Tree Classifier.joblib')
rfc = load('Random Forest Classifier.joblib')
###
xgbc = load('Random Forest Classifier.joblib')
compare = pd.read_csv('compare_scores.csv', sep = ',')

rlc_accuracy=compare.iloc[0]["accuracy"]
knn_accuracy=compare.iloc[1]["accuracy"]
dtc_accuracy=compare.iloc[2]["accuracy"]
rfc_accuracy=compare.iloc[3]["accuracy"]
xgb_accuracy=compare.iloc[4]["accuracy"]

rlc_precision=compare.iloc[0]["precision"]
knn_precision=compare.iloc[1]["precision"]
dtc_precision=compare.iloc[2]["precision"]
rfc_precision=compare.iloc[3]["precision"]
xgb_precision=compare.iloc[4]["precision"]

rlc_rappel=compare.iloc[0]["rappel"]
knn_rappel=compare.iloc[1]["rappel"]
dtc_rappel=compare.iloc[2]["rappel"]
rfc_rappel=compare.iloc[3]["rappel"]
xgb_rappel=compare.iloc[4]["rappel"]



