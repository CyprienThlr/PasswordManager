import tkinter as tk
from tkinter import messagebox
import random
import string


# Fonction pour générer le mot de passe
def generate_password():
    length = int(entry_length.get())  # Obtenir la longueur du mot de passe souhaitée
    if length < 4:
        messagebox.showwarning("Erreur", "La longueur du mot de passe doit être d'au moins 4 caractères.")
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)


# Fonction pour copier le mot de passe dans le presse-papiers
def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(entry_password.get())
    messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers!")


# Créer la fenêtre principale
window = tk.Tk()
window.title("Générateur de mot de passe")

# Créer les widgets
label_length = tk.Label(window, text="Longueur du mot de passe :")
label_length.pack(pady=5)

entry_length = tk.Entry(window)
entry_length.pack(pady=5)

button_generate = tk.Button(window, text="Générer", command=generate_password)
button_generate.pack(pady=5)

label_password = tk.Label(window, text="Mot de passe généré :")
label_password.pack(pady=5)

entry_password = tk.Entry(window, width=30)
entry_password.pack(pady=5)

button_copy = tk.Button(window, text="Copier", command=copy_to_clipboard)
button_copy.pack(pady=5)

# Lancer la boucle principale
window.mainloop()