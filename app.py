# @Project:  Suivi formations
# @Email:  benoit.ghirardini@michelin.com
# @Author: Benoit Ghirardini
# @Date: Août 2022
# @Version: 1.0


from _init import *
from _main import *
from _charts import *
from _edit_sql import *
from verify_files import *
from _mail import Mailing
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

import streamlit as st  # pip install streamlit
import time


# C:/Python/Python310/python.exe -m streamlit run 'c:/Users/F269167/OneDrive - MFP Michelin/Projets en cours/Suivi formations/Base Python - V1/Codes tests/test dashboard/app1.py'

# Icons Streamlit : https://pastebin.com/raw/w0z7d5Wh
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

nom_db = "Bdd.db"

st.set_page_config(page_title="Suivi formations",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state='collapsed')




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .font {
font-size:18px ; font-family: 'MS Sans Serif'; color: #0078d7;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

hide_table_row_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    font {font-size:5px}
    </style>
    """

cellsytle_jscode = JsCode("""
function(params) {
    if (params.value > 90) {
        return {
            'color': 'white',
            'backgroundColor': 'green'
        }
    } 
    if (params.value > 30 & params.value < 90) {
        return {
            'color': 'black',
            'backgroundColor': 'yellow'
        }
    }    
    
    if (params.value > 0 & params.value < 30) {
        return {
            'color': 'black',
            'backgroundColor': 'orange'
        }
    } 

    if (params.value <= 0) {
        return {
            'color': 'black',
            'backgroundColor': 'red'
        }
    }      
    
    else {
        return {
            'color': 'white',
            
        }
    }
};
""")


classement_jscode = JsCode("""
function(params) {
    if (params.value >0 & params.value <2) {
        return {
            'color': 'black',
            'backgroundColor': '#FFD700'
        }
    } 
    if (params.value >1 & params.value <3) {
        return {
            'color': 'black',
            'backgroundColor': '#C0C0C0'
        }
    }    
    
    if (params.value >2 & params.value <4) {
        return {
            'color': 'black',
            'backgroundColor': '#CD7F32'
        }
    } 

};
""")
# ---------------------------------------------------

class main(): # -- Application du header
    ## -- Fonction global du Header
    def test(df):
        gd = GridOptionsBuilder.from_dataframe(df)

    def header_workflow(self):
        left_header_column, left_midle_header_column, right_midle_header_column, right_header_column = st.columns(4)# -- Définition des colonnes sur le header
        self.list_workflow = Init.list_personnes() # -- Récupération des personnes suivies
        temp = []

        for elem in self.list_workflow[2]:
                temp.append("{} | {}".format(elem[0], elem[1]))
        
        option = temp
    
        if self.choix_visu == 'Par personne':
            with left_header_column:
                self.workflow_selected = st.selectbox("Choix par personne", options=option)
                


            main.subheader_workflow(self)
    
    def subheader_workflow(self):
        left_column, left_midle_column, right_midle_column, right_column = st.columns(4)# -- Définition des colonnes sous l'entête du site
        title = str(self.workflow_selected).split()
        if title[2] == "|":
            self.header_title.title("{} {}".format(title[0], title[1]))
            self.chorus = title[3]
            self.info = synthese.Synth_personne(title[3])
            self.chart_workflow = synthese.Synth_chart_workflow(title[3])
            self.personne = "{} {}".format(title[0], title[1])
        elif title[3] == "|":
            self.header_title.title("{} {} {}".format(title[0], title[1], title[2]))
            self.chorus = title[4]
            self.info = synthese.Synth_personne(title[4])
            self.chart_workflow = synthese.Synth_chart_workflow(title[4])
            self.personne = "{} {} {}".format(title[0], title[1], title[2])
        elif title[4] == "|":
            self.header_title.title("{} {} {} {}".format(title[0], title[1], title[2], title[3]))
            self.chorus = title[5]
            self.info = synthese.Synth_personne(title[5])
            self.chart_workflow = synthese.Synth_chart_workflow(title[5])
            self.personne = "{} {} {} {}".format(title[0], title[1], title[2], title[3])
        elif title[5] == "|":
            self.header_title.title("{} {} {} {} {}".format(title[0], title[1], title[2], title[3], title[4]))
            self.chorus = title[6]
            self.info = synthese.Synth_personne(title[6])
            self.chart_workflow = synthese.Synth_chart_workflow(title[6])
            self.personne = "{} {} {} {} {}".format(title[0], title[1], title[2], title[3], title[4])

        Afaire = []
        fait = []
        for elem in self.chart_workflow[0]:
            Afaire.append(elem)
        for elem in self.chart_workflow[1]:
            fait.append(elem)
        if len(Afaire) > 3:
            self.chart_bars = charts._charts_bars(Afaire, fait)
            #chart_radar = charts._chart_radar(Afaire, fait)        
        else:
            self.chart_bars = charts._charts_bars(Afaire, fait)


        for elem in self.info[0]:
            Michelin_ID = elem[5]
            Mail = elem[6]
            Manager = elem[49]

        with left_column:
            st.subheader("🔎 Info")
            st.markdown('<p class="font">Id Michelin : {}</p>'.format(Michelin_ID), unsafe_allow_html=True)
            st.markdown('<p class="font">Chorus : {}</p>'.format(self.chorus), unsafe_allow_html=True)
            st.markdown('<p class="font">Mail : {}</p>'.format(Mail), unsafe_allow_html=True)
            st.markdown('<p class="font">Manageur : {}</p>'.format(Manager), unsafe_allow_html=True)
            st.markdown('<p class="font">Mail manageur : {}</p>'.format(self.info[10]), unsafe_allow_html=True)


        with left_midle_column:
            st.subheader("📋 Bilan formations")
            st.markdown('<p class="font">Formations à faire : {}</p>'.format(self.info[1]), unsafe_allow_html=True)
            st.markdown('<p class="font">Formations effectuées : {}</p>'.format(self.info[2]), unsafe_allow_html=True)
            st.markdown('<p class="font">Formations restantes : {}</p>'.format(self.info[3]), unsafe_allow_html=True)
            st.markdown('<p class="font">Formations effectuées hors suivi : {}</p>'.format(self.info[4]), unsafe_allow_html=True)

        with right_midle_column:
            if self.info[6] != 0:
                st.subheader("Réactualisation metier à faire pour l'année {}".format(datetime.now().year))
                st.markdown('<p class="font">Réactualisations à faire : {}</p>'.format(self.info[5]), unsafe_allow_html=True)
                st.markdown('<p class="font">Réactualisations effectuées : {}</p>'.format(self.info[7]), unsafe_allow_html=True)
                st.markdown('<p class="font">Taux de respect : {}%</p>'.format(self.info[9]), unsafe_allow_html=True)
            
        if self.info[8]:
            st.subheader("🔔 Réactualisation à venir :")
            df = pd.DataFrame(self.info[8], columns=["Codes modules","Intitulés", "Date limite", "Jours restant", "Mailing", "Rappel fait", "Date du rappel"])
            
            #df = df.set_index("Codes modules")

            with st.expander("Ouvrir/Fermer la visualisation des alertes"):


                
            # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                gb = GridOptionsBuilder.from_dataframe(df)
                gb.configure_column('Jours restant', cellStyle=cellsytle_jscode)
                gb.configure_column("Mailing", headerCheckboxSelection = True, checkboxSelection=True)
                gb.configure_selection(selection_mode='multiple')

                grid_options = gb.build()
                grid_response = AgGrid(df,
                    theme="streamlit",
                    gridOptions=grid_options,
                    allow_unsafe_jscode=True,
                    fit_columns_on_grid_load=True,
                    reload_data=False,
                    try_to_convert_back_to_original_types=False,
                    height=400
                    )
                df = grid_response['data']
                selected = grid_response['selected_rows']
                selected_df = pd.DataFrame(selected)

                if not selected_df.empty :
                    if st.button("Envoyer le rappel"):
                        mail_object = selected_df.loc[:,['Codes modules','Intitulés','Date limite', 'Jours restant']]

                        #st.write(selected_df.loc[:,['Codes modules','Intitulés','Date limite', 'Jours restant']])
                        Mailing.send_mail(Mail, self.info[10], mail_object, self.personne, Manager)
                        
                        for elem in mail_object['Codes modules']:
                            update_rappel = edit.update_rappel(self.chorus, elem)
                        
                        sleep(2)
                        st.experimental_rerun()
                    
                    

                    #if rappel.values:
                        #st.write(rappel.values)

        
        with right_column:
            st.altair_chart(self.chart_bars, use_container_width=True)
        
        main.details_workflow(self)
    
    def details_workflow(self):
        workflow_selected = str(self.workflow_selected).split()
        st.subheader("📑 Détails de {} {}".format(workflow_selected[0], workflow_selected[1]))

        with st.expander("Afficher/Cacher détails de {} {}".format(workflow_selected[0], workflow_selected[1])):
            name = workflow_selected[0] + " " + workflow_selected[1]

            column1, column2, column3 = st.columns([1,1,3]) # -- Définition des colonnes sous l'entête du header (le header contient le titre, la selection manager, et les infos relatives au manager)
            # -- Colonne 1
            categories =[]
            for cat in self.info[11]:categories.append(cat[0])

            with column1:
                st.subheader("Catégories") # -- Titre de la colonne
                
                try: # -- Test principal
                    # -- Chargement des catégories modules
                    self.categories = st.selectbox("",
                    options=categories,
                    )
            
                    
                    st.text("")
                    st.text("")
                    
                    list_codes = [] # -- Prépare la liste pour les codes modules
                    
                    # -- Test si présence catégories
                    try:
                        # -- Si présence catégories, on lance la condition
                        if self.categories:
                            codes = synthese.Synth_codes_workflow(self.chorus, self.categories) # -- Récupère les codes modules suivant la catégories choisie
                            # -- Pour chaque code dans la liste de codes
                            for elem in codes:
                                test = "{} | {}".format(elem[0], elem[1]) # -- Prépare le code en ajoutant le code et sa déscription
                                list_codes.append(test) # -- Ajoute le code dans la liste
                            
                            # -- Si des codes sont présents, on lance la condition
                            if codes:
                                st.subheader("Codes modules")
                                self.code = st.selectbox("",
                                options=list_codes,
                                )
                    except: # -- Si erreur le test présence catégories, on passe
                        pass
                            
                except: # -- Si erreur sur le test principal, on passe
                    pass


            # -- Colonne 2        
            with column2:
                self.active_value = edit.verif_cat_personne(self.chorus, self.categories)
                #st.write("Effectifs : {} | Suivie par : {} personne(s)".format(effectifs, self.active_value))

                label1 = "La catégorie {} est actuellement :".format(self.categories)
                label2 = "Modifier le suivi de la catégorie {}".format(self.categories)
                if "False" in self.active_value[0]:
                    bt_radio_cat = st.radio(label1, {"Suivie", "Non suivie"}, index=0, disabled=True, horizontal=True)
                elif "True" in self.active_value[0]:
                    bt_radio_cat = st.radio(label1, {"Suivie", "Non suivie"}, index=1, disabled=True, horizontal=True)



                selection_cat = st.radio(label2, ("Suivi", "Non Suivi"), key="follow", horizontal=True)
                valider_cat = st.button("Valider", key="Valid_modif_cat")


                if valider_cat:
                    if selection_cat == "Suivi":
                        if bt_radio_cat != "Suivie":
                            requette_cat = edit.active_categorie_personne(self.chorus, self.categories)
                            if "Success" in requette_cat:
                                st.success("La mise à jour de la catégorie {} à bien été effectuée pour {}.".format(self.categories, name))
                                time.sleep(2)
                            else:
                                st.error("Erreur lors de la mise à jour de la catégorie {}. Erreur renvoyée : {}".format(self.categories, requette_cat))
                                time.sleep(2)
                        else:
                            st.info("La catégorie {} est déja {} , aucune modification ne sera effectuée.".format(self.categories, bt_radio_cat))
                            time.sleep(2)

                    elif selection_cat == "Non Suivi":
                        if bt_radio_cat != "Non suivie":
                            requette_cat = edit.desactive_categorie_personne(self.chorus, self.categories)
                            if "Success" in requette_cat:
                                st.success("La mise à jour de la catégorie {} à bien été effectuée pour {}.".format(self.categories, name))
                                time.sleep(2)

                            else:
                                st.error("Erreur lors de la mise à jour de la catégorie {}. Erreur renvoyée : {}".format(self.categories, requette_cat))
                                time.sleep(2)
                        else:
                            st.info("La catégorie {} est déja {} , aucune modification ne sera effectuée.".format(self.categories, bt_radio_cat))
                            time.sleep(2)
                    st.session_state["success"] = True

                try:
                    if self.code:
                        code = self.code[slice(6)]
                        active_code = edit.verif_module_personne(self.chorus, code)

                        label1_module = "Le module {} est actuellement :".format(self.code)
                        label2_module = "Modifier le suivi du module {}".format(code)
                        if "False" in active_code[0]:
                            bt_radio_module = st.radio(label1_module, {"Suivi", "Non suivi"}, index=1, disabled=True, horizontal=True)
                        elif "True" in active_code[0]:
                            bt_radio_module = st.radio(label1_module, {"Suivi", "Non suivi"}, index=0, disabled=True, horizontal=True)

                    selection_module = st.radio(label2_module, ("Suivi", "Non suivi"), horizontal=True)
                    valider_module = st.button("Valider", key="Valid_modif_module")

                    if valider_module:
                        if selection_module == "Suivi":
                            if bt_radio_module != "Suivi":
                                requette_module = edit.active_module_personne(self.chorus, code)
                                
                                if "Success" in requette_module:
                                    st.success("La mise à jour du module {} à bien été effectuée pour {}.".format(code, name))
                                    time.sleep(2)                           
                                else:
                                    st.error("Erreur lors de la mise à jour du module {}. Erreur renvoyée : {}".format(code, requette_module))
                                    time.sleep(2)
                            else:
                                st.info("Le module {} est déja {} , aucune modification ne sera effectuée.".format(code, bt_radio_module))
                                time.sleep(2)                           

                        elif selection_module == "Non suivi":
                            if bt_radio_module != "Non suivi":
                                requette_module = edit.desactive_module_personne(self.chorus, code)
                                if len(list_codes) == 1 :
                                    edit.desactive_categorie_personne(self.chorus, self.categories)
                                if "Success" in requette_module:
                                    st.success("La mise à jour du module {} à bien été effectuée pour {}.".format(code, name))
                                    time.sleep(2)

                                else:
                                    st.error("Erreur lors de la mise à jour du module {}. Erreur renvoyée : {}".format(code, requette_module))
                                    time.sleep(2)
                            else:
                                st.info("Le module {} est déja {} , aucune modification ne sera effectuée.".format(code, bt_radio_module))
                                time.sleep(2)                            

                        st.session_state["success"] = True
                except:
                    pass

            # -- Colonne 3
            with column3:
                if "True" in self.active_value[0]:
                    bilan_cat = synthese.bilan_cat_personne(self.chorus, self.categories)
                    df = pd.DataFrame(bilan_cat, columns=["Codes modules", "Intitulés codes modules", "Suivi", "Terminé le", "Date de validité"])
                    df = df.replace({'Suivi': 'True'}, {'Suivi': 'Oui'}, regex=True)
                    df = df.replace({'Suivi': 'False'}, {'Suivi': 'Non'}, regex=True)
                  


                    gb = GridOptionsBuilder.from_dataframe(df)
                    gb.configure_column('Terminé le', editable=True)
                    gb.configure_selection(selection_mode='single')
                    grid_options = gb.build()


                    response = AgGrid(
                        df,
                        theme="streamlit",
                        key='table1',
                        gridOptions=grid_options,
                        allow_unsafe_jscode=True,
                        fit_columns_on_grid_load=True,
                        reload_data=False,
                        height=400
                        )
                    
                    df1 = pd.DataFrame(response['data'])
                    test = df.compare(df1, keep_shape=True, keep_equal=True)

                    df = response['data']
                    selected = response['selected_rows']
                    selected_df = pd.DataFrame(selected)
                    
                    if selected:
                        for elem in test.values:
                            if "/" in elem[7]: #Vérifie le format date, le format doit obligatoirement etre du style jj-mm-yyyy
                                test = str(elem[7]).replace("/", "-")
                                elem[7] = test

                            if len(elem[7]) == 10:    
                                if elem[6] != elem[7]:
                                    st.session_state["success"] = True
                                    success = st.info(f"La date pour le code {elem[0]}, va être modifiée, veuillez patienter.")
                                    test = edit.update_date(self.chorus, elem[7], elem[0])
                            
                            elif len(elem[7]) != 10 and elem[7] !='': st.warning("Le format date ne correspond pas. Merci de respecter le format suivant : jj-mm-aaaa")


                if "success" in st.session_state:
                    if st.session_state["success"] == True:
                        st.session_state["success"] ='false'
                        st.experimental_rerun()


    def header_synthese(self):
        left_header_column, left_midle_header_column, right_midle_header_column, right_header_column = st.columns(4)# -- Définition des colonnes sur le header
        # -- Colonne gauche du header (entête de site)
        if self.choix_visu == "Par équipe":
            with left_header_column:
                
                    self.manager_selected = self.manager_choice("Choix par manageurs", options=self.list_workflow[1])
                    if self.manager_selected != "Synthèse atelier":
                        self.header_title.title("Equipe de {}".format(self.manager_selected))
                        self.top5 = Workflow.top_5(self.manager_selected)
                        recap_N1 = synthese.Synth_manager(self.manager_selected)
                        self.formations_a_faire_N1 = recap_N1[0]
                        self.formations_faites_N1 = recap_N1[1]
                        self.formations_restantes_N1 = recap_N1[2]
                        self.formations_hors_suivi_N1 = recap_N1[3]
                        self.reactualisations_N1 = recap_N1[4]
                        self.taux_respet_reactu_N1 = recap_N1[5]
                        self.nb_effectif_N1 = recap_N1[6]
                        self.categories_N1 = recap_N1[7]
                        self.effectif_N1 = recap_N1[8]
                        self.modules_N1 = recap_N1[9]
                        self.reactu_alerte_N1 = recap_N1[10]

                        self.chart_manager = synthese.Synth_charts_manager(self.manager_selected)

                        Afaire = []
                        fait = []
                        for elem in self.chart_manager[0]:
                            Afaire.append(elem)
                        for elem in self.chart_manager[1]:
                            fait.append(elem)
                        if len(Afaire) > 3:
                            self.chart_bars = charts._charts_bars(Afaire, fait)
                            #chart_radar = charts._chart_radar(Afaire, fait)        
                        else:
                            self.chart_bars = charts._charts_bars(Afaire, fait)
                    else:
                        self.header_title.title("Synthèse atelier")
                        self.top5 = Workflow.top_5_atelier()
                        self.chart_synthese = synthese.Synth_charts()

                        Afaire = []
                        fait = []
                        for elem in self.chart_synthese[0]:
                            Afaire.append(elem)
                        for elem in self.chart_synthese[1]:
                            fait.append(elem)
                            
                        self.chart_bars = charts._charts_bars(Afaire, fait)


            with left_midle_header_column:
                pass                


            with right_midle_header_column:
                pass

            with right_header_column:
                pass
          
            main.subheader_synthese(self)
        elif self.choix_visu == 'Par personne': main.header_workflow(self)


    def subheader_synthese(self):

        left_column, left_midle_column, right_midle_column, right_column = st.columns(4)# -- Définition des colonnes sous l'entête du site
            # -- Colonne de gauche subheader
        if self.choix_visu == "Par équipe":
            with left_column:
                
                
                if self.manager_selected == "Synthèse atelier":
                    st.subheader("🔎 Récapitulatif atelier")
                    st.text("Formations à faire : {}".format(self.formations_a_faire))
                    st.text("Formations effectuées : {}".format(self.formations_faites))
                    st.text("Formations restantes : {}".format(self.formations_restantes))
                    st.text("Formations effectuées en hors suivi : {}".format(self.formations_hors_suivi))               

            
            
            
                elif self.manager_selected != "Synthèse atelier":
                    st.subheader("🔎 Récapitulatif de l'équipe")
                    st.text("Effectif de l'équipe : {}".format(self.nb_effectif_N1))
                    st.text("Formations à faire : {}".format(self.formations_a_faire_N1))
                    st.text("Formations effectuées : {}".format(self.formations_faites_N1))
                    st.text("Formations restantes : {}".format(self.formations_restantes_N1))
                    st.text("Formations effectuées en hors suivi : {}".format(self.formations_hors_suivi_N1))



            # -- Colonne du milieu subheader


            
            if self.manager_selected != "Synthèse atelier" and self.categories_N1:        
                self.details_manager(self.categories_N1, self.manager_selected, self.nb_effectif_N1)

            
            with left_midle_column:
                if self.manager_selected != "Synthèse atelier":
                    if self.reactualisations_N1 != 0:
                        st.subheader("📆 Réactualisation metier pour l'année {}".format(datetime.now().year))
                        st.text("Réactualisation à faire : {}".format(self.reactualisations_N1))
                        st.text("Taux de respect réactualisation : {}%".format(self.taux_respet_reactu_N1))

                    try:
                        if self.reactu_alerte_N1:
                            st.subheader("🔔 Réactualisation à venir :")
                            df = pd.DataFrame(self.reactu_alerte_N1, columns=["Codes modules","Intitulés", "Date limite", "Jours restant", "Rappel"])
                            df = df.set_index("Codes modules")
                            with st.expander("Ouvrir/Fermer la visualisation des alertes"):
                                gb = GridOptionsBuilder.from_dataframe(df)
                                gb.configure_column('Jours restant', cellStyle=cellsytle_jscode)
                                gb.configure_column("Rappel", headerCheckboxSelection = True, checkboxSelection=True)
                                gb.configure_selection(selection_mode='multiple')

                                grid_options = gb.build()
                                grid_response = AgGrid(df,
                                    theme="streamlit",
                                    gridOptions=grid_options,
                                    allow_unsafe_jscode=True,
                                    fit_columns_on_grid_load=True,
                                    reload_data=False,
                                    try_to_convert_back_to_original_types=False,
                                    height=400
                                    )
                                df = grid_response['data']
                                selected = grid_response['selected_rows']
                                selected_df = pd.DataFrame(selected)

                                if not selected_df.empty :
                                    #st.write(selected_df.loc[:,['Codes modules','Intitulés','Date limite', 'Jours restant']])
                                    #rappel = selected_df.loc[:,['Rappel']]
                                    st.info("Lors de la selection un mail sera envoyé à la personne avec en copie son manager avec les infos sur le retard du code module à faire.")
                                    #if rappel.values:
                                        #st.write(rappel.values)

                                        
                    except: pass

                elif self.reactualisations and self.manager_selected == "Synthèse atelier":
                    st.subheader("📆 Réactualisation metier pour l'année {}".format(datetime.now().year))
                    st.text("Réactualisation à faire : {}".format(self.reactualisations))
                    st.text("Taux de respect réactualisation : {}%".format(self.taux_respet_reactu))

                    try:
                        if self.reactu_alerte:
                            st.subheader("🔔 Réactualisation à venir :")
                            df = pd.DataFrame(self.reactu_alerte, columns=["Codes modules","Intitulés", "Date limite", "Jours restant", "Rappel"])
                            #df = df.set_index("Codes modules")
                            with st.expander("Ouvrir/Fermer la visualisation des alertes"):
                                #st.markdown(hide_table_row_index, unsafe_allow_html=True)
                                gb = GridOptionsBuilder.from_dataframe(df)
                                gb.configure_column('Jours restant', cellStyle=cellsytle_jscode)
                                gb.configure_column("Rappel", headerCheckboxSelection = True, checkboxSelection=True)
                                gb.configure_selection(selection_mode='multiple')

                                grid_options = gb.build()
                                grid_response = AgGrid(df,
                                    theme="streamlit",
                                    gridOptions=grid_options,
                                    allow_unsafe_jscode=True,
                                    fit_columns_on_grid_load=True,
                                    reload_data=False,
                                    try_to_convert_back_to_original_types=False,
                                    height=400
                                    )
                                df = grid_response['data']
                                selected = grid_response['selected_rows']
                                selected_df = pd.DataFrame(selected)

                                if not selected_df.empty :
                                    #st.write(selected_df.loc[:,['Codes modules','Intitulés','Date limite', 'Jours restant']])
                                    #rappel = selected_df.loc[:,['Rappel']]
                                    st.info("Lors de la selection un mail sera envoyé à la personne avec en copie son manager avec les infos sur le retard du code module à faire.")
                                    #if rappel.values:
                                        #st.write(rappel.values)

                    except: pass


                
                    #st.subheader("Aucune réactu à faire")
            # -- Colonne de droite subheader      
            with right_midle_column:
                st.subheader("🏆 Classement")
                i = 1
                list_test = []
                for elem in self.top5:
                    list_test.append([i, elem[0], elem[1]])
                    i += 1
                    #if i >5:break
                data_classement = pd.DataFrame(list_test, columns=["Pos:", "Personnes", "Scores"])
                class_gb = GridOptionsBuilder.from_dataframe(data_classement)
                class_gb.configure_column('Pos:', cellStyle=classement_jscode)
                option_class = class_gb.build()
                
                AgGrid(
                    data_classement,
                    theme="balham",
                    gridOptions=option_class,
                    allow_unsafe_jscode=True,
                    fit_columns_on_grid_load=True,
                    reload_data=False,
                    height=200
                    )


            with right_column:
                    try:
                        st.plotly_chart(self.chart_radar, use_container_width=False)
                    except:
                        pass
                        st.altair_chart(self.chart_bars, use_container_width=True)


    

    # -- FIN DU HEADER


    # -- Fonction du siderbar (menu glissant gauche)
    def sidebar(self, list_workflow):
        self.list_workflow = list_workflow # -- Récupération de la liste effectif (vient de la fonction Open)
        self.workflow_selected = st.sidebar.multiselect("", options=list_workflow[0]) # -- Attribution de la liste effectif dans le widget multiselect
        
        self.open_init = st.sidebar.checkbox("Ouvrir menu mise à jour", key="Menu_maj") # -- Création du bouton Ouverture panneau initialisation fichiers
   
        # -- Modification des titres header et sidebar lors de la selection d'un effectif
        if self.workflow_selected:
            self.header_title.title(self.workflow_selected[0])
            self.sidebar_left_title.title(self.workflow_selected[0])
            app.header_workflow()




        # -- Si la clé "Valid" n'est pas dans la session streamlit, alors on effectue la condition    
        if "Valid" not in st.session_state:
            if self.open_init: # -- Si le bouton ouverture menu initialisation est activé on effectue la condition
                self.inf = st.sidebar.info # -- Définition d'une variable information pour affichage 
                files = self.file("Selectionnez un fichier", key="Choix") # -- Ouverture d'une boite de dialogue windows pour la selection d'un fichier en l'attibuant à 'files
                
                # -- Si un fichier est choisi on effectue la condition
                if files:
                    self.inf("Veuillez patienter pendant la lecture du fichier", icon="ℹ️") # -- Affiche un message d'info
                    time.sleep(0.5)
                    self.verif = verify.verify_file(self, files) # -- Lance la procédure de vérification du fichier 
                    
                    if "Erreur" not in self.verif: # -- Si la valeur Erreur n'est pas dans la session, on effectue la condition
                        self.inf("Fichier csv créé, vous pouvez commencer la mise à jour en cliquant sur le bouton 'Valider' ", icon="✔️") # -- Affiche le message d'info
                        st.sidebar.button("Valider", key="Valid") # -- Affichage du bouton valider            
                        st.session_state["verif"] = self.verif[0] # -- récupère l'état de la verif dans la session
                        st.session_state["Table"] = self.verif[1] # -- Récupère la table à modifier dans la session

                    else:
                        if "Choix" in st.session_state:
                            del st.session_state["Choix"]
                            time.sleep(0.5)
                            st.experimental_rerun()
                            
        else:
            main.update_sql() # -- Effectue la mise à jour de la base de données
    
    # -- Fonction détails manager
    def details_manager(self, categories, manager, effectifs):
        if st.session_state["Workflow"] == False:
            st.subheader("📑 Détails de {}".format(self.manager_selected))
            with st.expander("Afficher/Cacher détails équipe de {}".format(self.manager_selected)):
                column1, column2, column3, column4, column5, column6 = st.columns(6) # -- Définition des colonnes sous l'entête du header (le header contient le titre, la selection manager, et les infos relatives au manager)
                # -- Colonne 1
                with column1:
                    st.subheader("Catégories") # -- Titre de la colonne
                    
                    try: # -- Test principal
                        # -- Chargement des catégories modules
                        categories = st.selectbox("",
                        options=categories,
                        )
                
                        self.categories = categories
                        
                        st.text("")
                        st.text("")
                        
                        list_codes = [] # -- Prépare la liste pour les codes modules
                        
                        # -- Test si présence catégories
                        try:
                            # -- Si présence catégories, on lance la condition
                            if categories:
                                codes = synthese.Synth_codes_modules(manager, categories) # -- Récupère les codes modules suivant la catégories choisie
                                # -- Pour chaque code dans la liste de codes
                                for elem in codes:
                                    test = "{} | {}".format(elem[0], elem[1]) # -- Prépare le code en ajoutant le code et sa déscription
                                    list_codes.append(test) # -- Ajoute le code dans la liste
                                
                                # -- Si des codes sont présents, on lance la condition
                                if codes:
                                    st.subheader("Codes modules")
                                    self.code = st.selectbox("",
                                    options=list_codes,
                                    )
                        except: # -- Si erreur le test présence catégories, on passe
                            pass
                                
                    except: # -- Si erreur sur le test principal, on passe
                        pass


                # -- Colonne 2        
                with column2:
                    self.active_value = edit.active_value(self.categories, self.manager_selected)
                    st.write("Effectifs : {} | Suivie par : {} personne(s)".format(effectifs, self.active_value))
                    
                    label1 = "La catégorie {} est actuellement :".format(self.categories)
                    label2 = "Modifier le suivi de la catégorie {}".format(self.categories)
                    if self.active_value == 0:
                        bt_radio_cat = st.radio(label1, {"Suivie", "Non suivie"}, index=1, disabled=True, horizontal=True)
                    elif self.active_value == effectifs:
                        bt_radio_cat = st.radio(label1, {"Suivie", "Non suivie"}, index=0, disabled=True, horizontal=True)
                    elif self.active_value != effectifs:
                        bt_radio_cat = st.radio(label1, {"Suivie", "Non suivie"}, index=0, disabled=True, horizontal=True)
                        st.info("Cette catégorie n'est pas suivie par l'ensemble de l'équipe", icon="⚠️")


                    selection_cat = st.radio(label2, ("Suivi", "Non Suivi"), key="follow", horizontal=True)
                    valider_cat = st.button("Valider", key="Valid_modif_cat")


                    if valider_cat:
                        if selection_cat == "Suivi":
                            if bt_radio_cat != "Suivie":
                                requette_cat = edit.active_categorie_manager(self.categories, self.manager_selected)
                                if "Success" in requette_cat:
                                    st.success("La mise à jour de la catégorie {} à bien été effectuée pour le manageur {}.".format(self.categories, self.manager_selected))
                                    time.sleep(2)
                                else:
                                    st.error("Erreur lors de la mise à jour de la catégorie {}. Erreur renvoyée : {}".format(self.categories, requette_cat))
                                    time.sleep(2)
                            else:
                                st.info("La catégorie {} est déja {} , aucune modification ne sera effectuée.".format(self.categories, bt_radio_cat))
                                time.sleep(2)

                        elif selection_cat == "Non Suivi":
                            if bt_radio_cat != "Non suivie":
                                requette_cat = edit.desactive_categorie_manager(self.categories, self.manager_selected)
                                if "Success" in requette_cat:
                                    st.success("La mise à jour de la catégorie {} à bien été effectuée pour le manageur {}.".format(self.categories, self.manager_selected))
                                    time.sleep(2)

                                else:
                                    st.error("Erreur lors de la mise à jour de la catégorie {}. Erreur renvoyée : {}".format(self.categories, requette_cat))
                                    time.sleep(2)
                            else:
                                st.info("La catégorie {} est déja {} , aucune modification ne sera effectuée.".format(self.categories, bt_radio_cat))
                                time.sleep(2)
                        st.session_state["success"] = True

                    try:
                        if self.code:
                            code = self.code[slice(6)]
                            active_code = edit.active_module(code, self.manager_selected)

                            label1_module = "Le module {} est actuellement :".format(self.code)
                            label2_module = "Modifier le suivi du module {}".format(code)
                            if active_code[0] == 'False':
                                bt_radio_module = st.radio(label1_module, {"Suivi", "Non suivi"}, index=0, disabled=True, horizontal=True)
                            elif active_code[0] == 'True':
                                bt_radio_module = st.radio(label1_module, {"Suivi", "Non suivi"}, index=1, disabled=True, horizontal=True)

                        selection_module = st.radio(label2_module, ("Suivi", "Non suivi"), horizontal=True)
                        valider_module = st.button("Valider", key="Valid_modif_module")

                        if valider_module:
                            if selection_module == "Suivi":
                                if bt_radio_module != "Suivi":
                                    requette_module = edit.active_module_manager(code, self.manager_selected)
                                    if "Success" in requette_module:
                                        st.success("La mise à jour du module {} à bien été effectuée sur l'effectif de {}.".format(code, self.manager_selected))
                                        time.sleep(2)                           
                                    else:
                                        st.error("Erreur lors de la mise à jour du module {}. Erreur renvoyée : {}".format(code, requette_module))
                                        time.sleep(2)
                                else:
                                    st.info("Le module {} est déja {} , aucune modification ne sera effectuée.".format(code, bt_radio_module))
                                    time.sleep(2)                           

                            elif selection_module == "Non suivi":
                                if bt_radio_module != "Non suivi":
                                    requette_module = edit.desactive_module_manager(code, self.manager_selected)
                                    if "Success" in requette_module:
                                        st.success("La mise à jour du module {} à bien été effectuée sur l'effectif de {}.".format(code, self.manager_selected))
                                        time.sleep(2)

                                    else:
                                        st.error("Erreur lors de la mise à jour du module {}. Erreur renvoyée : {}".format(code, requette_module))
                                        time.sleep(2)
                                else:
                                    st.info("Le module {} est déja {} , aucune modification ne sera effectuée.".format(code, bt_radio_module))
                                    time.sleep(2)                            

                            st.session_state["success"] = True
                    except:
                        pass

                # -- Colonne 3
                with column3:
                    try:
                        if self.active_value == effectifs:
                            list_temp = []
                            st.subheader("Effectif de {}".format(self.manager_selected))
                            for elem in self.effectif_N1:
                                list_temp.append(("{} | {}").format(elem[1], elem[0]))
                
                            selection_personne = st.selectbox(self.code, list_temp)
                            if selection_personne:
                                temp = str(selection_personne).split()
                                personne = "{} {}".format(temp[0], temp[1])
                                chorus = temp[3]
                                valeur = edit.verif_module_personne(chorus, code)
                                if valeur[1] == 'True':
                                    bt_radio_categorie_personne = st.radio("Catégorie suivie :", {"Suivie", "Non suivie"}, key="bt_radio_cat_personne", index=1, disabled=True, horizontal=True)
                                elif valeur[1] == 'False':
                                    bt_radio_categorie_personne = st.radio("Catégorie suivie :", {"Suivie", "Non suivie"}, key="bt_radio_cat_personne", index=0, disabled=True, horizontal=True)

                                selection_categorie_personne = st.radio("Suivi catégorie :", {"Suivi", "Non suivi"}, key="select_categorie", horizontal=True)
                                valide_cat_personne = st.button("Valider", key="Valide_modif_cat_personne")
                                                                
                                if valeur[0] == 'True':
                                    bt_radio_module_personne = st.radio("Module suivi :", {"Suivi", "Non suivi"}, key="bt_radio_personne", index=0, disabled=True, horizontal=True)                    
                                elif valeur[0] == 'False':
                                    bt_radio_module_personne = st.radio("Module suivi :", {"Suivi", "Non suivi"}, key="bt_radio_personne", index=1, disabled=True, horizontal=True) 

                                selection_module_personne = st.radio("Suivi module :", {"Suivi", "Non suivi"}, key="select_module", horizontal=True)
                                valide_module_personne = st.button("Valider", key="Valide_modif_module_personne")

                                if valide_cat_personne:
                                    if selection_categorie_personne == "Suivi":
                                        if bt_radio_categorie_personne != "Suivi":
                                            modif_categorie_personne = edit.active_categorie_personne(chorus, self.categories)
                                            if "Success" in modif_categorie_personne:
                                                st.success("La mise à jour de la catégorie {} à bien été effectuée pour {}.".format(self.categories, personne))
                                                time.sleep(2)                           
                                            else:
                                                st.error("Erreur lors de la mise à jour de la catégorie {}. Erreur renvoyée : {}".format(self.categories, modif_module_personne))
                                                time.sleep(2)
                                        else:
                                            st.info("La catégorie {} est déja 'suivie', aucune modification ne sera effectuée.".format(self.categories))
                                            time.sleep(2)

                                        st.session_state["success"] = True 
                                    
                                    
                                    elif selection_categorie_personne == "Non suivi":
                                        if bt_radio_categorie_personne != "Non suivi":
                                            modif_categorie_personne = edit.desactive_categorie_personne(chorus, self.categories)
                                            if "Success" in modif_categorie_personne:
                                                st.success("La mise à jour de la catégorie module {} à bien été effectuée pour {}.".format(self.categories, personne))
                                                time.sleep(2)                           
                                            else:
                                                st.error("Erreur lors de la mise à jour de la catégorie module {}. Erreur renvoyée : {}".format(self.categories, modif_module_personne))
                                                time.sleep(2)
                                        else:
                                            st.info("La catégorie {} est déja 'non suivie', aucune modification ne sera effectuée.".format(self.categories))
                                            time.sleep(2)

                                        st.session_state["success"] = True 



                                if valide_module_personne:
                                    if selection_module_personne == "Suivi":
                                        if bt_radio_module_personne != "Suivi":
                                            modif_module_personne = edit.active_module_personne(chorus, code)
                                            if "Success" in modif_module_personne:
                                                st.success("La mise à jour du module {} à bien été effectuée pour {}.".format(code, personne))
                                                time.sleep(2)                           
                                            else:
                                                st.error("Erreur lors de la mise à jour du module {}. Erreur renvoyée : {}".format(code, modif_module_personne))
                                                time.sleep(2)
                                        else:
                                            st.info("Le module {} est déja 'suivi', aucune modification ne sera effectuée.".format(code))
                                            time.sleep(2)

                                        st.session_state["success"] = True 
                                    
                                    
                                    elif selection_module_personne == "Non suivi":
                                        if bt_radio_module_personne != "Non suivi":
                                            modif_module_personne = edit.desactive_module_personne(chorus, code)
                                            if "Success" in modif_module_personne:
                                                st.success("La mise à jour du module {} à bien été effectuée pour {}.".format(code, personne))
                                                time.sleep(2)                          
                                            else:
                                                st.error("Erreur lors de la mise à jour du module {}. Erreur renvoyée : {}".format(code, modif_module_personne))
                                                time.sleep(2)
                                        else:
                                            st.info("Le module {} est déja 'non suivi', aucune modification ne sera effectuée.".format(code))
                                            time.sleep(2)
                                            
                                        st.session_state["success"] = True
                        elif self.active_value != effectifs and self.active_value!= 0:
                            list_temp = []
                            st.subheader("Effectif de {}".format(self.manager_selected))
                            self.personne_hors_suivi = synthese.recherche_personne_hors_suivi(self.manager_selected, self.categories, code)
                            
                            for elem in self.personne_hors_suivi:
                                list_temp.append(("{} | {}").format(elem[0], elem[1]))

                            
                            if len(list_temp) == 1:
                                label_selection_personne_hors_suivi = "{} personne suit la catégorie {}".format(len(list_temp),self.categories)
                            elif len(list_temp) > 1:
                                label_selection_personne_hors_suivi = "{} personnes suivent la catégorie {}".format(len(list_temp),self.categories)
                            
                            
                            selection_personne_hors_suivi = st.selectbox(label_selection_personne_hors_suivi, list_temp)

                            if selection_personne_hors_suivi:
                                temp = str(selection_personne_hors_suivi).split()
                                personne = "{} {}".format(temp[0], temp[1])
                                chorus = temp[3]

                                valeur = edit.verif_module_personne(chorus, code)
                                if valeur[1] == 'True':
                                    bt_radio_categorie_hors_suivi_personne = st.radio("Catégorie suivie :", {"Suivie", "Non suivie"}, key="bt_radio_cat_personne", index=1, disabled=True, horizontal=True)
                                elif valeur[1] == 'False':
                                    bt_radio_categorie_hors_suivi_personne = st.radio("Catégorie suivie :", {"Suivie", "Non suivie"}, key="bt_radio_cat_personne", index=0, disabled=True, horizontal=True)




                        else:
                            st.subheader("Aucune personne ne suit cette catégorie")
                    except:
                        pass



                    if "success" in st.session_state:
                        if st.session_state["success"] == True:
                            st.session_state["success"] ='false'
                            st.experimental_rerun()
                with column4:
                    pass
                with column5:
                    pass
                with column6:
                    pass
                    """
                    if "top5" in st.session_state:
                        st.subheader("🏆 Top 5 🏆")
                        i = 1
                        for elem in self.top5:
                            st.markdown("{} - {} |  {}".format(i, elem[0], elem[1]))
                            i += 1
                            if i >5:break
                    """




                


    def update_sql():
        csv = st.session_state["verif"]
        table = st.session_state["Table"]

        if table == "Suivi":
            update = edit.update_suivi(csv)
            return
        elif table == "Catalogue":
            update = edit.update_catalogue(csv)
            return
        elif table == "Effectifs":
            update = edit.update_effectifs(csv)
            return
        
    def clear():
        st.session_state.Choix = []
  
    def open(self):
        #self.init = sql.connect(f"Fichiers\{nom_db}", check_same_thread=False)
        self.list_workflow = Init.list_personnes() # -- Récupération des personnes suivies
        self.file = st.sidebar.file_uploader # -- Choix fichier effectifs
        self.choix_visu = st.radio("Changement de mode de visualisation", options=["Par équipe", "Par personne"])

        #app.sidebar(self.list_workflow) # -- Envoi des données vers le sidebar du site (menu glissant gauche)




        self.check = False
        self.info = st.sidebar.info
        self.error = st.sidebar.error
        self.header_title = st.title("Suivi formations") # -- Création variable titre page
        
        left_column, right_column = st.sidebar.columns(2)       
        with left_column:
            self.sidebar_left_title = st.sidebar.header("Menu principal") # -- Création variable titre menu glissant
        with right_column:
            self.manager_choice = st.selectbox # -- Liste déroulante manageurs
  

        self.trainings = synthese.Synth_Atelier() # -- Récupération des données formations
        self.formations_a_faire = self.trainings[0]
        self.formations_faites = self.trainings[1]
        self.formations_restantes = self.trainings[2]
        self.formations_hors_suivi = self.trainings[3]
        self.reactualisations = self.trainings[4]
        self.taux_respet_reactu = self.trainings[5]
        self.reactu_alerte = self.trainings[6]

        app.header_synthese()  # -- Envoi des données vers le header du site
        
    
    def _init(self):
        try:
            bdd = sql.connect(f'Fichiers\{nom_db}')
            _init = bdd.execute("SELECT * FROM Admins")

            for id in _init.fetchall():
                st.write(id[2])
                if id[2] == os.environ["USERNAME"]:
                    app.open()
                break

        except sql.Error:
            install._Init(self, bdd, nom_db)




if __name__ == "__main__":
    app = main()
    st.session_state["Workflow"] = False
    app._init()
    #app.open()
  
  


