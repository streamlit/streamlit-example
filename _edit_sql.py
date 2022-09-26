import sqlite3 as sql
from time import sleep
import datetime
import pandas as pd
import streamlit as st
from datetime import *

# -- Définition des variables globales --
nom_db = "Bdd.db"
bdd = sql.connect(f"Fichiers\{nom_db}", check_same_thread=False)
bdd_cursor = bdd.cursor()


class edit():
    def active_categorie_manager(categorie, manager):
        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        for elements in requette.fetchall():
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        sql_update ="UPDATE S_{} SET Suivi_categories='True', Suivi_module='True' WHERE Suivi_categories='False' AND Categories='{}'".format(ID_Employee, categorie)
                        bdd_cursor.execute(sql_update)
                        bdd.commit()
                except sql.Error as e:
                    return ("Erreur sql : {}".format(str(e)))
                except:
                    pass
        return ("Success")

    def desactive_categorie_manager(categories, manager):
        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
       
        for elements in requette.fetchall():
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        sql_update ="UPDATE S_{} SET Suivi_categories='False', Suivi_module='False' WHERE Suivi_categories='True' AND Categories='{}'".format(ID_Employee, categories)
                        bdd_cursor.execute(sql_update)
                        bdd.commit()
                except sql.Error as e:
                    return ("Erreur sql : {}".format(str(e)))
                except:
                    pass
        return ("Success")

    def desactive_module_manager(module, manager):
        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for elements in requette.fetchall():
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        sql_update ="UPDATE S_{} SET Suivi_module='False' WHERE Suivi_module='True' AND Codes_modules='{}'".format(ID_Employee, module)
                        bdd_cursor.execute(sql_update)
                        bdd.commit()
                except sql.Error as e:
                    return ("Erreur sql : {}".format(str(e)))
                except:
                    pass
        return ("Success")


    def active_module_manager(module, manager):
        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        
        for elements in requette.fetchall():
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        sql_update ="UPDATE S_{} SET Suivi_module='True' WHERE Suivi_module='False' AND Codes_modules='{}'".format(ID_Employee, module)
                        bdd_cursor.execute(sql_update)
                        bdd.commit()     
                except sql.Error as e:
                    return ("Erreur sql : {}".format(str(e)))
                except:
                    pass
        return ("Success")

    def active_value(categorie, manager):
        list_test = []
        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        
        for elements in requette.fetchall():
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        value = bdd.execute("SELECT Suivi_categories FROM S_{} WHERE Categories='{}'".format(ID_Employee, categorie))
                        value = value.fetchone()
                        if value is not None:
                            list_test.append((value[0]))
                        
                except:
                    pass
        print(list_test.count("True"))
        return list_test.count("True")



    def active_module(code, manager):
        
        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        
        for elements in requette.fetchall():
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        value = bdd.execute("SELECT Suivi_module FROM S_{} WHERE Codes_modules='{}'".format(ID_Employee, code))
                        return (value.fetchone())
                except:
                    pass
    
    def update_suivi(csv):
        try:
            stud_data = pd.read_csv(csv, sep=',', header=0)#Avec pour délimiteur ',' et on prend les entêtes
            stud_data.to_sql("Suivi", bdd, if_exists="replace", index=False)
            st.info("Mise à jour de la table 'Suivi' terminée", icon="✅")
            etat = st.info("Mise à jour des tables")

        except sql.Error as e:
            return str(e)

        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = requette.fetchall()
        nb_table = len(table_name) - 6 # -- Compte le nombre de table de la base - les bases qui ne sont pas celles des agents
        percent = round(nb_table / 100) #-- Calcul le % d'avancement pour 100%s
        progress = st.progress(0)
        cnt = 0

        for elements in table_name:
            table = elements[0]
            cnt = cnt + percent

            if cnt < 100:
                progress.progress(cnt)
            else:
                cnt = 0
                progress.progress(100)
            
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                codes_modules = bdd.execute("SELECT Codes_modules FROM S_{}".format(ID_Employee))
                etat.info("Avancement de la mise à jour : {}% | Mise à jour de la table : {}".format(cnt, ID_Employee))



                for codes in codes_modules.fetchall():
                    recherche = bdd.execute("SELECT Enrollment_Date_and_Time_Completed FROM Suivi WHERE Course_Code='{}' AND Workers_Employee_ID='{}' ORDER BY Enrollment_Date_and_Time_Completed DESC".format(codes[0], ID_Employee))
                    date = recherche.fetchone()

                    if date:
                        #date = pd.to_datetime(date).date
                        date = str(date[0]).split(" ")
        
                        date  = datetime.strptime(date[0], '%Y-%m-%d').strftime("%d-%m-%Y")
                        update ="UPDATE S_{} SET Date_fait='{}' WHERE Codes_modules='{}'".format(ID_Employee, str(date), codes[0])
                        bdd_cursor.execute(update)
                        bdd.commit()
                        


        st.info("Mise à jour des tables 'Personnes' terminée.")
        
        st.session_state["Menu_maj"] = False
        st.experimental_rerun()

    def update_catalogue(csv):
        st.info("Mise à jour de la table 'Catalogue' en cours")
        try:
            stud_data = pd.read_csv(csv, sep=',', header=0)#Avec pour délimiteur ',' et on prend les entêtes
            stud_data.to_sql("Catalogue", bdd, if_exists="replace", index=False)
            st.info("Mise à jour de la table 'Catalogue' terminée")

        except sql.Error as e:
            return str(e)

        st.session_state["Menu_maj"] = False
        st.experimental_rerun()        


    def update_effectifs(csv):
        st.info("Mise à jour de la table 'Effectifs' en cours")
        try:
            stud_data = pd.read_csv(csv, sep=',', header=0)#Avec pour délimiteur ',' et on prend les entêtes
            stud_data.to_sql("Effectifs", bdd, if_exists="replace", index=False)
            st.info("Mise à jour de la table 'Effectifs' terminée")

        except sql.Error as e:
            return str(e)

        st.session_state["Menu_maj"] = False
        st.experimental_rerun()

    def verif_cat_personne(chorus, categorie):
        try:
            requet = bdd.execute("SELECT Suivi_categories FROM S_{} WHERE Categories='{}'".format(chorus, categorie))
            return requet.fetchall()
        except sql.Error as e:
            return(f"Erreur Sql : {str(e)}")

    def verif_module_personne(chorus, code_module):

        try:
            requet = bdd.execute("SELECT Suivi_module, Suivi_categories FROM S_{} WHERE Codes_modules='{}'".format(chorus, code_module))
            return requet.fetchall()

        except sql.Error as e:
            return ("Erreur Sql : {}".format(str(e)))
     
    def active_module_personne(chorus, code_module):
        
        try :
            sql_update ="UPDATE S_{} SET Suivi_module='True' WHERE Suivi_module='False' AND Codes_modules='{}'".format(chorus, code_module)
            bdd_cursor.execute(sql_update)
            bdd.commit()
            return("Success")

        except sql.Error as e:
            return ("Erreur SQL : {}".format(str(e)))


    def desactive_module_personne(chorus, code_module):
        
        try :
            sql_update ="UPDATE S_{} SET Suivi_module='False' WHERE Suivi_module='True' AND Codes_modules='{}'".format(chorus, code_module)
            bdd_cursor.execute(sql_update)
            bdd.commit()
            return("Success")
            
        except sql.Error as e:
            return ("Erreur SQL : {}".format(str(e)))

    def active_categorie_personne(chorus, categorie):
        
        try :
            sql_update ="UPDATE S_{} SET Suivi_categories='True' WHERE Suivi_categories='False' AND Categories='{}'".format(chorus, categorie)
            bdd_cursor.execute(sql_update)
            bdd.commit()
            return("Success")

        except sql.Error as e:
            return ("Erreur SQL : {}".format(str(e)))

    def desactive_categorie_personne(chorus, categorie):
        
        try :
            sql_update ="UPDATE S_{} SET Suivi_categories='False' WHERE Suivi_categories='True' AND Categories='{}'".format(chorus, categorie)
            bdd_cursor.execute(sql_update)
            bdd.commit()
            return("Success")

        except sql.Error as e:
            return ("Erreur SQL : {}".format(str(e)))

    def update_date(chorus, ladate, code):
        ladate = datetime.strptime(ladate, "%d-%m-%Y")
        datelimite = ladate + timedelta(days=(365*4))

        verif = bdd.execute("SELECT Date_fait FROM S_{} WHERE Codes_modules='{}'".format(chorus, code))

        if verif:
            date_fait = verif.fetchone()
            if date_fait[0]:
                date_fait = datetime.strptime(date_fait[0], "%d-%m-%Y")

            if ladate != date_fait:
                try:
                    ladate = datetime.strftime(ladate, "%d-%m-%Y")
                    limite = datetime.strftime(datelimite, "%d-%m-%Y")
                    sql_update ="UPDATE S_{} SET Date_fait='{}', Date_fin='{}' WHERE Codes_modules='{}'".format(chorus, str(ladate), str(limite), code)
                    bdd_cursor.execute(sql_update)
                    bdd.commit()
                    success = st.info(f"Mise à jour effectuée avec succès pour le module {code}")
                    sleep(2)
                    st.experimental_rerun()

                except sql.Error as e:
                    st.warning(f"Erreur pendant la mise à jour. Erreur retournée : {str(e)}")                   

    def update_rappel(chorus, code):
        jour_rappel = datetime.strftime(datetime.now(), "%d-%m-%Y")

        try:
            sql_update ="UPDATE S_{} SET Rappel_mail='{}', Date_rappel='{}' WHERE Codes_modules='{}'".format(chorus, 'True', str(jour_rappel), code)
            bdd_cursor.execute(sql_update)
            bdd.commit()
            
        
        except sql.Error as e:
            return str(e)

    def create_db_workflow(db, liste):
        st.write(liste)
        for elem in liste:
            table = f"S_{elem[1]}"

            try:
                bdd.execute("""CREATE TABLE IF NOT EXISTS {} (
                                Suivi_personne BOOLEAN,
                                Codes_modules TEXT,
                                Intitules_codes_modules TEXT,
                                Categories TEXT,
                                Suivi_module BOOLEAN,
                                Suivi_categories TEXT,
                                Date_fait DATE,
                                Date_fin DATE,
                                Duree_validite INTEGER,
                                Rappel_mail BOOLEAN,
                                Date_rappel DATE,
                                Manager TEXT
                            )""".format(table))

            except sql.Error as e:
                return(str(e))

    def update_db_workflow(db, liste):
        requette = bdd.execute("SELECT name FROM sqlite_master WHERE type='table';")
                
        for elements in requette:
            if "S_" in elements[0]:
                table = str(elements[0]).replace("S_", "")
                manager, = bdd.execute(f"SELECT Manager_name FROM Effectifs WHERE Employee_ID='{table}'")
                manager = manager[0]

                try:
                    for code in liste:
                        if code[1] == "Production": 
                            duree_validite = 4 
                        else:
                            duree_validite = 0

                        bdd.execute("""INSERT INTO S_{} (
                            Suivi_personne,
                            Codes_modules,
                            Intitules_codes_modules,
                            Categories,
                            Suivi_module,
                            Suivi_categories,
                            Date_fait,
                            Date_fin,
                            Duree_validite,
                            Rappel_mail,
                            Date_rappel,
                            Manager)
                            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}') """.format(table, True, code[0], code[2], code[1], True, True, "", "", duree_validite, False, "", manager))
                        bdd.commit()

                except sql.Error as e:
                    return(str(e))



