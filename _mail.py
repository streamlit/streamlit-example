import win32com.client as win32 
import pythoncom
import pandas as pd
import streamlit as st
import os
import codecs
from time import sleep

class Mailing():
    def send_mail(to, cc, body, personne, manager):
        pythoncom.CoInitialize()
        body = pd.DataFrame(body)

        signature_path = os.path.join((os.environ['USERPROFILE']),'AppData\Roaming\Microsoft\Signatures\signature_fichiers\\') # Finds the path to Outlook signature files with signature name "Work"
        html_doc = os.path.join((os.environ['USERPROFILE']),'AppData\Roaming\Microsoft\Signatures\signature.htm')     #Specifies the name of the HTML version of the stored signature
        html_doc = html_doc.replace('\\\\', '\\') #Removes escape backslashes from path string


        html_file = codecs.open(html_doc, errors='ignore') #Opens HTML file and ignores errors
        signature_code = html_file.read()               #Writes contents of HTML signature file to a string
        signature_code = signature_code.replace('signature_fichiers/', signature_path)      #Replaces local directory with full directory path
        html_file.close()


        style = body.style.applymap(Mailing.color_etat, subset=['Jours restant'])   
        result = style.to_html()


        outlook = win32.gencache.EnsureDispatch('outlook.application') 
        mail = outlook.CreateItem(0) 
        mail.To = to
        mail.CC = cc + ';vincent.beaufort@michelin.com'
        mail.Subject = 'Message subject'
        mail.Body = 'Voici un exemple de mailing ;)' #body 
        mail.HTMLBody = f'<h1>Voici un exemple de mailing: </h1> <br><font color="red">En rouge : Formation en retard </font><br><br><font color="orange">En orange : A faire rapidement </font><br><br><font color="yellow">En jaune : A faire dans les 3 mois </font><br><br><br>{result}<br><br><br>' + signature_code #this field is optional # To attach a file to the email (optional): attachment = "Path to the attachment" mail.Attachments.Add(attachment) mail.Send()
        mail.Display(True)
        

        #attachment = "Path to the attachment" 
        #mail.Attachments.Add(attachment) 

        #mail.Send()
        st.info(f'Un email de rappel à été envoyé à {personne} et à {manager}')
        sleep(2)
        #st.experimental_rerun()

    def color_etat(x):
        color = ''
        
        try:
            if x <= 0 :color ='red'
            elif x < 30 and x > 0 : color ='orange'
            elif x > 30 and x < 90 : color ='#FFFF00'
            elif x > 90 :color ='green'
        except: pass

        return f'background-color: {color}'

