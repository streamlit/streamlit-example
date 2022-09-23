# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit

import os
import sqlite3 as sql
import streamlit as st
from time import sleep
from verify_files import *
from _edit_sql import * 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode


class install():
     def _Init(self, bdd, nom_db):
          self.nom_db = nom_db
          self.progress = st.progress(0)
          _bdd = sql.connect(f'Fichiers\{self.nom_db}')
          try:
               _bdd.execute("SELECT * FROM Catalogue")
               __init = "Catalogue"
               self.title = st.title("Installation de l'application")
               self.sous_titre = st.subheader("Création des tables")
               self.progress.progress(25)
          
          except sql.Error:
               self.title = st.title("Installation de l'application")
               self.sous_titre = st.subheader("Création des tables")
               self.progress = st.progress(0)
               file = st.file_uploader
               self._warning = st.warning
               _file = file("Selectionnez le fichier RPT Catalogue")

               if _file:
                    self._info = st.info("Merci de patientez pendant la vérification du fichier....")
                    verif_file = verify.verify_file(self, _file)
                    if "Catalogue" in verif_file:
                         sleep(0.5)
                         if st.button("Installer la base de données Catalogue"):
                              _csv = verif_file[0]
                              table = verif_file[1]
                              self._info.info("Création de la table en cours")
                              stud_data = pd.read_csv(_csv, sep=',', header=0)#Avec pour délimiteur ',' et on prend les entêtes
                              stud_data.to_sql(table, bdd, if_exists="replace", index=False) #Exportation du fichier .csv vers la base de données
                              sleep(0.5)
                              self._info.info("Table Catalogue créé")
                              self.progress.progress(25)


          try:
               _bdd.execute("SELECT * FROM Effectifs")
               __init = "Catalogue, Effectifs"
               self.progress.progress(50)
          except sql.Error:
               file2 = st.file_uploader
               _file2 = file2("Selectionnez le fichier RPT Effectif")

               if _file2:
                    self._info = st.info("Merci de patientez pendant la vérification du fichier....")
                    verif_file2 = verify.verify_file(self, _file2)
                    if "Effectifs" in verif_file2:
                         sleep(0.5)
                         if st.button("Installer la base de données Effectif"):
                              _csv = verif_file2[0]
                              table = verif_file2[1]
                              self._info.info("Création de la table en cours")
                              stud_data = pd.read_csv(_csv, sep=',', header=0)#Avec pour délimiteur ',' et on prend les entêtes
                              stud_data.to_sql(table, bdd, if_exists="replace", index=False) #Exportation du fichier .csv vers la base de données
                              sleep(0.5)
                              self._info.info("Table Effectifs créé")
                              self.progress.progress(50)
                              st.button("Etape suivante")
          try:
               if "Catalogue, Effectifs" in __init:
                    install._init2(self)
          except : pass

     def _init2(self):
          self.title.title("Installation en cours")
          self.sous_titre.subheader("Choix des personnes et des codes modules à suivre")
          col1, col2, col3, col4 = st.columns(4)
          liste_personne = []
          bdd = sql.connect(f'Fichiers\{self.nom_db}')
          
          with col1:
               st.subheader("Selectionnez les personnes à suivre")
               requette = bdd.execute("SELECT Worker, Employee_ID, Manager_name, Manager_Employee_ID FROM Effectifs")

               for name in requette.fetchall():
                    liste_personne.append((name[0], name[1], name[2], name[3]))
               df = pd.DataFrame(liste_personne, columns=['Personne', 'Chorus', 'Manager', 'Chorus Manager'])

               gb = GridOptionsBuilder.from_dataframe(df)
               gb.configure_column("Personne", headerCheckboxSelection = True, checkboxSelection=True)
               gb.configure_selection(selection_mode='multiple')
               grid_options = gb.build()

               response = AgGrid(
                              df,
                              gridOptions=grid_options,
                              height = 300
                              )
                    
               dftemp = pd.DataFrame(response['data'])
               df = response['data']
               selected = response['selected_rows']
               
  
               with col2:
                    self.info_personnes = st.subheader("Personnes suivies")
                    try:
                         if st.button("Créer les tables de données", key="valider_personnes"):
                              selected_df = pd.DataFrame(selected, columns=['Personne', 'Chorus', 'Manager', 'Chorus Manager'])
                              create_db_workflow = edit.create_db_workflow(self.nom_db, selected_df.values)
                              if create_db_workflow == None:
                                   self.progress.progress(75)
                                   st.write(f"{len(selected_df)} table(s) de créé(s)")
                              else:
                                   st.write(create_db_workflow)

                    except : pass
               
                    
          with col3:
               st.subheader("Selectionnez les codes modules à suivre")


               liste_code = []
               requette = bdd.execute("SELECT Course_code, Métier, Titre_du_cours FROM Catalogue WHERE Course_code<>''")

               for code in requette.fetchall():
                    liste_code.append((code[0], code[1], code[2]))
               df1 = pd.DataFrame(liste_code, columns=['Code module', 'Catégories', 'Description'])

               gb1 = GridOptionsBuilder.from_dataframe(df1)
               gb1.configure_column("Code module", headerCheckboxSelection = True, checkboxSelection=True)
               gb1.configure_selection(selection_mode='multiple')
               grid_options1 = gb1.build()

               response1 = AgGrid(
                              df1,
                              gridOptions=grid_options1,
                              height = 300
                              )
                    
               df1_temp = pd.DataFrame(response1['data'])
               df1 = response1['data']
               selected = response1['selected_rows']
                         


               with col4:
                    self.info_codes_module = st.subheader("Codes modules selectionnés")

                    if st.button("Mise à jour tables personnes"):
                         selected_df1 = pd.DataFrame(selected, columns=['Code module', 'Catégories', 'Description'])
                         update_db_workflow = edit.update_db_workflow(self.nom_db, selected_df1.values)
                         if update_db_workflow == None:
                              st.write("Mise à jour terminée")
                              self.progress.progress(100)
                              install._init3(self.nom_db, finalisation = True)
                         else:
                              st.write(update_db_workflow)


     def _init3(db, finalisation):
          if finalisation == True:
               st.write(os.environ["USERNAME"])

               bdd = sql.connect(f"Fichiers\{db}")

               bdd.execute("""CREATE TABLE Admins (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         nom TEXT NOT NULL,
                         Michelin_ID TEXT NOT NULL
                         )""")
               name, = bdd.execute("SELECT Worker FROM Effectifs WHERE Michelin_ID='{}'".format(os.environ["USERNAME"]))
               bdd.execute("INSERT INTO Admins (id,nom,Michelin_ID) VALUES (1,'{}', '{}')".format(name[0], os.environ["USERNAME"]))
               bdd.commit()
               st.button("Lancer l'application")

          else:
               pass  
               

