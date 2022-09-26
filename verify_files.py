
import streamlit as st
import pandas as pd
from numpy import *
import os



class verify():
    def verify_file(self, files):
        chemin = "C:/Users/{}/Documents".format(os.environ.get( "USERNAME" ))
        
        #files = r'C:\Users\F269167\OneDrive - MFP Michelin\Projets en cours\Suivi formations\Base Excel-Access\InstallV3\Fichiers\EFF Cfe à Fin fév 2022 sans coeff.xlsx'
        try:
            read_file = pd.read_excel (files)
            

        #Remplace toutes les entêtes qui contiennent des ' ' par des '_'
            i = 0
            ii = 0
            for rows in read_file.values:
                if rows[3] is NaN:
                    i=i+1
                else:
                    if i != 0:
                        for ii in range(i):
                            read_file.drop(ii, inplace=True)
                        
                        new_header = read_file.iloc[0]
                        
                        read_file = read_file[1:] #take the data less the header row
                        read_file.columns = new_header #set the header row as the df header

                        read_file.columns = read_file.columns.str.strip().str.replace(' ', '_')
                        read_file.columns = read_file.columns.str.strip().str.replace("'", "")
                        if "Professional_Category" in read_file:

                            update_table = "Effectifs"
                        elif "Enrollment_Date_and_Time_Completed" in read_file:

                            update_table = "Suivi"
                        elif "Code_de_la_formation" in read_file:

                            update_table = "Catalogue"
                        else:
                            st.warning("Ce fichier ne correspond pas au fichier attendu. (fichier attendu : Rpt Learn completed, EFF ou Catalogue")                        
                        break

                    else:
                        read_file.columns = read_file.columns.str.strip().str.replace(' ', '_')
                        read_file.columns = read_file.columns.str.strip().str.replace("'", "")

                        if "Professional_Category" in read_file:

                            update_table = "Effectifs"
                        elif "Enrollment_Date_and_Time_Completed" in read_file:

                            update_table = "Suivi"
                        elif "Code_de_la_formation" in read_file:

                            update_table = "Catalogue"
                        else:
                            st.sidebar.warning("Ce fichier ne correspond pas au fichier attendu. (fichier attendu : Rpt Learn completed, EFF ou Catalogue")
                        break

            try:
                read_file.to_csv (chemin + "/ext.csv", index = None, header=True)
                self.Extract_csv = chemin + "/ext.csv"

                return self.Extract_csv, update_table
        
            except:
                
                return ("Erreur sur l'encodage xls-csv")

        except:
            return ("Erreur pendant la lecture du fichier. Verifier l'état du fichier...")

