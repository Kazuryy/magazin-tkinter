from tkinter import *
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
sys.path.append("MODULES/main_graph_functions.py")
from MODULES.main_graph_functions import  creation, connexion, inscription, delete_account, launch_modify_user

creation()


window = ttk.Window(themename="vapor")
window.title("Menu principal")
window.geometry("1000x600")

# Définir un style pour le bouton
style = ttk.Style()
style.configure("Custom.TButton", font=("Helvetica", 16))

connexion_button = ttk.Button(window, text="Connexion", command=connexion, bootstyle="PRIMARY") 
connexion_button.pack(pady=(40,10))

inscription_button = ttk.Button(window, text="Inscription", command=inscription, bootstyle="PRIMARY") 
inscription_button.pack(pady=10)

modification_button = ttk.Button(window, text="Modification de compte", command=launch_modify_user, bootstyle="WARNING") 
modification_button.pack(pady=(30,10))

delete_button = ttk.Button(window, text="Suppression de compte ",command=delete_account, bootstyle="DANGER")
delete_button.pack(pady=5)

quit_button = ttk.Button(window, text="Quitter", command= window.quit, bootstyle="SECONDARY")
quit_button.pack(pady=20)

window.mainloop()
