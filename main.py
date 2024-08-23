import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import json
import os


# Générer une clé de chiffrement
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Charger la clé de chiffrement
def load_key():
    return open("secret.key", "rb").read()


# Chiffrer un mot de passe
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password


# Déchiffrer un mot de passe
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password


# Enregistrer un mot de passe
def save_password(account, password, key):
    encrypted_password = encrypt_password(password, key)
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
    else:
        data = {}
    data[account] = encrypted_password.decode()
    with open("passwords.json", "w") as file:
        json.dump(data, file)


# Récupérer un mot de passe
def load_password(account, key):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
        encrypted_password = data.get(account)
        if encrypted_password:
            return decrypt_password(encrypted_password.encode(), key)
        else:
            return None
    else:
        return None


class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.key = load_key()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Password Manager")
        self.label.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Password", command=self.add_password)
        self.add_button.pack(pady=5)

        self.retrieve_button = tk.Button(self.root, text="Retrieve Password", command=self.retrieve_password)
        self.retrieve_button.pack(pady=10)

    def add_password(self):
        account = simpledialog.askstring("Account", "Enter account name:")
        password = simpledialog.askstring("Password", "Enter password:", show='*')
        if account and password:
            save_password(account, password, self.key)
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            messagebox.showwarning("Error", "Account name and password cannot be empty.")

    def retrieve_password(self):
        account = simpledialog.askstring("Account", "Enter account name:")
        if account:
            password = load_password(account, self.key)
            if password:
                messagebox.showinfo("Password", f"Password for {account}: {password}")
            else:
                messagebox.showwarning("Error", "No password found for this account.")
        else:
            messagebox.showwarning("Error", "Account name cannot be empty.")


if __name__ == "__main__":
    if not os.path.exists("secret.key"):
        generate_key()

    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()