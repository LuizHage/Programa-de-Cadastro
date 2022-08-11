# -*- coding: utf-8 -*-
"""
Created on Wed May 18 08:50:10 2022
@author: luiz_
"""

# Importar o TKinter
import sqlite3

from tkinter import W
from tkinter import messagebox
from tkinter import Tk, Entry, Label, Button


# ==============================================================================
# ==============================================================================
# Função para entrar no programa
def EntrarPrograma(login, senha):
    # Se conectar a uma pré-existente
    con = sqlite3.connect('remo_data1.db')
    # Cria um cursor (meio de modificar o db)
    q = con.cursor()
    q.execute("SELECT * FROM logins WHERE login = '{}'".format(login))
    informacoes = q.fetchone()
    if senha == informacoes[1]:
        print('Bem vindo ao programa do Clube de Natação!!!')

    else:
        messagebox.showerror("Erro de Login", "Usuário ou Senha não encontrados.")
    # ------------------------------------------------------------------------------------------------------------------
    # Commit
    con.commit()
    # Fechar
    con.close()


# ======================================================================================================================
# ======================================================================================================================
# Criando Classe do Login
class TelaLogin(Tk):
    def __init__(self):
        super().__init__()
        # --------------------------------------------------------------------------------------------------------------
        # Configuração da tela
        self.title('Login - Clube de Natação')
        # login.geometry("745x600")
        self.resizable(False, False)
        # --------------------------------------------------------------------------------------------------------------
        # Criando as partes essênciais de ‘login’
        Label(self, text="Login").grid(row=0, column=0, sticky=W, padx=10)
        self.login_entry = Entry(self)
        self.login_entry.grid(row=0, column=1, sticky=W, padx=10)

        Label(self, text="Senha").grid(row=1, column=0, sticky=W, padx=10)
        self.senha_entry = Entry(self, show="*")
        self.senha_entry.grid(row=1, column=1, sticky=W, padx=10)

        Button(self, text="Entrar", command=lambda: EntrarPrograma(self.login_entry.get(), self.senha_entry.get()
                                                                   )).grid(row=3, column=0, columnspan=2,
                                                                           sticky=W, padx=10)


# ======================================================================================================================
# ======================================================================================================================
#Main Loop do Programa
if __name__ == '__main__':
    # Chama a classe
    app = TelaLogin()
    # Main loop do Login
    app.mainloop()
# ======================================================================================================================
# ======================================================================================================================
