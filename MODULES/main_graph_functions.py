import pandas as pd
from tkinter import *
import os
import sys
# sys.path.append("menu_pro")
# from menu_pro import main
import hashlib
import requests
import logging
import smtplib, ssl
import tkinter as tk
import tkinter.messagebox as messagebox
sys.path.append("MODULES/users_graph_functions.py")
from MODULES.users_graph_functions import interface_user
import ttkbootstrap as ttk
from ttkbootstrap.constants import *




smtp_address = 'smtp.gmail.com'
smtp_port = 465 # Pour Gmail


email_address = 'mail_to_change'
email_password = 'app_password_to_change '


path_user="DATA/utilisateurs.csv"
path_product="DATA/products.csv"
path_rocku="DATA/rocku.csv"
path_credentials = "DATA/credentials.csv"



utilisateur_connecte = None


logging.basicConfig(filename='history.log', level=logging.INFO, 
                    format='%(asctime)s - %(username)s - %(message)s')

def log_request(username, compromised):
    status = 'Compromised' if compromised else 'Safe'
    logging.info(f'Username: {username}, Status: {status}', extra={'username': username})


def launch_main(id_user):
    try:
        df = pd.read_csv(path_credentials)
        if not df.empty:
            df.at[0, 'Id'] = id_user
        else:
            df = pd.DataFrame({"Id": [id_user]})
        df.to_csv(path_credentials, index=False)
    except FileNotFoundError:
        print("Fichier non trouvé")
        return
    


# Example usage:
#_Creation_____________________________________________________
#_______________________________________________________________

def creation():

    if os.path.exists(path_user):
        print("Données utilisateurs trouvées 🫡")
    else:
        df=pd.DataFrame(columns=["Id","Nom","Prenom","Login","Password","Salt"])
        df.to_csv(path_user, index=False)


    if os.path.exists(path_product):
        print("Données produits trouvées 🫡")
    else:
        df=pd.DataFrame(columns=["Name","Price","Quantity","Id"])
        df.to_csv(path_product, index=False)

    if os.path.exists(path_credentials):
        print("Credentials file found 🫡")
    else:
        df=pd.DataFrame(columns=["Id"])
        df.to_csv(path_credentials, index=False)



#_Connexion_____________________________________________________
#_______________________________________________________________

def hashed_input(password, salt) -> str:
    """Retourne le hash SHA-1 du mot de passe salé."""
    salted_pw = password + salt
    return hashlib.sha1(salted_pw.encode('utf-8')).hexdigest().upper()


def connexion():
    global window_connexion
    window_connexion = ttk.Window(themename="vapor")
    window_connexion.title("Connexion")

    #print('\nVeuillez renseigner tous les champs de connexion')
    text_champs =Label(window_connexion, text = "Veuillez renseigner tous les champs de connexion", font=("Helvetica", 16))
    text_champs.grid(row= 0, column=0, columnspan=2, padx=10, pady=10)
    
    #username = str(input('Login: '))
    text_username =Label(window_connexion, text = "Login (Mail):")
    text_username.grid(row=1, column=0, padx=10, pady=10)
    
    expression_username = StringVar()
    username =Entry(window_connexion, textvariable=expression_username, width=40) #str(input('Login: '))
    username.grid(row=1, column=1, padx=10, pady=10)
    
    #password = str(input('Password: '))
    text_password =Label(window_connexion, text = "Password:")
    text_password.grid(row=2, column=0, padx=10, pady=10)
    expression_password = StringVar()
    password =Entry(window_connexion, textvariable=expression_password, width=40)
    password.grid(row=2, column=1, padx=10, pady=10)
    
    bouton_connexion=ttk.Button(window_connexion, text="Connexion", bootstyle='PRIMARY', command=lambda: recherche_user(username, password))
    bouton_connexion.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    window_connexion.quit()
    window_connexion.mainloop()
#dsl
def recherche_user(username, password):

    username = username.get()
    password = password.get()
    
    df = pd.read_csv(path_user) # Données de la base de données sur les utilisateurs

    user = df[df['Login'] == username]
    if not user.empty:
        salt = user.iloc[0]['Salt']
        hashed_pw_input = hashed_input(password, salt)

        if user.iloc[0]['Password'] == hashed_pw_input:
            id_user = user.iloc[0]['Id']
        else:
            print("❌ -> Erreur : Utilisateur non trouvé")
            return

        if check_info_in_file(password) == True:
            log_request(username, True)
            
            #print("❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
            messagebox.showerror("Erreur", "❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
            
            send_mail(username)
            modifier_utilisateur(username, password)


        elif check_password_pwned(password) == True:
            log_request(username, True)
            #print("❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
            messagebox.showerror("Erreur", "❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
            
            send_mail(username)
            modifier_utilisateur(username, password)
        
        if user.iloc[0]['Password'] == hashed_pw_input:
            id_user = user.iloc[0]['Id']
            log_request(username, False)
            messagebox.showinfo("Succès", "✅ -> Connexion réussie.")
            window_connexion.destroy()
            launch_main(id_user)
            interface_user()
        else:
            #print("❌ -> Erreur : Utilisateur non trouvé")
            messagebox.showerror("Erreur", "❌ -> Erreur : Utilisateur non trouvé")
            return

    else:
        log_request(username, True)
        print("❌ -> Erreur : Utilisateur non trouvé")
        messagebox.showerror("Erreur", "❌ -> Erreur : Utilisateur non trouvé")


def send_mail(email_receiver):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        server.login(email_address, email_password)
        server.sendmail(email_address, email_receiver, f"Subject: MOT DE PASSE COMPROMIS\n\nVotre mot de passe est compromis, veuillez le changer.")

def modifier_utilisateur(login, password):
    global window_modify

    window_modify = ttk.Window(themename="vapor")
    window_modify.title('Modifications')

    login = login.get()
    password = password.get()

    window_launch_modify.destroy()

    try:
        df = pd.read_csv(path_user)

        user_row = df[df['Login'] == login]
        if not user_row.empty:
            id_user = user_row['Id'].values[0]
            salt = user_row['Salt'].values[0]
            hashed_pw = hashed_input(password, salt)

            if user_row['Password'].values[0] == hashed_pw:
                text_input_nom = Label(window_modify, text="Nom:")
                text_input_nom.pack(pady=(10, 5))
                input_nom = StringVar()
                input_nom_entry = Entry(window_modify, textvariable=input_nom, width=40)
                input_nom_entry.pack(pady=(5, 10))

                text_input_prenom = Label(window_modify, text="Prenom:")
                text_input_prenom.pack(pady=(10, 5))
                input_prenom = StringVar()
                input_prenom_entry = Entry(window_modify, textvariable=input_prenom, width=40)
                input_prenom_entry.pack(pady=(5, 10))

                text_input_login = Label(window_modify, text="Mail:")
                text_input_login.pack(pady=(10, 5))
                input_login = StringVar()
                input_login_entry = Entry(window_modify, textvariable=input_login, width=40)
                input_login_entry.pack(pady=(5, 10))

                text_input_password = Label(window_modify, text="Password:")
                text_input_password.pack(pady=(10, 5))
                input_password = StringVar()
                input_password_entry = Entry(window_modify, textvariable=input_password, width=40, show='*')
                input_password_entry.pack(pady=(5, 10))

                bouton_modifier = ttk.Button(window_modify, text="Modifier", command=lambda: edit_user(input_nom, input_prenom, input_login, input_password, id_user), bootstyle="PRIMARY")
                bouton_modifier.pack(pady=20)

            else:
                messagebox.showerror("Erreur", "❌  Mot de passe incorrect")
                window_modify.destroy()
        else:
            messagebox.showerror("Erreur", "❌  Utilisateur non trouvé")
            window_modify.destroy()

    except FileNotFoundError:
        log_request(login, True)
        print("Fichier non trouvé")
        return

    window_modify.mainloop()

def edit_user(nom, prenom,login,password,id_user):

    nom = nom.get()
    prenom = prenom.get()
    login = login.get()
    password = password.get()

    df = pd.read_csv(path_user)
    new_salt = generate_salt()
    hashed_pw_input = hashed_input(password, new_salt)
    if check_info_in_file(hashed_pw_input) == True:
        log_request(login, True)
        #print("❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
        messagebox.showerror("Erreur", "❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
        return
    
    if check_password_pwned(password) == True:
        log_request(login, True)
        #print("Mot de passe compromis 😬, utilisez un autre mot de passe 😉")
        messagebox.showerror("Erreur", "Mot de passe compromis 😬, utilisez un autre mot de passe 😉")
        return
    
    # Mise à jour des informations de l'utilisateur
    df.loc[df['Id'] == id_user, 'Nom'] = nom
    df.loc[df['Id'] == id_user, 'Prenom'] = prenom
    df.loc[df['Id'] == id_user, 'Login'] = login
    df.loc[df['Id'] == id_user, 'Password'] = hashed_pw_input
    df.loc[df['Id'] == id_user, 'Salt'] = new_salt

    df.to_csv(path_user, index=False)
    log_request(login, False)
    #print("✅ -> Utilisateur modifié avec succès.")
    messagebox.showinfo("Succès", "✅ -> Utilisateur modifié avec succès.")
    window_modify.destroy()
    

def launch_modify_user():
    global window_launch_modify
    window_launch_modify = ttk.Window(themename="vapor")
    window_launch_modify.geometry("400x200")
    window_launch_modify.title("Modification de compte")

    text_input_login = Label(window_launch_modify, text = "Mail:")
    text_input_login.pack(pady=(10,5), padx=10)

    input_login = StringVar()
    input_login = Entry(window_launch_modify, textvariable=input_login, width=40)
    input_login.pack(pady=(5,10), padx=10)

    text_input_password = Label(window_launch_modify, text = "Mot de passe:")
    text_input_password.pack(pady=(10,5), padx=10)

    input_password = StringVar()
    input_password = Entry(window_launch_modify, textvariable=input_login, width=40)
    input_password.pack(pady=(5,10), padx=10)

    bouton_modifier = ttk.Button(window_launch_modify, text="Modifier", command=lambda: modifier_utilisateur(input_login, input_password), bootstyle="PRIMARY")
    bouton_modifier.pack(pady=5, padx=10)

    window_launch_modify.mainloop()
    

#_Inscription__________________________________________________
#______________________________________________________________


def generate_salt():
    """Génère un sel aléatoire de 16 octets"""
    return os.urandom(16).hex()


def inscription_ajout(nom, prenom, login, password):
    nom = nom.get()
    prenom = prenom.get()
    login = login.get()
    password = password.get()
    

    df = pd.read_csv(path_user)
    
    if 'Id' not in df.columns:
        df['Id'] = range(1, len(df) + 1)
    if 'Salt' not in df.columns:
        df['Salt'] = ''
    
    if login in df['Login'].values:
        #print(f"❌ -> Le login '{login}' existe déjà. Veuillez en choisir un autre.")
        text_login_already_used = Label(window_inscription, text = "❌ -> Le login '{login}' existe déjà. Veuillez en choisir un autre")
        text_login_already_used.pack()
        return
    
    new_id = df['Id'].max() + 1 if not df.empty else 1

    salt = generate_salt()
    hashed_pw = hashed_input(password, salt)
    
    if check_info_in_file(hashed_pw) == True:
        #print("❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
        text_password_pwnd = Label(window_inscription, text = "❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
        text_password_pwnd.pack()
        return
    
    if check_password_pwned(password) == True:
        #print("❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
        text_password_pwnd = Label(window_inscription, text = "❌ -> Ce mot de passe est compromis. Veuillez en choisir un autre.")
        text_password_pwnd.pack()
        return
    
    ligne = pd.DataFrame({"Id": [new_id], "Nom": [nom], "Prenom": [prenom], "Login": [login], "Password": [hashed_pw], "Salt": [salt]})
    print("\nNouvelle ligne à ajouter:")
    print(ligne)
    
    df = pd.concat([df, ligne], ignore_index=True)
    
    df.to_csv(path_user, index=False)
    print("Fichier mis à jour avec succès. 🫡")

    messagebox.showinfo("Succès", "✅ -> Inscription réussie.")
    window_inscription.destroy()
    


def inscription():
    global window_inscription
    window_inscription = ttk.Window(themename="vapor")
    window_inscription.geometry("400x400")
    window_inscription.title("Inscription")
    #print('\nVeuillez renseigner tous les champs de connexion')
    text_inscription = Label(window_inscription, text = "Veuillez renseigner tous les champs de connexion")
    text_inscription.pack(pady=(5,10), padx=10)
    
    #nom=str(input('Nom:'))
    text_nom = Label(window_inscription, text = "Nom:")
    text_nom.pack(pady=(10,5))
    nom = StringVar()
    nom = Entry(window_inscription, textvariable=nom, width=40)
    nom.pack(pady=(5,10), padx=10)

    #prenom=str(input('Prenom:'))
    text_prenom = Label(window_inscription, text = "Prenom:")
    text_prenom.pack(pady=(10,5))
    prenom = StringVar()
    prenom = Entry(window_inscription,textvariable=prenom, width=40)
    prenom.pack(pady=(5,10), padx=10)
    
    #login=str(input('Login:'))
    text_login = Label(window_inscription, text = "Mail:")
    text_login.pack(pady=(10,5))
    login = StringVar()
    login = Entry(window_inscription,textvariable=login, width=40)
    login.pack(pady=(5,10), padx=10)

    #password=str(input('Password:'))
    text_password = Label(window_inscription, text = "Password: ")
    text_password.pack(pady=(10,5))
    password = StringVar()
    password = Entry(window_inscription,    textvariable=password, width=40)
    password.pack(pady=(5,10), padx=10)

    Bouton = ttk.Button(window_inscription, text="Sign in", command=lambda: inscription_ajout(nom, prenom, login, password), bootstyle="PRIMARY")
    Bouton.pack()

    
    window_inscription.mainloop()

def check_info_in_file(password):
    try:
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        df = pd.read_csv(path_rocku, encoding='utf-8')
        if sha1_hash in df.values:
            print(f"Information found: {password}")
            return True
        else:
            print("Information not found in the file.")
            return False
    except FileNotFoundError:
        print(f"The file {path_rocku} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")



#_Suppression_Compte___________________________________________
#______________________________________________________________
def delete_account():
    def confirm_deletion():
        input_login = login_var.get()
        input_password = password_var.get()

        df_users = pd.read_csv(path_user)
        user_row = df_users[df_users['Login'] == input_login]
        if not user_row.empty:
            salt = user_row['Salt'].values[0]
            hashed_pw = hashed_input(input_password, salt)

            if user_row['Password'].values[0] == hashed_pw:
                id_user = user_row['Id'].values[0]

                df_products = pd.read_csv(path_product)
                if id_user in df_products['Id'].values:
                    df_products = df_products[df_products['Id'] != id_user]
                    df_products.to_csv(path_product, index=False)
                    print("\n✅ -> Produits supprimés avec succès 🫡")

                df_users = df_users[df_users['Id'] != id_user]
                df_users.to_csv(path_user, index=False)
                print("✅ -> Utilisateur supprimé avec succès 🫡")
                messagebox.showinfo("Succès", "✅ -> Utilisateur supprimé avec succès.")
                window_delete.destroy()
            else:
                messagebox.showerror("Erreur", "❌ Identifiant ou mot de passe incorrect.")
        else:
            messagebox.showerror("Erreur", "❌ Identifiant ou mot de passe incorrect.")

    def cancel_deletion():
        messagebox.showinfo("Annulé", "❌ Suppression annulée.")
        window_delete.destroy()

    window_delete = tk.Toplevel()
    window_delete.title("Supprimer le compte")

    text_confirmation = tk.Label(window_delete, text="🚨 Voulez vous vraiment supprimer votre compte ? 🚨")
    text_confirmation.pack()

    login_var = tk.StringVar()
    password_var = tk.StringVar()

    text_input_login = tk.Label(window_delete, text="🧔‍♂️ Identifiant:")
    text_input_login.pack()
    input_login = tk.Entry(window_delete, textvariable=login_var, width=40)
    input_login.pack(pady=10)

    text_input_password = tk.Label(window_delete, text="🔑 Mot de passe:")
    text_input_password.pack()
    input_password = tk.Entry(window_delete, textvariable=password_var, width=40, show="*")
    input_password.pack(pady=10)

    yes_button = ttk.Button(window_delete, text="Supprimer", command=confirm_deletion, bootstyle="DANGER")
    yes_button.pack(pady=10)

    no_button = ttk.Button(window_delete, text="Annuler", command=cancel_deletion)
    no_button.pack(pady=10)




#_Mot_de_passe_compromis_______________________________________
#______________________________________________________________

def check_password_pwned(password: str) -> bool:
    """Vérifie si un mot de passe est compromis via Have I Been Pwned."""
    
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]  # Les 5 premiers caractères du hash
    suffix = sha1_hash[5:]  # Le reste du hash

    # Appeler l'API de HIBP
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête à l'API HIBP : {response.status_code}")

    # Vérifier si le suffixe est dans la réponse
    hashes = response.text.splitlines()
    for line in hashes:
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            print(f"😨 Mot de passe compromis ! Trouvé {count} fois. Veulliez en choisir un autre 💡.")
            return True

    print("✅ Mot de passe sûr. Pas trouvé dans les bases de données compromises.")
    return False

#_interface graphique_____________________________________________________

