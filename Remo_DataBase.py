# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:35:28 2022
@author: luiz_
"""

import sqlite3
from datetime import datetime
from os import path


def BD_file_existe():
    fileName = "remo_data1.db"
    if path.isfile(fileName):
        print("O arquivo de banco de dados está na pasta.")
        return True
    else:
        print("O arquivo de banco de dados não foi encontrado!!!")
        return False


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
        data_pagamento text
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
    login = "LuizHage"
    senha = "01001001010"
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


def BD_modificando_alunos():
    # Atualiza a data de pagamento e a mensalidade paga
    data_em_texto = '30/08/2022'
    data_hj = datetime.strptime(data_em_texto, '%d/%m/%Y')
    cpf = 130501219

    conn = sqlite3.connect('remo_data1.db')
    c = conn.cursor()
    c.execute('''UPDATE alunos SET data_pagamento = :data_pgt WHERE CPF = :cpf''',
              {
                  'data_pgt': data_hj,
                  'cpf': cpf
              })
    # Commit
    conn.commit()
    # Fechar
    conn.close()
    print("Informações modificadas com sucesso!")


def BD_adicionando_alunos():
    login = "Login"
    senha = 123456
    # Criar uma base de dados ou se conectar a uma pré-existente
    conn = sqlite3.connect('remo_data1.db')
    c = conn.cursor()

    '''
    # Criar tabela do BD
    c.execute(
        "INSERT INTO alunos VALUES (:nome_aluno, :data_nasc, :CPF, :RG, :sexo,:responsavel,:endereco,:CEP,"
        ":bairro,:telefone,:socio,:modalidade,:idade,:horario_aula,:dias_aula,:professor,"
        ":data_matricula,:bolsista,:valor_matricula,:valor_mensalidade,:mensalidade_paga,:data_pagamento)",
        {
            'nome_aluno': str(self.nome_aluno),
            'data_nasc': str(self.data_nasc),
            'CPF': str(self.cpf),
            'RG': int(self.rg),
            'sexo': str(self.sexo),
            'responsavel': str(self.responsavel),
            'endereco': str(self.endereco),
            'CEP': int(self.cep),
            'bairro': str(self.bairro),
            'telefone': int(self.fone),

            'socio': int(self.socio),
            'modalidade': str(self.mod),
            'idade': str(self.idade),
            'horario_aula': str(self.horario),
            'dias_aula': str(self.dias_das_aulas),
            'professor': str(self.professor),
            'data_matricula': data_hj,
            'bolsista': self.bolsista,
            'valor_matricula': int(self.valor_matricula),

            'valor_mensalidade': int(self.valor_mensalidade),
            'mensalidade_paga': mensalidade_paga,
            'data_pagamento': data_hj
            })
    '''

    # Commit
    conn.commit()
    # Fechar
    conn.close()
    print("Aluno criado com sucesso!!!")


# BD_file_existe()
# BD_criar_BancoDeDados()
# BD_criar_Logins()
BD_adicionando_logins()
# BD_modificando_alunos()
# BD_adicionando_alunos()

