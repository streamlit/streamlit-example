# @Project:  Suivi formations
# @Email:  benoit.ghirardini@michelin.com
# @Author: Benoit Ghirardini
# @Date: Août 2022
# @Version: 1.0


#       ---- MAIN ----
# -- Sous programme principal --
# Connection à la base de données
# Execution des requettes


# -- Importation des bibliothèques
from calendar import c, month

from datetime import date, datetime, timedelta
from time import *
import sqlite3 as sql
import pandas as pd
import streamlit as st # pip install streamlit




nom_db = "Bdd.db"
# -- Définition des variables globales --
bdd = sql.connect(f"Fichiers\{nom_db}", check_same_thread=False)
bdd_cursor = bdd.cursor()



compt_reactu_tot_metier = 0
compt_reactu_tot_metier_fait = 0


# -- Classe principale
class Init():
    def _Init(self):
        Init.list_personnes()
        pass

    # -- Fonction qui permet de recuperer la liste des personnes suivies
    def list_personnes():
        # -- Variables utilisées:
        #   -Liste des personnes suivies // @list_workflow
        list_workflow = []
        list_manager = []
        list_Chorus = []
        list_manager.append("Synthèse atelier")


        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for elements in requette:
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Worker, Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                if temp:
                    list_workflow.append(temp[0])
                    list_Chorus.append((temp[0], ID_Employee))
                try:
                    if temp[1] in list_manager:
                        pass
                    else:
                        list_manager.append(temp[1])
                except:
                    pass
                
        return list_workflow, list_manager, list_Chorus
    
    def list_manageurs(self, manager):
        # -- Variables utilisées:
        #   -Liste des manageurs suivis // @list_manager        
        pass    

# -- Classe synthèse --
# - Gestion de la partie synthèse atelier -
class synthese():
    # -- Fonction Synth_atelier
    # -- Fonction qui permet de récuperer toutes les infos pour la synthèse atelier
    def Synth_Atelier(): 
        # -- Variables utilisées:
        #   -Nombre de formations total à faire // @total_number_of_training
        #   -Nombre de formations effectuées // @total_number_of_training_done
        #   -Nombre de formations effectuées hors suivi // @total_number_of_training_not_followed
        #   -Nombre de formations restantes // @total_number_of_training_remaining
        
        end_year = datetime.now().year -1
        year = datetime.now().year

        date_of_reactu = "31-12-{}".format(end_year)
        date_of_reactu = datetime.strptime(date_of_reactu, '%d-%m-%Y')
        date_limit_of_reactu = "31-12-{}".format(year)
        date_limit_of_reactu = datetime.strptime(date_limit_of_reactu, '%d-%m-%Y')
        date_now = datetime.now()


        total_number_of_training = 0
        total_number_of_training_done = 0
        total_number_of_training_remaining = 0
        total_number_of_training_not_followed = 0
        total_number_of_update = 0
        codes_modules_seuil = []
        total_number_of_update_done = 0

        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for elements in requette:
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                number_of_training, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='True'".format(ID_Employee))
                number_of_training_done, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='True' and Date_fait<>''".format(ID_Employee))
                number_of_training_not_followed, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='False' and Date_fait<>''".format(ID_Employee))
                #number_of_update, = bdd.execute("SELECT COUNT (*) FROM S_{} WHERE Suivi_module='True' AND Categories='Metiers' AND Date_fin>'{}' AND Date_fin<='{}'".format(ID_Employee, date_of_reactu, date_limit_of_reactu))
                recup_date = bdd.execute("SELECT Date_fin, Codes_modules, Intitules_codes_modules FROM S_{} WHERE Suivi_module='True' AND Categories='Metiers' AND Date_fin<>''".format(ID_Employee))
                for elem in recup_date:
                    
                    if elem[0] != '?':
                        ladate = datetime.strptime(elem[0], '%d-%m-%Y')
                        if ladate > date_of_reactu and ladate < date_limit_of_reactu:
                            total_number_of_update +=1
                            jour = ladate - datetime.now()
                            seuil_alerte_90j = ladate - timedelta(days=90)
                            


                            if date_now > seuil_alerte_90j:
                                codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, "📧"))
                            else:
                                codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, ""))

                
                recup_date = bdd.execute("SELECT Date_fait FROM S_{} WHERE Suivi_module='True' AND Categories='Metiers' AND Date_fait<>''".format(ID_Employee))
                for elem in recup_date:
                    if elem[0] != '':
                        ladate = datetime.strptime(elem[0], '%d-%m-%Y')
                        if ladate > date_of_reactu and ladate < date_limit_of_reactu:
                            total_number_of_update_done +=1

            # Comptage
                total_number_of_training = total_number_of_training + number_of_training[0]
                total_number_of_training_done = total_number_of_training_done + number_of_training_done[0]
                total_number_of_training_not_followed = total_number_of_training_not_followed + number_of_training_not_followed[0]
                total_number_of_training_remaining = total_number_of_training - total_number_of_training_done

        
        
        if total_number_of_update_done != 0:
            rate_respect = round(((total_number_of_update / total_number_of_update_done) / 100), 2)
        else:
            rate_respect = 0

        # Renvoie les données
        return total_number_of_training, total_number_of_training_done, total_number_of_training_remaining, total_number_of_training_not_followed, total_number_of_update, rate_respect, codes_modules_seuil
        




    # -- Fonction pour récupèrer la synthèse équipe de chaque manageurs
    def Synth_manager(manager):
        # -- Variable utilisées:
        #   -Nombre de formations à faire // @total_number_of_training
        #   -Nombre de formations effectuées // @total_number_of_training_done
        #   -Nombre de formations restantes // @total_number_of_training_remaining
        #   -Nombre d'actualisations pour la catégories metiers à faire // @number_of_update
        #   -Nombre d'actualisations effectuées // @number_of_update_done
        #   -Taux de respect (% d'actualisation effectuées/actualisation à faire) // @rate_respect
        end_year = datetime.now().year -1
        year = datetime.now().year
        st.write(manager)
        date_of_reactu = "31-12-{}".format(end_year)
        date_of_reactu = datetime.strptime(date_of_reactu, '%d-%m-%Y')
        date_limit_of_reactu = "31-12-{}".format(year)
        date_limit_of_reactu = datetime.strptime(date_limit_of_reactu, '%d-%m-%Y')
        date_now =datetime.now()

        total_number_of_training = 0
        total_number_of_training_done = 0
        total_number_of_training_remaining = 0
        total_number_of_training_not_followed = 0
        total_number_of_update = 0
        total_number_of_update_metier = 0
        total_number_of_update_done = 0
        total_workflow = 0
        codes_modules_seuil = []
        list_cats = []
        list_personnes = []
        list_personnes_hors_suivi = []

        list_personnes = bdd.execute("SELECT Employee_ID, Worker FROM Effectifs WHERE Manager_name='{}'".format(manager))


        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for elements in requette:
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne

                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:

                    if temp[0] == manager:
                        requette_cat = bdd.execute("SELECT DISTINCT Categories FROM S_{}".format(ID_Employee))
                        number_of_training, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True'".format(ID_Employee))
                        number_of_training_done, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' and Date_fait<>''".format(ID_Employee))
                        number_of_training_not_followed, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='False' AND Suivi_module='False' and Date_fait<>''".format(ID_Employee))
                        number_of_update, = bdd.execute("SELECT COUNT(Codes_modules) FROM S_{} WHERE Categories='Metiers' AND Suivi_module='True' AND Suivi_categories='True'".format(ID_Employee))
                        recup_date = bdd.execute("SELECT Date_fin, Codes_modules, Intitules_codes_modules FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' AND Categories='Metiers' AND Date_fin<>''".format(ID_Employee))
                        
                        for elem in recup_date:
                            
                            if elem[0] != '?':
                                ladate = datetime.strptime(elem[0], '%d-%m-%Y')
                                jour = ladate - datetime.now()

                                if ladate > date_of_reactu and ladate < date_limit_of_reactu:
                                    total_number_of_update +=1

                                    seuil_alerte_90j = ladate - timedelta(days=90)

                                    if date_now > seuil_alerte_90j:
                                        codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, "📧"))
                                    else:
                                        codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, ""))
                        recup_date = bdd.execute("SELECT Date_fait FROM S_{} WHERE Suivi_module='True' AND Categories='Metiers' AND Date_fait<>''".format(ID_Employee))

                        for elem in recup_date:
                            if elem[0] != '':
                                ladate = datetime.strptime(elem[0], '%d-%m-%Y')
                                if ladate > date_of_reactu and ladate < date_limit_of_reactu:
                                    print(ladate)
                                    total_number_of_update_done +=1


                        # Ajout dans la liste cat
                        for elem in requette_cat:
                            if elem[0] in list_cats:
                                pass
                            else:
                                list_cats.append(elem[0])
                            
                        # Comptage
                        total_number_of_training = total_number_of_training + number_of_training[0]
                        total_number_of_training_done = total_number_of_training_done + number_of_training_done[0]
                        total_number_of_training_not_followed = total_number_of_training_not_followed + number_of_training_not_followed[0]
                        total_number_of_training_remaining = total_number_of_training - total_number_of_training_done
                        total_number_of_update_metier = total_number_of_update_metier + number_of_update[0]
                        total_workflow = total_workflow +1
                except:
                    pass
                    

        print("Codes modules {}:".format(total_number_of_update_metier))
        print("Fait : {}".format(total_number_of_update_done))
        print("Effectif : {}".format(total_workflow))

        if total_number_of_update_metier != 0:
            rate_respect = round(((total_number_of_update_done / total_number_of_update_metier) * 100) , 1)
            print(rate_respect)
        else:
            rate_respect = 0
    

        return total_number_of_training, total_number_of_training_done, total_number_of_training_remaining, total_number_of_training_not_followed, total_number_of_update, rate_respect, total_workflow, list_cats, list_personnes.fetchall(), list_personnes_hors_suivi, codes_modules_seuil


    def Synth_codes_modules(manager, categories):
        list_codes = []
        list_intitule = []
        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        for elements in requette:
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        requette_code = bdd.execute("SELECT Codes_modules, Intitules_codes_modules FROM S_{} WHERE Categories='{}' AND Suivi_categories='True'".format(ID_Employee, categories))
                        
                        # Ajout dans la liste cat
                        for elem in requette_code:
                            if elem[0] in list_codes:
                                pass
                            else:
                                list_codes.append((elem[0], elem[1]))
                except:
                    pass
        
        return list_codes
        
    def Synth_codes_workflow(personne, categories):
        requette_code = bdd.execute("SELECT Codes_modules, Intitules_codes_modules FROM S_{} WHERE Categories='{}' AND Suivi_categories='True'".format(personne, categories))
        return requette_code.fetchall()

        

    # -- Fonction pour récupèrer la synthese de la personne selectionnée
    def Synth_personne(personne):
        # -- Variable utilisées:
        #   -Nombre de formations à faire // @total_number_of_training
        #   -Nombre de formations effectuées // @total_number_of_training_done
        #   -Nombre de formations restantes // @total_number_of_training_remaining
        #   -Nombre d'actualisations pour la catégories metiers à faire // @number_of_update
        #   -Nombre d'actualisations effectuées // @number_of_update_done
        #   -Taux de respect (% d'actualisation effectuées/actualisation à faire) // @rate_respect
        end_year = datetime.now().year -1
        year = datetime.now().year

        date_of_reactu = "31-12-{}".format(end_year)
        date_of_reactu = datetime.strptime(date_of_reactu, '%d-%m-%Y')
        date_limit_of_reactu = "31-12-{}".format(year)
        date_limit_of_reactu = datetime.strptime(date_limit_of_reactu, '%d-%m-%Y')
        date_now = datetime.now()

        total_number_of_training = 0
        total_number_of_training_done = 0
        total_number_of_training_remaining = 0
        total_number_of_training_not_followed = 0
        total_number_of_update = 0
        total_number_of_update_metier = 0
        total_number_of_update_done = 0
        retour_info = []
        codes_modules_seuil = []

        info = bdd.execute("SELECT * FROM Effectifs WHERE Employee_ID='{}'".format(personne))
        retour_info.append(info.fetchall())

        for elem in retour_info:
            for test in elem:
                id_manager = round(test[48])
                mail = bdd.execute("SELECT * FROM Effectifs WHERE Employee_ID='{}'".format(id_manager))
                mail = mail.fetchall()
                for elem in mail:
                    mail_manager=elem[6]
                    break
            break
            
            


        

        Wf_training, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True'".format(personne))
        retour_info.append(Wf_training[0])
        
        Wf_training_ok, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' AND Date_fait<>''".format(personne))
        retour_info.append(Wf_training_ok[0])
        
        Wf_training_remaining = Wf_training[0] - Wf_training_ok[0]
        retour_info.append(Wf_training_remaining)
        
        Wf_training_HS, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='False' AND Date_fait<>''".format(personne))
        retour_info.append(Wf_training_HS[0])
        
        number_of_update, = bdd.execute("SELECT COUNT(Codes_modules) FROM S_{} WHERE Categories='Metiers' AND Suivi_categories='True'".format(personne))
        retour_info.append(number_of_update[0])

        recup_date = bdd.execute("SELECT Date_fin, Codes_modules, Intitules_codes_modules, Rappel_mail, Date_rappel FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' AND Categories='Metiers' AND Date_fin<>''".format(personne))

        for elem in recup_date:
            
            if elem[0] != '?':
                ladate = datetime.strptime(elem[0], '%d-%m-%Y')
                if ladate > date_of_reactu and ladate <= date_limit_of_reactu:
                    total_number_of_update +=1

                    seuil_alerte_90j = ladate - timedelta(days=90)
                    seuil1 = datetime.strftime(seuil_alerte_90j, "%d/%m/%Y")
                    
                    seuil_alerte_30j = ladate - timedelta(days=30)
                    seuil2 = datetime.strftime(seuil_alerte_30j, "%d/%m/%Y")

                    jour = ladate - datetime.now()
                    
                    if elem[3] == 'False':
                        if date_now > seuil_alerte_90j:
                            codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, "📧", "Non", ""))
                        else:
                            codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, "", "", ""))
                    elif elem[3] == 'True':
                        if date_now > seuil_alerte_90j:
                            codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, "📧", "Oui", elem[4]))
                        else:
                            codes_modules_seuil.append((elem[1], elem[2], elem[0], jour.days, "", "Oui", elem[4]))



        retour_info.append(total_number_of_update)
        
        
        recup_date = bdd.execute("SELECT Date_fait FROM S_{} WHERE Suivi_module='True' AND Categories='Metiers' AND Date_fait<>''".format(personne))
        for elem in recup_date:
            if elem[0] != '':
                ladate = datetime.strptime(elem[0], '%d-%m-%Y')
                if ladate > date_of_reactu and ladate < date_limit_of_reactu:
                    print(ladate)
                    total_number_of_update_done +=1

        retour_info.append(total_number_of_update_done)

        retour_info.append(codes_modules_seuil)

        list_categories = bdd.execute("SELECT DISTINCT Categories FROM S_{} GROUP BY Categories".format(personne))

        if total_number_of_update != 0:
            rate_respect = round(((total_number_of_update_done / number_of_update[0]) * 100) , 1)
            print(rate_respect)
        else:
            rate_respect = 0
        retour_info.append(rate_respect)

        retour_info.append(mail_manager)

        retour_info.append(list_categories.fetchall())
        
        return retour_info
    def bilan_cat_personne(chorus, categorie):
        requette = bdd.execute("SELECT Codes_modules, Intitules_codes_modules, Suivi_module, Date_fait, Date_fin FROM S_{} WHERE Categories='{}'".format(chorus, categorie))
        return requette.fetchall()


    def Synth_charts():
        list_cats = []
        list_done = []
        list_temp = []

        compt = 0


        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        for elements in requette:
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                number_of_training_by_cat = bdd.execute("SELECT Categories, COUNT(Codes_modules) FROM S_{} WHERE Suivi_module='True' GROUP BY Categories".format(ID_Employee))
                number_of_training_by_cat_done = bdd.execute("SELECT Categories, COUNT(Codes_modules) FROM S_{} WHERE Suivi_module='True' AND Date_fait<>'' GROUP BY Categories".format(ID_Employee))
                
                temp = number_of_training_by_cat.fetchall()
                temp2 = number_of_training_by_cat_done.fetchall()

                for elem in temp:
                    if elem[0] in list_cats:
                        pass
                    else:
                        list_cats.append((elem[0], elem[1]))
                
                for elem in temp2:
                    if elem[0] in list_cats:
                        pass
                    else:
                        list_done.append((elem[0], elem[1]))

                # Comptage
        list_cats.sort()
        list_done.sort()

        for elem in list_cats:
            temp = elem[0]
            break
        for elem in list_cats:
            if temp == elem[0]:
                compt = compt + elem[1]
            else:
                list_temp.append((temp, compt))
                temp = elem[0]
                compt = 0
        
        list_cats=list_temp

        list_temp =[]
        compt = 0
        for elem in list_done:
            temp = elem[0]
            break
        for elem in list_done:
            if temp == elem[0]:
                compt = compt + elem[1]
            else:
                list_temp.append((temp, compt))
                temp = elem[0]
                compt = 0

        list_done=list_temp
        

        

 

        return list_cats, list_done

    def Synth_charts_manager(manager):
        list_cats = []
        list_done = []
        list_temp = []

        compt = 0


        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        for elements in requette:
            table = elements[0]
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                requet = bdd.execute("SELECT Manager_name FROM Effectifs WHERE Employee_ID='{}'".format(ID_Employee))
                temp = requet.fetchone()
                try:
                    if temp[0] == manager:
                        number_of_training_by_cat = bdd.execute("SELECT Categories, COUNT(Codes_modules) FROM S_{} WHERE Suivi_module='True' GROUP BY Categories".format(ID_Employee))
                        number_of_training_by_cat_done = bdd.execute("SELECT Categories, COUNT(Codes_modules) FROM S_{} WHERE Suivi_module='True' AND Date_fait<>'' GROUP BY Categories".format(ID_Employee))
                        
                        temp = number_of_training_by_cat.fetchall()
                        temp2 = number_of_training_by_cat_done.fetchall()

                        for elem in temp:
                            if elem[0] in list_cats:
                                pass
                            else:
                                list_cats.append((elem[0], elem[1]))
                        
                        for elem in temp2:
                            if elem[0] in list_cats:
                                pass
                            else:
                                list_done.append((elem[0], elem[1]))
                except:
                    pass
                # Comptage
        list_cats.sort()
        list_done.sort()

        for elem in list_cats:
            temp = elem[0]
            break
        for elem in list_cats:
            if temp == elem[0]:
                compt = compt + elem[1]
            else:
                list_temp.append((temp, compt))
                temp = elem[0]
                compt = 0
        
        list_cats=list_temp

        list_temp =[]
        compt = 0
        for elem in list_done:
            temp = elem[0]
            break
        for elem in list_done:
            if temp == elem[0]:
                compt = compt + elem[1]
            else:
                list_temp.append((temp, compt))
                temp = elem[0]
                compt = 0

        list_done=list_temp
        

        

 

        return list_cats, list_done

    def Synth_chart_workflow(personne):
        list_objectif = []
        list_done = []

        number_of_training_by_cat = bdd.execute("SELECT Categories, COUNT(Codes_modules) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' GROUP BY Categories".format(personne))
        number_of_training_by_cat_done = bdd.execute("SELECT Categories, COUNT(Codes_modules) FROM S_{} WHERE Suivi_categories='True' AND Date_fait<>'' GROUP BY Categories".format(personne))
                        
        list_objectif = number_of_training_by_cat.fetchall()
        list_done = number_of_training_by_cat_done.fetchall()


        return list_objectif, list_done



    def recherche_personne_hors_suivi(manager, categories, code):
        list_personnes = []
        list_personnes_hors_suivi = []
        test = bdd.execute("SELECT Employee_ID, Worker FROM Effectifs WHERE Manager_name='{}'".format(manager))
        list_personnes = test.fetchall()

        for elem in list_personnes:
            try:
                requet = bdd_cursor.execute("SELECT Suivi_categories FROM S_{} WHERE Date_fait<>'' AND Categories='{}' AND Codes_modules='{}'".format(elem[0], categories, code))
                temp = requet.fetchone()
                if temp[0] == 'True':
                    list_personnes_hors_suivi.append((elem[1], elem[0]))

            except:
                pass
        print(list_personnes_hors_suivi)
        return list_personnes_hors_suivi
    #recherche_personne_hors_suivi("Floriand Filari", "Digital")

class Workflow():
    def Workflow_choice(personne):
        cat = []
        values = []
        Id, = bdd.execute("SELECT Employee_ID FROM Effectifs WHERE Worker='{}'".format(personne))
        if Id:
            Wf_training, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='True'".format(Id[0]))
            Wf_training_ok, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='True' AND Date_fait<>''".format(Id[0]))
            Wf_training_HS, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='False' AND Date_fait<>''".format(Id[0]))
            list_categories = bdd.execute("SELECT Categories, COUNT(Categories) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' AND Date_fait<>'' GROUP BY Categories".format(Id[0]))
            Manager = bdd.execute("SELECT Manager FROM S_{}".format(Id[0]))
            
        for elem in list_categories:
            cat.append(elem[0])
            values.append(elem[1])
        return Wf_training, Wf_training_ok, Wf_training_HS, cat, values, Manager
    #Workflow_choice("Benoit Ghirardini")

    def Workflow_manager(manageur):
        list_Id = []

        Wf_training_count = 0
        Wf_training_ok_count = 0
        Wf_training_HS_count = 0
        list_Id = bdd.execute("SELECT Employee_ID, Worker_name FROM Effectifs WHERE Manager_name='{}'".format(manageur))
        for Id in list_Id:
            try:
                Wf_training, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='True'".format(Id[0]))
                Wf_training_ok, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='True' AND Date_fait<>''".format(Id[0]))
                Wf_training_HS, = bdd.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_module='False' AND Date_fait<>''".format(Id[0]))
                Wf_training_count = Wf_training_count + Wf_training[0]
                Wf_training_ok_count = Wf_training_ok_count + Wf_training_ok[0]
                Wf_training_HS_count = Wf_training_HS_count + Wf_training_HS[0]


            except:
                pass

        return Wf_training_count, Wf_training_ok_count, Wf_training_HS_count

    def top_5(manager):
        list_top_5 = []

        Id_N1 = bdd.execute("SELECT Manager_Employee_ID FROM Effectifs WHERE Manager_name='{}'".format(manager))
        Id_N1 = Id_N1.fetchone()

        for elem in Id_N1:
            Id_Manager = int(elem)

        try:
            test, = bdd_cursor.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' AND Date_Fait<>''".format(str(Id_Manager)))
            list_top_5.append((manager, test[0]))
        
        except:
            pass
        
        list_personnes = bdd.execute("SELECT Employee_ID, Worker FROM Effectifs WHERE Manager_name='{}'".format(manager))

        for elements in list_personnes:
            ID_Employee = elements[0]

            try:

                test, = bdd_cursor.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' AND Date_Fait<>''".format(ID_Employee))
                list_top_5.append((elements[1], test[0]))
            except:
                pass
        sorted_listed = sorted(list_top_5, key=lambda item:(item[1]), reverse=True)


        return sorted_listed



    def top_5_atelier():
        list_top_5 = []

        requette = bdd_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        requette = requette.fetchall()
        for elem in requette:
            table = elem[0]
            print(table)
            if "S_" in table:
                ID_Employee = str(table).replace("S_", "") # Récupère l'id chorus de la personne
                test, = bdd_cursor.execute("SELECT COUNT(*) FROM S_{} WHERE Suivi_categories='True' AND Suivi_module='True' AND Date_Fait<>''".format(ID_Employee))
                list_top_5.append((elem[0], test[0]))

        
        sorted_listed = sorted(list_top_5, key=lambda item:(item[1]), reverse=True)
        test_list = []
        for elem in sorted_listed:
            id = str(elem[0]).replace("S_", "") # Récupère l'id chorus de la personne
            try:
                worker, = bdd.execute("SELECT Worker FROM Effectifs WHERE Employee_ID='{}'".format(id))
                test_list.append((worker[0],elem[1]))
            except:pass

        return test_list

