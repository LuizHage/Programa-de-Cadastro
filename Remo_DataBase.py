# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:35:28 2022
@author: luiz_
"""

import sqlite3


def BD_criar_BancoDeDados():
    # Criar uma base de dados ou se conectar a uma pré-existente
    conn = sqlite3.connect('remo_data1.db')
    c = conn.cursor()
    # Criar tabela do BD
    c.execute("""CREATE TABLE alunos(
        nome_aluno text,
        data_nasc text,
        CPF integer,
        RG integer,
        sexo text,
        responsavel text,          
        endereco text,
        CEP integer,
        bairro text,
        telefone integer,
        socio integer,              
        modalidade text,
        idade text,
        horario_aula text,
        dias_aula text,
        professor text,             
        data_matricula text,
        bolsista integer,
        valor_matricula integer,
        valor_mensalidade integer,
        mensalidade_paga text,
        data_pagamento int
        )""")

    # Commit
    conn.commit()
    # Fechar
    conn.close()
    print("Banco de Dados criado com sucesso!!!")


def BD_criar_Logins():
    # Criar uma base de dados ou se conectar a uma pré-existente
    conn = sqlite3.connect('remo_data1.db')
    c = conn.cursor()
    # Criar tabela do BD
    c.execute("""CREATE TABLE logins(
        login text,
        senha text
        )""")

    # Commit
    conn.commit()
    # Fechar
    conn.close()
    print("Logins criados com sucesso!!!")


def BD_adicionando_logins():
    login = "Login"
    senha = 123456
    # Criar uma base de dados ou se conectar a uma pré-existente
    conn = sqlite3.connect('remo_data1.db')
    c = conn.cursor()
    # Criar tabela do BD
    c.execute(
        "INSERT INTO logins VALUES (:login, :senha)",
        {
            'login': str(login),
            'senha': str(senha)
        })

    # Commit
    conn.commit()
    # Fechar
    conn.close()
    print("Login e Senha criada com sucesso!!!")


BD_criar_BancoDeDados()
BD_criar_Logins()
BD_adicionando_logins()
