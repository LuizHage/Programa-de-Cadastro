# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:45:10 2022
@author: luiz_
"""

from os import path
import sqlite3
import openpyxl

from datetime import datetime
from tkinter import messagebox


# Funções auxiliares dos programas principais
# ======================================================================================================================
# 1- Função para verificar se existe o arquivo com os dados do sistema
def file_exist(file_name):
    if path.isfile(file_name):
        return True
    else:
        return False


# 2- Função Data e Hora de Hoje
def data_hora():
    data_e_hora_atuais = datetime.now()
    data = data_e_hora_atuais.strftime('%d/%m/%Y')
    return data, data_e_hora_atuais.day, data_e_hora_atuais.month


# 3- Função que gera a folha de cálculo do financeiro
def bd_excel():
    """Cria uma planilha do Excel com base nos dados do BD de hoje"""
    # Mensagem para perguntar sobre gerar Excel
    resposta = messagebox.askquestion("Confirmar informações",
                                      "Um arquivo Excel sobre a movimentação financeira será gerado E O ANTIGO SERÁ "
                                      "APAGADO.\n"
                                      "Você confirma estas informações?")
    if resposta == 'yes':
        try:
            # Cria uma Planilha no Excel
            book = openpyxl.Workbook()
            # Cria uma página
            book.create_sheet('Financeiro')
            # Selecionar uma página
            fin_page = book['Financeiro']
            fin_page.append(['n°', 'NOME', 'TURMA', 'ATRASO', 'DIA', 'MÊS', 'MATRICULA', 'MENSALIDADE'])
            # --------------------------------------------------------------------------
            # Se conecta a base de dados pré-existente
            conn = sqlite3.connect('remo_data1.db')
            c = conn.cursor()
            # Função para retirar a data, dia e mês
            [data_hj, dia, mes] = data_hora()
            # Retira as informações do Banco de Dados
            c.execute(f"SELECT * FROM alunos WHERE data_pagamento = '{data_hj}'")
            informacoes = c.fetchall()
            i = 1
            for info in informacoes:
                # Escreve nas linhas do Excel n°, Aluno, Turma, Atraso, dia, mês, mat, mens
                aluno, turma, atraso, mat, mens = str(info[0]), str(info[12]) + '-' + str(info[13]), \
                                                  ' ', str(info[18]), str(info[19])
                fin_page.append([i, aluno + '-' + turma, atraso, dia, mes, mat, mens])
                i += 1
            # ------------------------------------------------------------------
            # Commit
            conn.commit()
            # Fechar
            conn.close()
            # Salva o Excel gerado
            book.save('Planilhas de Controle - Teste.xlsx')
            messagebox.showinfo("Processo Concluído", "Planilha do Excel gerado com sucesso!")
        # ----------------------------------------------------------------------
        except PermissionError:
            # Erro ao salvar/gerar o arquivo
            messagebox.showerror("Erro ao criar Excel", "Feche o arquivo Excel para criar o novo arquivo!!!")
    # --------------------------------------------------------------------------


# 4- Função para verificar se a informação na caixa de texto foi escrita corretamente
def VerificarTexto(var, dic, num_car, nome_var):
    verif = str(var).strip()
    # 0 — Verificação para nomes
    if dic == 0 and verif.translate(verif.maketrans({"'": None, '-': None, ',': None, '.': None, ' ': None})).isalpha():
        return True
    # 1 — Verificação para texto com dicionário
    elif dic == 1 and verif.translate(verif.maketrans({',': None, '.': None, ' ': None})).isalnum():
        return True
    # 2 — Verificação para data de nascimento
    elif dic == 2:
        try:
            formato_dmy = bool(datetime.strptime(var, "%d/%m/%Y"))
        except ValueError:
            formato_dmy = False
        # Dicionário para retirar da data
        retirar_dic3 = {' ': None, '-': None, '/': None}
        conversor = verif.maketrans(retirar_dic3)
        if verif.translate(conversor).isnumeric() and len(
                verif.translate(conversor)) == num_car and formato_dmy:
            return True
    # 3 — Verificação para número com dicionário
    elif dic == 3:
        retirar_dic2 = {'(': None, ')': None, '.': None, ' ': None, '-': None, '/': None}
        conversor = verif.maketrans(retirar_dic2)
        if type(num_car) == int and verif.translate(conversor).isnumeric() and \
                len(verif.translate(conversor)) == num_car:
            return True
        elif type(num_car) == list and verif.translate(conversor).isnumeric() and (
                num_car[0] <= len(verif.translate(conversor)) <= num_car[1]):
            return True
    # 4 — Verificação para número sem dicionário
    elif dic == 4 and verif.replace(" ", "").isnumeric():
        return True
    # 5 — Verificação para qualquer coisa
    elif dic == 5 and verif.replace(" ", "").isalnum():
        return True
    else:
        messagebox.showerror("Erro de entrada de dados",
                             f"{nome_var} não está no padrão certo!\n"
                             "Favor, revise esta caixa de texto.")
        return False

