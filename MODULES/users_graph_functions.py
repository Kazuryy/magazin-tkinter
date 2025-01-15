import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

path='DATA/products.csv'
path_user="DATA/utilisateurs.csv"
path_credentials="DATA/credentials.csv"





#_____CUSTOM_______________________________________________________________________________
def personalisation(index_user):
    df = pd.read_csv(path_user)
    if index_user in df['Id'].values:
        global nom_user
        nom_user = df.loc[df['Id'] == index_user, 'Nom'].values[0]
        
        global prenom_user
        prenom_user = df.loc[df['Id'] == index_user, 'Prenom'].values[0]
        
        print(f"\n👤 -> Bienvenue dans votre espace vendeur {prenom_user} {nom_user}! 😁")
    
    else:
        print("Erreur Identification.")



#___AJOUT___________________________________________________________________________________________

def ajout(index_user):
    global window_add_products
    window_add_products = ttk.Window(themename="vapor")
    window_add_products.title("Ajout de produits")
    try:

        # name = str(input('Nom du produit'))
        text_nom = Label(window_add_products, text = "Nom:", font=("Helvetica", 12))
        text_nom.grid(row=0, column=0, pady=10)
        
        name = StringVar()
        name_entry = Entry(window_add_products, textvariable=name, width=40)
        name_entry.grid(row=0, column=1, pady=10)

        # price = str(input('Prix du produit'))
        text_price =Label(window_add_products, text = "Prix:", font=("Helvetica", 12))
        text_price.grid(row=1, column=0, pady=10)
        
        price = StringVar()
        price_entry=Entry(window_add_products, textvariable=price, width=40)
        price_entry.grid(row=1, column=1, pady=10)
        
        
        #quantity = str(input('Quantité du produit'))
        text_quantity =Label(window_add_products, text ="Quantité:", font=("Helvetica", 12))
        text_quantity.grid(row=2, column=0, pady=10)
        
        quantity= StringVar()
        quantity_entry = Entry(window_add_products, textvariable=quantity, width=40)
        quantity_entry.grid(row=2, column=1, pady=10)

        add_button = ttk.Button(window_add_products, text="Ajouter", command=lambda : add_to_list(name_entry.get(), price_entry.get(), quantity_entry.get(), index_user), bootstyle='PRIMARY')
        add_button.grid(row=3, column=0,pady=10)
        
        btn_leave = ttk.Button(window_add_products, text="Quitter",command= lambda: window_add_products.destroy(), bootstyle='DANGER' )
        btn_leave.grid(row=3, column=1,pady=10)

        window_add_products.mainloop()
        
    except FileNotFoundError:
        #print("\n❌ -> Erreur : le fichier n'a pas été trouvé.")
        messagebox.showerror("❌ -> Erreur : le fichier n'a pas été trouvé.")
    

def add_to_list(name, price, quantity, index_user):
    try:
        df = pd.read_csv(path)
        ligne=pd.DataFrame({"Name":[name],"Price":[price],"Quantity":[quantity], "Id": [index_user]}) # Ajouter en fonction de l'utilisateur
        df= pd.concat([df,ligne], ignore_index=True)
        df.to_csv(path, index=False)
        print("\n✅ -> Produit ajouté avec succès 🫡")
        messagebox.showinfo("Produit ajouté avec succès 🫡")
        window_add_products.destroy()
    except FileNotFoundError:
        #print("\n❌ -> Erreur : le fichier n'a pas été trouvé.")
        messagebox.showerror("❌ -> Erreur : le fichier n'a pas été trouvé.")
    

#___MODIFICATION________________________________________________________________________________________________

import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, StringVar, Entry, Label

def edit_product(index_user):
    global window_edit_products
    window_edit_products = ttk.Window(themename="vapor")
    window_edit_products.title("Edit products")
    
    # Variables pour stocker les entrées
    input_nom_var = StringVar()
    new_name_var = StringVar()
    new_price_var = StringVar()
    new_quantity_var = StringVar()
    
    # Création des widgets
    text = Label(window_edit_products, text="Nom du produit à modifier :", font=("Helvetica", 12))
    text.grid(row=0, column=0, pady=10)
    
    input_nom = Entry(window_edit_products, textvariable=input_nom_var, width=40)
    input_nom.grid(row=0, column=1, pady=10)

    text_new_name = Label(window_edit_products, text="Nouveau nom du produit:", font=("Helvetica", 12))
    text_new_name.grid(row=1, column=0, pady=10)
    
    new_name_entry = Entry(window_edit_products, textvariable=new_name_var, width=40)
    new_name_entry.grid(row=1, column=1, pady=10)

    text_new_price = Label(window_edit_products, text="Nouveau prix du produit:", font=("Helvetica", 12))
    text_new_price.grid(row=2, column=0, pady=10)
    
    new_price_entry = Entry(window_edit_products, textvariable=new_price_var, width=40)
    new_price_entry.grid(row=2, column=1, pady=10)

    text_new_quantity = Label(window_edit_products, text="Nouvelle quantité du produit:", font=("Helvetica", 12))
    text_new_quantity.grid(row=3, column=0, pady=10)
    
    new_quantity_entry = Entry(window_edit_products, textvariable=new_quantity_var, width=40)
    new_quantity_entry.grid(row=3, column=1, pady=10)
    
    def save_changes():
        try:
            input_nom_value = input_nom.get()
            new_name = new_name_entry.get()
            new_price = new_price_entry.get()
            new_quantity = new_quantity_entry.get()
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(path)
            
            # Check if the product exists and edit it
            if input_nom_value in df['Name'].values and index_user in df['Id'].values:
                result = df[(df['Name'] == input_nom_value) & (df['Id'] == index_user)]
                
                if not result.empty:
                    # Update the product information
                    df.loc[(df['Name'] == input_nom_value) & (df['Id'] == index_user), 'Price'] = new_price
                    df.loc[(df['Name'] == input_nom_value) & (df['Id'] == index_user), 'Quantity'] = new_quantity
                    df.loc[(df['Name'] == input_nom_value) & (df['Id'] == index_user), 'Name'] = new_name
                    
                    # Write the updated DataFrame back to the CSV file
                    df.to_csv(path, index=False)
                    messagebox.showinfo("Succès", "✅ -> Produit modifié avec succès")
                    window_edit_products.destroy()
                else:
                    messagebox.showerror("Erreur", "❌ -> Produit non trouvé")
            else:
                messagebox.showerror("Erreur", "❌ -> Produit non trouvé")
                
        except FileNotFoundError:
            messagebox.showerror("Erreur", "❌ -> Erreur : Le fichier 'produits.csv' n'existe pas.")
        except PermissionError:
            messagebox.showerror("Erreur", "❌ -> Erreur : Vous n'avez pas les permissions nécessaires")
        except ValueError:
            messagebox.showerror("Erreur", "❌ -> Erreur : Veuillez entrer des valeurs numériques valides pour le prix et la quantité")
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ -> Une erreur s'est produite : {e}")

    # Boutons
    btn_save = ttk.Button(window_edit_products, text="Sauvegarder", command=save_changes, bootstyle="PRIMARY")
    btn_save.grid(row=4, column=0, pady=10)
    
    btn_leave = ttk.Button(window_edit_products, text="Quitter", command=window_edit_products.destroy, bootstyle="DANGER")
    btn_leave.grid(row=4, column=1,  pady=10)
    
    window_edit_products.mainloop()




#___VOIR______________________________________________



def show_user_products(index_user):
    try:
        df = pd.read_csv(path)
        df_user = df[df['Id'] == index_user]
        
        if df_user.empty:
            messagebox.showinfo("Information", "❌ Aucun produit trouvé pour cet utilisateur.")
            return

        # Create a new window to display the result
        result_window = ttk.Toplevel()
        result_window.title("Liste des produits")
        result_window.geometry("600x400")

        # Création du frame principal
        tree_frame = ttk.Frame(result_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Création du Treeview
        tree = ttk.Treeview(tree_frame, columns=list(df_user.columns), show='headings')
        tree.pack(side='left', fill='both', expand=True)

        # Configuration des colonnes
        for col in df_user.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        # Insertion des données
        for index, row in df_user.iterrows():
            tree.insert('', 'end', values=list(row))

        # Création de la scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.config(yscrollcommand=scrollbar.set)

        # Bouton de fermeture
        close_button = ttk.Button(result_window, text="Fermer", command=result_window.destroy, bootstyle='DANGER')
        close_button.pack(pady=10)

        result_window.mainloop()

    except FileNotFoundError:
        messagebox.showinfo("Erreur", "❌ -> Erreur : le fichier n'a pas été trouvé.")
    
    except PermissionError:
        messagebox.showinfo("Erreur", "❌ -> Erreur : permissions insuffisantes pour ouvrir le fichier.")
    
    except Exception as e:
        messagebox.showinfo("Erreur", f"❌ -> Erreur inattendue : {e}")






#___SUPPRIMER__________________________________________
#______________________________________________________

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
from tkinter import messagebox, StringVar

def delete_produit(index_user):
    global window_delete_products
    window_delete_products = ttk.Window(themename="vapor")
    window_delete_products.title("Supprimer un produit")
    window_delete_products.geometry("400x300")
    
    # Variable pour stocker l'entrée
    input_nom_var = StringVar()
    
    # En-tête
    header = Label(
        window_delete_products, 
        text="Suppression de produit"
    )
    header.pack(pady=20)
    
    # Zone de saisie
    text_nom = Label(
        window_delete_products,
        text="Nom du produit à supprimer :"
    )
    text_nom.pack(pady=5)
    
    input_entry = Entry(
        window_delete_products,
        textvariable=input_nom_var
    )
    input_entry.pack(pady=5)
    
    def confirm_delete():
        try:
            product_name = input_entry.get().strip()
            
            if not product_name:
                messagebox.showwarning("Attention", "Veuillez entrer un nom de produit.")
                return
                
            # Read the CSV file into a DataFrame
            df = pd.read_csv(path)
            
            # Check if the product exists and remove it
            if product_name in df['Name'].values and index_user in df['Id'].values:
                result = df[(df['Name'] == product_name) & (df['Id'] == index_user)]
                
                if not result.empty:
                    # Demander confirmation
                    confirm = messagebox.askyesno(
                        "Confirmation",
                        f"Êtes-vous sûr de vouloir supprimer le produit '{product_name}' ?"
                    )
                    
                    if confirm:
                        df = df[~((df['Name'] == product_name) & (df['Id'] == index_user))]
                        df.to_csv(path, index=False)
                        messagebox.showinfo("Succès", "✅ Produit supprimé avec succès")
                        window_delete_products.destroy()
                else:
                    messagebox.showwarning(
                        "Attention",
                        "❌ Ce produit n'existe pas dans votre liste"
                    )
            else:
                messagebox.showwarning(
                    "Attention",
                    "❌ Ce produit n'existe pas dans votre liste"
                )
                
        except FileNotFoundError:
            messagebox.showerror("Erreur", "❌ Le fichier 'produits.csv' n'existe pas.")
        except PermissionError:
            messagebox.showerror("Erreur", "❌ Permissions insuffisantes pour modifier le fichier.")
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Une erreur s'est produite : {e}")
    
    # Boutons
    btn_delete = ttk.Button(
        window_delete_products,
        text="Supprimer",
        command=confirm_delete,
        bootstyle='DANGER'
    )
    btn_delete.pack(padx=5, pady=(20,10))
    
    btn_leave = ttk.Button(
        window_delete_products,
        text="Annuler",
        command=window_delete_products.destroy,
        bootstyle='SECONDARY'
    )
    btn_leave.pack(padx=5, pady=10)
    
    # Centrer la fenêtre
    window_delete_products.update_idletasks()
    width = window_delete_products.winfo_width()
    height = window_delete_products.winfo_height()
    x = (window_delete_products.winfo_screenwidth() // 2) - (width // 2)
    y = (window_delete_products.winfo_screenheight() // 2) - (height // 2)
    window_delete_products.geometry(f'{width}x{height}+{x}+{y}')
    
    window_delete_products.mainloop()


#___RECHERCHE__________________________________________
#______________________________________________________

def search_product(exp_input_nom, index_user):
    product_name = exp_input_nom.get().strip()
    df = pd.read_csv(path)
    
    df['Name'] = df['Name'].astype(str).str.strip()
    df['Id'] = df['Id'].astype(int)
    
    result = df[(df['Name'] == product_name) & (df['Id'] == index_user)]
    
    if not result.empty:
        # Formater le résultat de manière plus lisible
        info = f"""
        Produit trouvé :
        ------------------
        Nom : {result['Name'].iloc[0]}
        Prix : {result['Price'].iloc[0]} €
        Quantité : {result['Quantity'].iloc[0]}
        ID : {result['Id'].iloc[0]}
        """
        messagebox.showinfo("✅ Produit trouvé", info)
    else:
        messagebox.showerror("❌ Produit non trouvé", 
                           "Aucun produit ne correspond à votre recherche.\nVérifiez l'orthographe et réessayez.")

def search(index_user):
    global window_search_products
    window_search_products = Tk()
    window_search_products.title("Recherche de produits")
    window_search_products.geometry("400x300")  # Taille fixe pour la fenêtre
    
    # Ajout de padding général
    main_frame = Frame(window_search_products, padx=20, pady=20)
    main_frame.pack(expand=True, fill='both')
    
    # Titre
    title = Label(main_frame, 
                 text="Recherche de produits",
                 font=("Helvetica", 16, "bold"))
    title.pack(pady=(0, 20))
    
    # Frame pour le champ de recherche
    search_frame = Frame(main_frame)
    search_frame.pack(fill='x', pady=(0, 15))
    
    text_nom = Label(search_frame, 
                    text="Nom du produit :",
                    font=("Helvetica", 10))
    text_nom.pack(anchor='w')
    
    exp_input_nom = StringVar(window_search_products)
    input_nom = Entry(search_frame, 
                     textvariable=exp_input_nom,
                     width=40,
                     font=("Helvetica", 10),
                     justify=CENTER)
    input_nom.pack(fill='x', pady=(5, 0))
    
    # Frame pour les boutons
    button_frame = Frame(main_frame)
    button_frame.pack(pady=20)
    
    search_button = ttk.Button(button_frame,
                         text="🔍 Rechercher",
                         command=lambda: search_product(exp_input_nom, index_user),
                         bootstyle='PRIMARY')
    search_button.pack(side=LEFT, padx=5)
    
    btn_leave = ttk.Button(button_frame,
                      text="❌ Quitter",
                      command=window_search_products.destroy,
                      bootstyle='DANGER')
    btn_leave.pack(side=LEFT, padx=5)
    
    # Indication pour l'utilisateur
    help_text = Label(main_frame,
                     text="Entrez le nom exact du produit et cliquez sur Rechercher",
                     font=("Helvetica", 9, "italic"),
                     fg="gray")
    help_text.pack(pady=(10, 0))
    
    window_search_products.mainloop()

#___TRI________________________________________________
#______________________________________________________
# Ne Fonctionne pas
def configure_apple_style():
    # Configuration du style Apple pour les widgets Tkinter
    style = {
        "font": ('SF Pro Display', 14),
        "bg": "#007AFF",  # Couleur bleue typique des boutons Apple
        "fg": "white",
        "activebackground": "#005BB5",  # Couleur bleue plus foncée pour l'état actif
        "activeforeground": "white",
        "relief": "flat",
        "bd": 0,
        "highlightthickness": 0,
        "padx": 10,
        "pady": 5
    }
    return style

def display_sorted_data(tree, sort_by, path, index_user):
    for item in tree.get_children():
        tree.delete(item)
        
    try:
        df = pd.read_csv(path)
        df_filtered = df[df['Id'] == index_user]
        df_sorted = df_filtered.sort_values(by=sort_by, ascending=True)
        
        for index, row in df_sorted.iterrows():
            tree.insert('', 'end', values=(row['Name'], row['Price'], row['Quantity'], row['Id']))
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

def sort(index_user):
    global window_sort_products
    window_sort_products = Tk()
    window_sort_products.title("Tri des produits")
    window_sort_products.geometry("800x500")
    window_sort_products.configure(bg="white")

    # Configuration du style Apple
    apple_style = configure_apple_style()

    # Frame principale avec padding
    main_frame = Frame(window_sort_products, bg="white", padx=30, pady=30)
    main_frame.pack(expand=True, fill='both')

    # Titre dans le style Apple
    title = Label(main_frame, 
                 text="Mes Produits",
                 font=('SF Pro Display', 24, 'bold'),
                 bg="white",
                 fg="#1d1d1f")
    title.pack(pady=(0, 30), anchor='w')

    # Frame pour le tableau
    result_frame = Frame(main_frame, bg="white")
    result_frame.pack(fill='both', expand=True)

    # Configuration du Treeview
    tree = ttk.Treeview(result_frame, 
                       columns=('Name', 'Price', 'Quantity', 'Id'), 
                       show='headings',
                       style="Treeview")
    
    # Configuration des colonnes
    tree.heading('Name', text='Nom')
    tree.heading('Price', text='Prix')
    tree.heading('Quantity', text='Quantité')
    tree.heading('Id', text='ID')
    
    # Ajuster la largeur des colonnes
    tree.column('Name', width=200)
    tree.column('Price', width=100)
    tree.column('Quantity', width=100)
    tree.column('Id', width=100)

    # Scrollbar style Apple
    scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Frame pour les boutons avec fond blanc
    button_frame = Frame(main_frame)
    button_frame.pack(pady=30)



    # Boutons avec style Apple
    btn_tri_nom = ttk.Button(button_frame, 
                        text="Trier par nom",
                        command=lambda: display_sorted_data(tree, 'Name', path, index_user),
                        bootstyle='PRIMARY',)
    btn_tri_nom.pack(side=LEFT, padx=10)

    btn_tri_prix = ttk.Button(button_frame,
                         text="Trier par prix",
                         command=lambda: display_sorted_data(tree, 'Price', path, index_user),
                         bootstyle='PRIMARY')
    btn_tri_prix.pack(side=LEFT, padx=10)

    btn_tri_quantite = ttk.Button(button_frame,
                            text="Trier par quantité",
                            command=lambda: display_sorted_data(tree, 'Quantity', path, index_user),
                            bootstyle='PRIMARY')
    btn_tri_quantite.pack(side=LEFT, padx=10)

    # Bouton Quitter avec style différent
    btn_leave = ttk.Button(button_frame,
                      text="Fermer",
                      command=window_sort_products.destroy,
                        bootstyle='SECONDARY')
    btn_leave.pack(side=LEFT, padx=10)

    # Affichage initial
    display_sorted_data(tree, 'Name', path, index_user)

    window_sort_products.mainloop()
# Importer la valeur depuis le fichier main_graph_functions.py pour créer la session
def set_index_user():
    try:
        df = pd.read_csv(path_credentials)
        index_user = df.iloc[0]['Id']
        return index_user
    except FileNotFoundError:
        print(f"❌ -> Erreur : le fichier {path_credentials} n'a pas été trouvé.")

def interface_user():
    window_menu_user = ttk.Window(themename="vapor")
    window_menu_user.title("Menu utilisateur")
    window_menu_user.geometry("1000x600")

    index_user = set_index_user()
    print(index_user)
    
    adding_products_button =ttk.Button(window_menu_user, text="Ajouter des produits 📦", command=lambda : ajout(index_user)) 
    adding_products_button.pack(pady=10)

    edit_products_button = ttk.Button(window_menu_user, text="Modification des produits 🛠️", command=lambda : edit_product(index_user)) 
    edit_products_button.pack(pady=10)

    see_products_button = ttk.Button(window_menu_user, text="Voir les produits", command=lambda : show_user_products(index_user)) 
    see_products_button.pack(pady=10)

    delete_products_button =ttk.Button(window_menu_user, text="Suppression de produits 🗑️", command=lambda : delete_produit(index_user))
    delete_products_button.pack(pady=10)

    search_product_button =ttk.Button(window_menu_user, text="Recherche d'un produit 🔍", command=lambda : search(index_user) )
    search_product_button.pack(pady=10)

    sort_product_button =ttk.Button(window_menu_user, text="Trier les produits 📊", command=lambda : sort(index_user) )
    sort_product_button.pack(pady=10)

    log_out_button =ttk.Button(window_menu_user, text="Déconnexion -> 🚪", command=lambda : window_menu_user.destroy()) 
    log_out_button.pack(pady=10)

    window_menu_user.mainloop()

interface_user()