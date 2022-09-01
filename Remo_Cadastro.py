# -*- coding: utf-8 -*-
"""
Created on Wed May 18 08:50:10 2022
@author: luiz_
"""

import sqlite3
import openpyxl
from os import path
from datetime import datetime
from tkinter import IntVar, Checkbutton, W, E
from tkinter import LabelFrame, Toplevel
from tkinter import OptionMenu, StringVar, messagebox
from tkinter import Tk, Entry, Label, Button, END
from tkinter import ttk


# ======================================================================================================================
# ======================================================================================================================
# Função para verificar se existe o arquivo com os dados do sistema
def file_exist(file_name):
    if path.isfile(file_name):
        return True
    else:
        return False


class TelaLogin(Tk):
    def __init__(self):
        super().__init__()
        # --------------------------------------------------------------------------------------------------------------
        # Configuração da tela
        self.title('Login - Clube do Remo')
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

        Button(self, text="Entrar",
               command=lambda: self.func_entrar_programa(self.login_entry.get(), self.senha_entry.get()
                                                         )).grid(row=3, column=0, columnspan=2,
                                                                 sticky=W, padx=10)

    # ==============================================================================
    # ==============================================================================
    # Função para entrar no cadastro do sistema
    def func_entrar_programa(self, login, senha):
        # Se conectar a uma pré-existente
        if file_exist("remo_data1.db"):
            con = sqlite3.connect('remo_data1.db')
            # Cria um cursor (meio de modificar o db)
            q = con.cursor()
            q.execute("SELECT * FROM logins WHERE login = '{}'".format(login))
            informacoes = q.fetchone()
            try:
                if senha == informacoes[1]:
                    self.destroy()
                    # Chama a classe
                    app_Remo = RootPrograma()
                    # Main loop do Login
                    app_Remo.mainloop()
            except TypeError:
                messagebox.showerror("Erro de Login", "Usuário ou Senha não encontrados.")
            # ------------------------------------------------------------------------------------------------------------------
            # Commit
            con.commit()
            # Fechar
            con.close()
        else:
            messagebox.showerror("Erro aa iniciar", "O Arquivo remo_data1 não foi encontrado.")


# ======================================================================================================================
# ======================================================================================================================
# Funções à parte do sistema principal
# Função Data e Hora de Hoje
def data_hora():
    data_e_hora_atuais = datetime.now()
    data = data_e_hora_atuais.strftime('%d/%m/%Y')
    return data, data_e_hora_atuais.day, data_e_hora_atuais.month


# Função de Verificação das Pendências de pagamento
''' 
def pendencias(mes_ant):
    """
    No dia em que o mês virar, deve-se cobrar a mensalidade
    Pago --> Pendente
    Pendente --> Atraso 1
    Atraso 1 --> Atraso 2
    Atraso 2 --> Atraso 3 ==> Retirar o aluno do sistema.
    """
    (_, _, mes) = data_hora()
    if mes_ant != mes:
        # Conecta-se ao BD
        conn = sqlite3.connect('remo_data1.db')
        c = conn.cursor()
        # Retira as informações do Banco de Dados
        c.execute("SELECT * FROM alunos WHERE data_pagamento = '{}'".format(data_hj))
        informacoes = c.fetchall()
        for info in informacoes:

            fin_page.append([i, str(info[0]), str(info[12]) + '-' + str(info[13]), ' ', dia,
                             mes, str(info[18]), str(info[19])])
        # ------------------------------------------------------------------
        # Commit
        conn.commit()
        # Fechar
        conn.close()
'''


# pendencias()


# ======================================================================================================================
# Função que gera a folha de cálculo do financeiro
def bd_excel():
    """Cria uma planilha do Excel com base nos dados do BD de hoje"""
    # Mensagem para perguntar sobre gerar Excel
    resposta = messagebox.askquestion("Confirmar informações",
                                      "Um arquivo Excel sobre a movimentação financeira será gerado E O ANTIGO SERÁ "
                                      "APAGADO.\n Você confirma estas informações?")
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
            # Se conecta ao BD
            conn = sqlite3.connect('remo_data1.db')
            c = conn.cursor()
            # Função para retirar a data, dia e mês
            [data_hj, dia, mes] = data_hora()
            # Retira as informações do Banco de Dados
            c.execute("SELECT * FROM alunos WHERE data_pagamento = '{}'".format(data_hj))
            informacoes = c.fetchall()
            i = 1
            for info in informacoes:
                # Escreve nas linhas do Excel n°, Aluno, Turma, Atraso, dia, mês, mat, mens
                fin_page.append([i, str(info[0]), str(info[12]) + '-' + str(info[13]), ' ', dia,
                                 mes, str(info[18]), str(info[19])])
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
        except:
            # Erro ao salvar/gerar o arquivo
            messagebox.showerror("Erro ao criar Excel", "Feche o arquivo Excel para criar o novo arquivo!!!")
    # --------------------------------------------------------------------------


# ==============================================================================
# Função para modificar as informações do aluno
def modificar_info(aluno, data_nasc, cpf, rg, sexo, responsavel, endereco, cep, bairro, telefone, socio,
                   modalidade, faixa, hora, dias_aula,
                   professor, bolsista, valor_matricula, valor_mensalidade, mensalidade_paga):
    # Se tem responsável ou não
    if responsavel == "Sem Responsável":
        resp = 0
    else:
        resp = 1

    # Como o aluno já foi matriculado, matrícula = 0.
    # Porém, se a modificação for feita no mesmo dia da matrícula, deve constar o valor da matrícula
    mat = 1

    # Chamando a classe Aluno
    aluno_modificado = Aluno(aluno, data_nasc, cpf, rg, sexo, resp, responsavel,
                             endereco, bairro, cep, telefone, socio, mat,
                             modalidade, faixa, hora, dias_aula, professor, bolsista,
                             valor_matricula, valor_mensalidade)
    # Verificando as informações
    if aluno_modificado.verificacao():
        # Criar uma base de dados ou se conectar a uma pré-existente
        conn = sqlite3.connect('remo_data1.db')
        c = conn.cursor()
        c.execute('''UPDATE alunos SET
                      nome_aluno = :nome, 
                      data_nasc = :data,
                      RG = :rg,
                      sexo = :sexo,
                      responsavel = :responsavel, 
                      endereco = :endereco, 
                      CEP = :cep, 
                      bairro = :bairro, 
                      telefone = :telefone,
                      socio = :socio,
                      modalidade = :mod,
                      idade = :idade,
                      horario_aula = :horario,
                      dias_aula = :dias_aula,
                      professor = :professor,
                      bolsista = :bolsista,
                      valor_matricula = :valor_matricula,
                      valor_mensalidade = :valor_mensalidade,
                      mensalidade_paga = :mensalidade_paga

                      WHERE CPF = :cpf''',
                  {
                      'nome': str(aluno),
                      'data': str(data_nasc),
                      'rg': int(rg),
                      'sexo': sexo,
                      'responsavel': responsavel,
                      'endereco': endereco,
                      'cep': int(cep),
                      'bairro': bairro,
                      'telefone': int(telefone),
                      'socio': int(socio),
                      'mod': modalidade,
                      'idade': faixa,
                      'horario': hora,
                      'dias_aula': dias_aula,
                      'professor': professor,
                      'bolsista': bolsista,
                      'valor_matricula': int(valor_matricula),
                      'valor_mensalidade': int(valor_mensalidade),
                      'mensalidade_paga': mensalidade_paga,
                      'cpf': cpf
                  })
        # Commit
        conn.commit()
        # Fechar
        conn.close()
        messagebox.showinfo("Processo concuído", "Informações modificadas com sucesso!")
        infos.destroy()


# ==============================================================================
# ==============================================================================
# Criando Classe da página inicial do programa
class RootPrograma(Tk):
    def __init__(self):
        super().__init__()
        # --------------------------------------------------------------------------------------------------------------
        # Configuração da tela
        self.title('Cadastro - Clube do Remo (versão beta)')
        self.geometry("745x600")
        self.resizable(False, True)
        # Criar uma base de dados ou se conectar a uma pré-existente
        self.conn = sqlite3.connect('remo_data1.db')
        # Cria um cursor(meio de modificar o db)
        self.c = self.conn.cursor()
        # ==============================================================================
        # Criando o frame da área da matricula
        self.frame_inicial = LabelFrame(self, text="Mensalidade dos Alunos", padx=10, pady=10)
        self.frame_inicial.grid(padx=10, pady=10)

        # Criando o frames diferentes
        self.frame1 = LabelFrame(self.frame_inicial, text="Informações do Aluno", padx=10, pady=10)
        self.frame1.grid(padx=10, pady=10, row=1, column=0)

        self.frame2 = LabelFrame(self.frame_inicial, text="Informações da Aula", padx=10, pady=10)
        self.frame2.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        # ==============================================================================
        # ==============================================================================
        # Cadastro ou Mensalidade
        # Frame 0
        Label(self.frame_inicial, text="Aluno já cadastrado?").grid(row=0, column=0, sticky=W)
        self.mat = IntVar()
        self.m = Checkbutton(self.frame_inicial, text="Sim", variable=self.mat, command=self.func_cadastro_anterior)
        self.m.grid(row=0, column=0, sticky=W, padx=118)
        # Entry começa desabilitado e depois habilita
        self.pesquisa = Entry(self.frame_inicial, width=30)
        self.pesquisa.grid(row=0, column=0, sticky=W, padx=183)
        self.pesquisa.insert(0, "Digite o número de CPF")
        self.pesquisa.configure(state='disabled')
        # ==============================================================================
        # Entrada de dados
        # Frame 1
        Label(self.frame1, text="Nome do Aluno").grid(row=0, column=0, sticky=W)
        self.nome_aluno = Entry(self.frame1, width=50)  # 70
        self.nome_aluno.grid(row=0, column=1, sticky=W, padx=10, pady=5)
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="CPF").grid(row=1, column=0, sticky=W)
        self.cpf = Entry(self.frame1)
        self.cpf.grid(row=1, column=1, sticky=W, padx=10, pady=5)
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="RG").grid(row=1, column=1, sticky=W, padx=150, columnspan=2)
        self.rg = Entry(self.frame1)
        self.rg.grid(row=1, column=1, sticky=W, padx=190, pady=5, columnspan=3)
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="Responsável").grid(row=2, column=0, sticky=W)
        # Entry começa desabilitado e depois habilita
        self.responsavel = Entry(self.frame1, width=40, state='disabled')
        self.responsavel.grid(row=2, column=1, sticky=W, padx=70, pady=5, columnspan=2)
        self.resp = IntVar()
        self.r = Checkbutton(self.frame1, text="Sim", variable=self.resp, command=self.caixa_responsavel)
        self.r.grid(row=2, column=1, sticky=W, padx=5)
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="Endereço").grid(row=3, column=0, sticky=W)
        self.endereco = Entry(self.frame1, width=50)
        self.endereco.grid(row=3, column=1, sticky=W, padx=10, pady=5)  # columnspan=2,
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="CEP").grid(row=4, column=0, sticky=W)
        self.cep = Entry(self.frame1)
        self.cep.grid(row=4, column=1, sticky=W, padx=10, pady=5)
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="Telefone").grid(row=5, column=0, sticky=W)
        self.fone = Entry(self.frame1)
        self.fone.grid(row=5, column=1, sticky=W, padx=10, pady=5)
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="Data de nascimento").grid(row=0, column=2, sticky=W)
        self.data_nasc = Entry(self.frame1)
        self.data_nasc.grid(row=0, column=3, sticky=W, padx=5, pady=5)
        # ------------------------------------------------------------------------------
        self.sexualidade_list = [
            " ",
            "Masculino",
            "Feminino"
        ]
        self.sexo = StringVar()
        self.sexo.set(self.sexualidade_list[0])
        Label(self.frame1, text="Sexo").grid(row=1, column=2, sticky=W)
        # Fazer combobox depois
        # sexo_drop = ttk.Combobox(frame1, textvariable=sexo)#, *sexualidade
        self.sexo_drop = OptionMenu(self.frame1, self.sexo, *self.sexualidade_list)  # ,
        self.sexo_drop.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        # ------------------------------------------------------------------------------
        Label(self.frame1, text="Bairro").grid(row=4, column=2, sticky=W)
        self.bairro = Entry(self.frame1)
        self.bairro.grid(row=4, column=3, sticky=W, padx=5, pady=5)
        # ------------------------------------------------------------------------------
        # Sócio
        Label(self.frame1, text="Sócio").grid(row=5, column=2, sticky=W)
        self.social = IntVar()
        self.s = Checkbutton(self.frame1, text="Sim", variable=self.social)
        self.s.grid(row=5, column=3, sticky=W, padx=5)
        # ==============================================================================
        # Frame 2
        # Modalidades
        self.modalidades_dic = {
            'vazio': " ",
            'natação': "Natação",
            'hidro': "Hidroginástica",
            'polo': "Polo Aquático"
        }
        self.mod = StringVar()
        self.mod.set(self.modalidades_dic["vazio"])
        # Label e Menu de Opções de Modalidades
        Label(self.frame2, text="Modalidade").grid(row=0, column=0, sticky=W)
        self.mod_drop = OptionMenu(self.frame2, self.mod, *self.modalidades_dic.values())
        self.mod_drop.grid(row=0, column=1, sticky=W, padx=5)

        # Idades
        self.idades_dic = {
            'vazio': " ",
            'baby': "Gorro Branco",
            'amarelo': "Gorro Amarelo",
            'laranja': "Gorro Laranja",
            'verde': "Gorro Verde",
            'vermelho': "Gorro Vermelho",
            'infanto': "Infanto",
            'adulto': "Adulto"
        }
        self.idade = StringVar()
        self.idade.set(self.idades_dic["vazio"])
        # Label e Menu de Opções de Idade
        Label(self.frame2, text="Faixa Etária").grid(row=0, column=3, sticky=W)
        self.idade_drop = OptionMenu(self.frame2, self.idade, *self.idades_dic.values())
        self.idade_drop.grid(row=0, column=4, sticky=W, padx=5)
        # ==============================================================================
        # Segunda parte
        # Horarios
        self.horarios_dic = {
            'vazio': ' ',
            'hidro': "8:00",
            'polo': "8:00",
            'baby': "8:20",
            'natacao_infantil': ["9:00", "9:40", "10:20",
                                 "14:00", "14:40", "15:20", "16:00", "16:40", "17:20"],
            'natacao_infanto': ["8:00", "16:00", "18:00"],
            'natacao_adulto': [
                # Manhã
                "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00",
                # Tarde
                "14:00", "15:00", "18:00", "19:00", "20:00"]
        }
        self.horario = StringVar()
        self.horario.set(self.horarios_dic["vazio"])

        # Label e Menu de Opções de Horários
        Label(self.frame2, text="Horário das Aulas").grid(row=1, column=0, sticky=W)
        self.horario_aula_drop = OptionMenu(self.frame2, self.horario, self.horarios_dic["vazio"])
        self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
        self.horario_aula_drop.configure(state='disabled')

        # Dias das Aulas
        self.dias_aulas_list = [" ",
                                "2ª, 4ª e 6ª",
                                "3ª, 4ª e 6ª",
                                "3ª e 5ª",
                                "4ª e 6ª",
                                "Sábado"]
        self.dias_aulas_dic = {
            'vazio': self.dias_aulas_list[0],
            'hidro': self.dias_aulas_list[2:4],
            'polo': self.dias_aulas_list[4:6],
            'baby': self.dias_aulas_list[3:5],
            'natacao_infantil': self.dias_aulas_list[1:5],
            'natacao_infanto': [self.dias_aulas_list[1], self.dias_aulas_list[3]],
            'natacao_adulto': self.dias_aulas_list[1:4]
        }
        self.dia = StringVar()
        self.dia.set(self.dias_aulas_dic["vazio"])

        # Label e Menu de Opções de Dias de Aulas
        Label(self.frame2, text="Dias das Aulas").grid(row=1, column=3, sticky=W)
        self.dia_aula_drop = OptionMenu(self.frame2, self.dia, self.dias_aulas_dic["vazio"])
        self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)
        self.dia_aula_drop.configure(state='disabled')

        # Label Valor da Mensalidade
        Label(self.frame2, text="Valor da Mensalidade").grid(row=2, column=0, sticky=W, pady=2)
        self.mensalidade = Entry(self.frame2)
        self.mensalidade.grid(row=2, column=1, sticky=W, padx=7, columnspan=2, pady=2)

        # Label Valor da Matrícula
        Label(self.frame2, text="Valor da Matrícula").grid(row=2, column=3, sticky=W, pady=2)
        self.matricula = Entry(self.frame2)
        self.matricula.grid(row=2, column=4, sticky=W, padx=7, columnspan=2, pady=2)

        # Label Professor
        Label(self.frame2, text="Nome do Professor").grid(row=3, column=0, sticky=W, pady=2)
        self.professor = Entry(self.frame2)
        self.professor.grid(row=3, column=1, sticky=W, padx=7, columnspan=2, pady=2)

        # Label Bolsista
        Label(self.frame2, text="Bolsista").grid(row=3, column=3, sticky=W, pady=2)
        self.bolsista = IntVar()
        self.b = Checkbutton(self.frame2, text="Sim", variable=self.bolsista, command=self.caixa_bolsista)
        self.b.grid(row=3, column=4, sticky=W, padx=7, columnspan=2, pady=2)

        # ------------------------------------------------------------------------------
        Button(self.frame2, text="Confirmar", command=self.mod_idade).grid(row=0, column=6)
        # ==============================================================================
        # Pós-framas
        Button(self.frame_inicial, text="Verificar Informações",
               command=self.confirmacao_final).grid(row=3, column=0, sticky=W, padx=10)
        # ------------------------------------------------------------------------------
        Button(self.frame_inicial, text='Limpar', command=self.comando_limpar).grid(row=3, column=0, sticky=E)
        # ------------------------------------------------------------------------------
        Button(self, text="Gerar Excel do dia", command=bd_excel).grid(row=2, column=0, pady=(30, 0))

    # ==================================================================================================================
    # ==================================================================================================================
    # Funções gerais do Programa
    # 1- Limpar todas as caixas de texto
    def func_limpar_texto(self):
        # Limpa as caixas de texto
        self.nome_aluno.delete(0, END)
        self.data_nasc.delete(0, END)
        self.responsavel.delete(0, END)
        self.cpf.delete(0, END)
        self.rg.delete(0, END)
        # Retornar Responsável ao estado inicial
        self.responsavel.configure(state='disabled')
        self.endereco.delete(0, END)
        self.cep.delete(0, END)
        self.bairro.delete(0, END)
        self.fone.delete(0, END)
        self.professor.delete(0, END)
        self.mensalidade.delete(0, END)
        self.matricula.delete(0, END)

    # 2- Desabilitar todas as caixas de texto
    def func_desabilitar_texto(self):
        self.nome_aluno.configure(state='disabled')
        self.data_nasc.configure(state='disabled')
        self.sexo_drop.configure(state='disabled')
        self.responsavel.configure(state='disabled')
        self.cpf.configure(state='disabled')
        self.rg.configure(state='disabled')
        self.endereco.configure(state='disabled')
        self.cep.configure(state='disabled')
        self.bairro.configure(state='disabled')
        self.fone.configure(state='disabled')
        self.professor.configure(state='disabled')
        self.mensalidade.configure(state='disabled')
        self.matricula.configure(state='disabled')
        # desabilita as caixas de opção restantes ...
        self.mod_drop.configure(state='disabled')
        self.idade_drop.configure(state='disabled')
        # e as caixas de marcar e botões
        self.r.configure(state='disabled')
        self.s.configure(state='disabled')
        self.b.configure(state='disabled')
        Button(self.frame2, text="Confirmar", state='disabled').grid(row=0, column=6)

    # 3- Habilitar todas as caixas de texto
    def func_habilitar_texto(self):
        # Habilita as outras caixas de texto
        self.nome_aluno.configure(state='normal')
        self.data_nasc.configure(state='normal')
        self.sexo_drop.configure(state='normal')
        self.endereco.configure(state='normal')
        self.cpf.configure(state='normal')
        self.rg.configure(state='normal')
        self.cep.configure(state='normal')
        self.bairro.configure(state='normal')
        self.fone.configure(state='normal')
        self.professor.configure(state='normal')
        self.mensalidade.configure(state='normal')
        self.matricula.configure(state='normal')
        self.mod_drop.configure(state='normal')
        self.idade_drop.configure(state='normal')
        self.r.configure(state='normal')
        self.s.configure(state='normal')
        self.b.configure(state='normal')
        # Retorna o valor da matrícula para o estado inicial
        self.pesquisa.delete(0, END)
        self.pesquisa.insert(0, "Digite o número de CPF")
        self.pesquisa.configure(state='disabled')
        # Reabilita o Botão de Contirmar Modalidade e Idade
        Button(self.frame2, text="Confirmar", command=self.mod_idade).grid(row=0, column=6)

    # 4- Marcar a caixa 'sim' em responsável
    def caixa_responsavel(self):
        # global responsavel
        if self.resp.get() == 1:
            self.responsavel.configure(state='normal')
        else:
            self.responsavel.delete(0, END)
            self.responsavel.configure(state='disabled')

    # 5- Marcar a caixa 'sim' em Mensalidade
    def func_cadastro_anterior(self):
        # global pesquisa
        var = self.mat.get()
        if var == 1:
            # Hebilitar a caixa de texto do valor de matrícula
            self.pesquisa.configure(state='normal')
            self.pesquisa.delete(0, END)
            # Limpa e desabilita as caixas de texto
            self.comando_limpar()
            self.func_desabilitar_texto()
            # Deixar selecionado o botão de Mensalidade
            self.m.select()
            self.pesquisa.configure(state='normal')
            self.pesquisa.delete(0, END)
        else:
            # Retomar a Caixa de matrícula para o estado inicial
            self.func_habilitar_texto()

    # 6- Marcar a caixa 'sim' em Bolsista
    def caixa_bolsista(self):
        # Ações do programa quando a caixa de bolsista for selecionada
        var = self.bolsista.get()
        if var == 1:
            # Limpa mensalidade, escreve 0 e desabilita
            self.mensalidade.delete(0, END)
            self.mensalidade.insert(0, '0')
            self.mensalidade.configure(state='disabled')
            # Limpa matrícula, escreve 0 e desabilita
            self.matricula.delete(0, END)
            self.matricula.insert(0, '0')
            self.matricula.configure(state='disabled')
        else:
            # Limpa mensalidade, escreve 0 e desabilita
            self.mensalidade.configure(state='normal')
            self.mensalidade.delete(0, END)
            # Limpa matrícula, escreve 0 e desabilita
            self.matricula.configure(state='normal')
            self.matricula.delete(0, END)

    # 7- Botão Limpar --> retornar os valores ao estado inicial
    def comando_limpar(self):
        # Descelecionar as caixas
        self.r.deselect()
        self.s.deselect()
        self.b.deselect()
        self.func_limpar_texto()
        # Caso Matrícula esteja selecionada
        if self.mat.get() == 1:
            # Habilitar texto e desselecionar a caixa
            self.func_habilitar_texto()
            self.m.deselect()
        # Colocar as caixas de Opção no estado inicial
        self.sexo.set(self.sexualidade_list[0])
        self.mod.set(self.modalidades_dic["vazio"])
        self.idade.set(self.idades_dic["vazio"])
        self.horario.set(self.horarios_dic["vazio"])
        self.dia.set(self.dias_aulas_dic["vazio"])

        # Horario_aula_drop volta a ser o placeholder (horario_aula_drop)
        self.horario_aula_drop = OptionMenu(self.frame2, self.horario, *self.horarios_dic["vazio"])
        self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
        self.horario_aula_drop.configure(state='disabled')

        self.dia_aula_drop = OptionMenu(self.frame2, self.dia, self.dias_aulas_dic["vazio"])
        self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)
        self.dia_aula_drop.configure(state='disabled')

    # ==============================================================================
    # Comandos de Botão do programa
    # 1- Confirmar Modalidade e Idade para gerar horários e dias
    def mod_idade(self):
        # Sumir os valores ou pegar a info de qual a tabela atual
        self.horario.set(self.horarios_dic["vazio"])
        self.dia.set(self.dias_aulas_dic["vazio"])

        if self.mod.get() == self.modalidades_dic["vazio"] or self.idade.get() == self.idades_dic["vazio"]:
            # Mensagem de erro
            messagebox.showerror("Erro na seleção", "Modalidade ou Idade não selecionados")
            # Retornar valores para vazio
            self.horario.set(self.horarios_dic["vazio"])
            self.dia.set(self.dias_aulas_dic["vazio"])

            # Desabilitar Horario e Dia
            self.horario_aula_drop = OptionMenu(self.frame2, self.horario, self.horarios_dic["vazio"])
            self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
            self.horario_aula_drop.configure(state='disabled')

            self.dia_aula_drop = OptionMenu(self.frame2, self.dia, self.dias_aulas_dic["vazio"])
            self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)
            self.dia_aula_drop.configure(state='disabled')
        else:
            if self.mod.get() == self.modalidades_dic["natação"]:
                # Natação
                if self.idade.get() == self.idades_dic["baby"]:  # Baby/Gorro Branco
                    # Horário
                    self.horario.set(self.horarios_dic["baby"])
                    self.horario_aula_drop = OptionMenu(self.frame2, self.horario, self.horarios_dic["baby"])
                    self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                    # Dias das aulas
                    self.dia.set(self.dias_aulas_dic["baby"][0])
                    self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *self.dias_aulas_dic["baby"])
                    self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

                elif self.idade.get() == self.idades_dic["amarelo"]:  # Amarelo
                    # Horário
                    self.horario.set(self.horarios_dic["natacao_infantil"][0])
                    self.horario_aula_drop = OptionMenu(self.frame2, self.horario,
                                                        *self.horarios_dic["natacao_infantil"])
                    self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                    # Dias das aulas
                    self.dia.set(self.dias_aulas_dic["natacao_infantil"][0])
                    self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *self.dias_aulas_dic["natacao_infantil"])
                    self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

                elif self.idade.get() == self.idades_dic["laranja"]:  # Infantil 5~11 Laranja
                    # Horário
                    self.horario.set(self.horarios_dic["natacao_infantil"][0])
                    self.horario_aula_drop = OptionMenu(self.frame2, self.horario,
                                                        *self.horarios_dic["natacao_infantil"])
                    self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                    # Dias das aulas
                    dias_aulas_inf = self.dias_aulas_dic["natacao_infantil"]
                    self.dia.set(dias_aulas_inf[0])
                    self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *dias_aulas_inf)
                    self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

                elif self.idade.get() == self.idades_dic["verde"]:  # Infantil 5~11 Verde
                    # Horário
                    self.horario.set(self.horarios_dic["natacao_infantil"][0])
                    self.horario_aula_drop = OptionMenu(self.frame2, self.horario,
                                                        *self.horarios_dic["natacao_infantil"])
                    self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                    # Dias das aulas
                    dias_aulas_inf = self.dias_aulas_dic["natacao_infantil"]
                    self.dia.set(dias_aulas_inf[0])
                    self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *dias_aulas_inf)
                    self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

                elif self.idade.get() == self.idades_dic["vermelho"]:  # Infantil 5~11 Vermelho
                    # Horário
                    self.horario.set(self.horarios_dic["natacao_infantil"][0])
                    self.horario_aula_drop = OptionMenu(self.frame2, self.horario,
                                                        *self.horarios_dic["natacao_infantil"])
                    self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                    # Dias das aulas
                    dias_aulas_inf = self.dias_aulas_dic["natacao_infantil"]
                    self.dia.set(dias_aulas_inf[0])
                    self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *dias_aulas_inf)
                    self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

                elif self.idade.get() == self.idades_dic["infanto"]:  # Infanto 12~18
                    # Horário
                    self.horario.set(self.horarios_dic["natacao_infanto"][0])
                    self.horario_aula_drop = OptionMenu(self.frame2, self.horario,
                                                        *self.horarios_dic["natacao_infanto"])
                    self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                    # Dias das aulas
                    dias_aulas_infanto = self.dias_aulas_dic["natacao_infanto"]
                    self.dia.set(dias_aulas_infanto[0])
                    self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *dias_aulas_infanto)
                    self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

                elif self.idade.get() == self.idades_dic["adulto"]:  # Adulto 18+
                    # Horário
                    self.horario.set(self.horarios_dic["natacao_adulto"][0])
                    self.horario_aula_drop = OptionMenu(self.frame2, self.horario, *self.horarios_dic["natacao_adulto"])
                    self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                    # Dias das aulas
                    dias_aulas_adt = self.dias_aulas_dic["natacao_adulto"]
                    self.dia.set(dias_aulas_adt[0])
                    self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *dias_aulas_adt)
                    self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

            elif self.mod.get() == self.modalidades_dic["hidro"]:
                # Hidroginástica
                # Horário
                self.horario.set(self.horarios_dic["hidro"])
                self.horario_aula_drop = OptionMenu(self.frame2, self.horario, self.horarios_dic["hidro"])
                self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                # Dias das aulas
                dias_aulas_hidro = self.dias_aulas_dic["hidro"]
                self.dia.set(dias_aulas_hidro[0])
                self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *dias_aulas_hidro)
                self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)

            elif self.mod.get() == self.modalidades_dic["polo"]:
                # Polo-aquático
                # Horário
                self.horario.set(self.horarios_dic["polo"])
                self.horario_aula_drop = OptionMenu(self.frame2, self.horario, self.horarios_dic["polo"])
                self.horario_aula_drop.grid(row=1, column=1, sticky=W, padx=5)
                # Dias das aulas
                dias_aulas_polo = self.dias_aulas_dic["polo"]
                self.dia.set(dias_aulas_polo[0])
                self.dia_aula_drop = OptionMenu(self.frame2, self.dia, *dias_aulas_polo)
                self.dia_aula_drop.grid(row=1, column=4, sticky=W, padx=5)
        # Sinalizador aqui, nesta identação

    # 2- Botão de Confirmar os dados no final do Programa
    def confirmacao_final(self):
        if self.mat.get() == 1:
            # Criando uma segunda janela para mostrar os dados do aluno cadastrado
            global infos, aluno_matriculado
            infos = Toplevel()
            infos.title('Informações do Aluno')

            # create a notebook
            notebook = ttk.Notebook(infos)
            notebook.pack(pady=15)

            # create frames
            frame_infos = ttk.Frame(notebook, width=400, height=280)
            frame_mod = ttk.Frame(notebook, width=400, height=280)

            frame_infos.pack(fill='both', expand=True)
            frame_mod.pack(fill='both', expand=True)

            # add frames to notebook
            notebook.add(frame_infos, text='Informações Gerais')
            notebook.add(frame_mod, text='Modificar Informações')

            # --------------------------------------------------------------------------------------------------------------
            # Informações gerais de matrícula
            Label(frame_infos, text="Nome do Aluno:").grid(row=0, column=0, sticky=E)
            Label(frame_infos, text="Data de nascimento:").grid(row=1, column=0, sticky=E)
            Label(frame_infos, text="CPF:").grid(row=2, column=0, sticky=E)
            Label(frame_infos, text="RG:").grid(row=3, column=0, sticky=E)
            Label(frame_infos, text="Sexo:").grid(row=4, column=0, sticky=E)
            Label(frame_infos, text="Responsável:").grid(row=5, column=0, sticky=E)
            Label(frame_infos, text="Endereço:").grid(row=6, column=0, sticky=E)
            Label(frame_infos, text="CEP:").grid(row=7, column=0, sticky=E)
            Label(frame_infos, text="Bairro:").grid(row=8, column=0, sticky=E)
            Label(frame_infos, text="Telefone:").grid(row=9, column=0, sticky=E)
            Label(frame_infos, text="Sócio:").grid(row=10, column=0, sticky=E)

            # --------------------------------------------------------------------------------------------------------------
            # Informações da aula
            Label(frame_infos, text="\t Modalidade:").grid(row=11, column=0, sticky=E)
            Label(frame_infos, text="Faixa Etária:").grid(row=12, column=0, sticky=E)
            Label(frame_infos, text="Horário das Aulas:").grid(row=13, column=0, sticky=E)
            Label(frame_infos, text="Dias das Aulas:").grid(row=14, column=0, sticky=E)
            Label(frame_infos, text="Professor:").grid(row=15, column=0, sticky=E)
            Label(frame_infos, text="Bolsista:").grid(row=16, column=0, sticky=E)
            Label(frame_infos, text="Valor da Mensalidade:").grid(row=17, column=0, sticky=E)
            Label(frame_infos, text="Mensalidade paga?").grid(row=18, column=0, sticky=E)

            # Criar uma base de dados ou se conectar a uma pré-existente
            conn = sqlite3.connect('remo_data1.db')
            c = conn.cursor()
            # Pesquisar os dados no BD
            c.execute("SELECT * FROM alunos WHERE CPF = " + self.pesquisa.get())
            # Pegar todas as infos
            informacoes = c.fetchall()
            cpf_num = ''
            for info in informacoes:
                # Informações do aluno
                Label(frame_infos, text=info[0]).grid(row=0, column=1, sticky=W)
                Label(frame_infos, text=info[1]).grid(row=1, column=1, sticky=W)
                cpf_num = info[2]
                while len(str(cpf_num)) < 11:
                    cpf_num = '0' + str(cpf_num)
                Label(frame_infos, text=cpf_num).grid(row=2, column=1, sticky=W)
                Label(frame_infos, text=info[3]).grid(row=3, column=1, sticky=W)
                Label(frame_infos, text=info[4]).grid(row=4, column=1, sticky=W)
                Label(frame_infos, text=info[5]).grid(row=5, column=1, sticky=W)
                Label(frame_infos, text=info[6]).grid(row=6, column=1, sticky=W)
                Label(frame_infos, text=info[7]).grid(row=7, column=1, sticky=W)
                Label(frame_infos, text=info[8]).grid(row=8, column=1, sticky=W)
                Label(frame_infos, text=info[9]).grid(row=9, column=1, sticky=W)
                # Sócio (0/1)
                Label(frame_infos, text=info[10]).grid(row=10, column=1, sticky=W)
                # Aulas
                Label(frame_infos, text=info[11]).grid(row=11, column=1, sticky=W)
                Label(frame_infos, text=info[12]).grid(row=12, column=1, sticky=W)
                Label(frame_infos, text=info[13]).grid(row=13, column=1, sticky=W)
                Label(frame_infos, text=info[14]).grid(row=14, column=1, sticky=W)
                Label(frame_infos, text=info[15]).grid(row=15, column=1, sticky=W)
                Label(frame_infos, text=info[17]).grid(row=16, column=1, sticky=W)
                Label(frame_infos, text=info[19]).grid(row=17, column=1, sticky=W)
                Label(frame_infos, text=info[20]).grid(row=18, column=1, sticky=W)
                # ----------------------------------------------------------------------------------------------------------
                aluno_matriculado = Aluno(info[0], info[1], info[2], info[3], info[4], 1, info[5], info[6], info[8],
                                          info[7], info[9], info[10], 1, info[11], info[12], info[13], info[14],
                                          info[15], info[17], 0, info[19])
            # Commit
            conn.commit()
            # Fechar
            conn.close()
            # --------------------------------------------------------------------------------------------------------------
            Button(frame_infos, text='Gerar Recibo', command=aluno_matriculado.recibo).grid(row=19, column=0, padx=10,
                                                                                            pady=10, sticky=W,
                                                                                            columnspan=2)
            # --------------------------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------------------------
            # Frame - Modificar Informações
            Label(frame_mod, text="Nome do Aluno:").grid(row=0, column=0, sticky=E)
            Label(frame_mod, text="Data de nascimento:").grid(row=1, column=0, sticky=E)
            Label(frame_mod, text="CPF:").grid(row=2, column=0, sticky=E)
            Label(frame_mod, text="RG:").grid(row=3, column=0, sticky=E)
            Label(frame_mod, text="Sexo:").grid(row=4, column=0, sticky=E)
            Label(frame_mod, text="Responsável:").grid(row=5, column=0, sticky=E)
            Label(frame_mod, text="Endereço:").grid(row=6, column=0, sticky=E)
            Label(frame_mod, text="CEP:").grid(row=7, column=0, sticky=E)
            Label(frame_mod, text="Bairro:").grid(row=8, column=0, sticky=E)
            Label(frame_mod, text="Telefone:").grid(row=9, column=0, sticky=E)
            Label(frame_mod, text="Sócio:").grid(row=10, column=0, sticky=E)

            # --------------------------------------------------------------------------------------------------------------
            # Informações da aula
            Label(frame_mod, text="\t Modalidade:").grid(row=11, column=0, sticky=E)
            Label(frame_mod, text="Faixa Etária:").grid(row=12, column=0, sticky=E)
            Label(frame_mod, text="Horário das Aulas:").grid(row=13, column=0, sticky=E)
            Label(frame_mod, text="Dias das Aulas:").grid(row=14, column=0, sticky=E)
            Label(frame_mod, text="Professor:").grid(row=15, column=0, sticky=E)
            Label(frame_mod, text="Bolsista:").grid(row=16, column=0, sticky=E)
            Label(frame_mod, text="Valor da Mensalidade:").grid(row=17, column=0, sticky=E)
            Label(frame_mod, text="Mensalidade paga?").grid(row=18, column=0, sticky=E)

            nome_aluno_editor = Entry(frame_mod)
            nome_aluno_editor.grid(row=0, column=1, sticky=W)
            data_nasc_editor = Entry(frame_mod)
            data_nasc_editor.grid(row=1, column=1, sticky=W)
            rg_editor = Entry(frame_mod)
            rg_editor.grid(row=3, column=1, sticky=W)
            sexo_editor = Entry(frame_mod)
            sexo_editor.grid(row=4, column=1, sticky=W)
            responsavel_editor = Entry(frame_mod)
            responsavel_editor.grid(row=5, column=1, sticky=W)
            endereco_editor = Entry(frame_mod)
            endereco_editor.grid(row=6, column=1, sticky=W)
            cep_editor = Entry(frame_mod)
            cep_editor.grid(row=7, column=1, sticky=W)
            bairro_editor = Entry(frame_mod)
            bairro_editor.grid(row=8, column=1, sticky=W)
            fone_editor = Entry(frame_mod)
            fone_editor.grid(row=9, column=1, sticky=W)
            socio_editor = Entry(frame_mod)
            socio_editor.grid(row=10, column=1, sticky=W)

            modalidade_editor = Entry(frame_mod)
            modalidade_editor.grid(row=11, column=1, sticky=W)
            faixa_editor = Entry(frame_mod)
            faixa_editor.grid(row=12, column=1, sticky=W)
            horario_editor = Entry(frame_mod)
            horario_editor.grid(row=13, column=1, sticky=W)
            dia_editor = Entry(frame_mod)
            dia_editor.grid(row=14, column=1, sticky=W)

            professor_editor = Entry(frame_mod)
            professor_editor.grid(row=15, column=1, sticky=W)
            bolsa_editor = Entry(frame_mod)
            bolsa_editor.grid(row=16, column=1, sticky=W)
            valor_editor = Entry(frame_mod)
            valor_editor.grid(row=17, column=1, sticky=W)
            mensalidadePaga_editor = Entry(frame_mod)
            mensalidadePaga_editor.grid(row=18, column=1, sticky=W)

            # Criar uma base de dados ou se conectar a uma pré-existente
            conn = sqlite3.connect('remo_data1.db')
            c = conn.cursor()
            # Pesquisar os dados no BD
            c.execute("SELECT * FROM alunos WHERE CPF = " + self.pesquisa.get())
            # Pegar todas as infos
            informacoes = c.fetchall()
            for info in informacoes:
                # Informações do aluno
                nome_aluno_editor.insert(0, info[0])
                data_nasc_editor.insert(0, info[1])
                Label(frame_mod, text=cpf_num).grid(row=2, column=1, sticky=W)
                rg_editor.insert(0, info[3])
                sexo_editor.insert(0, info[4])
                responsavel_editor.insert(0, info[5])
                endereco_editor.insert(0, info[6])
                cep_editor.insert(0, info[7])
                bairro_editor.insert(0, info[8])
                fone_editor.insert(0, info[9])
                # Sócio (0/1)
                socio_editor.insert(0, info[10])
                modalidade_editor.insert(0, info[11])
                faixa_editor.insert(0, info[12])
                horario_editor.insert(0, info[13])
                dia_editor.insert(0, info[14])
                professor_editor.insert(0, info[15])
                bolsa_editor.insert(0, info[17])
                valor_matricula = info[18]
                valor_editor.insert(0, info[19])
                mensalidadePaga_editor.insert(0, info[20])

            # Commit
            conn.commit()
            # Fechar
            conn.close()
            # --------------------------------------------------------------------------------------------------------------
            Button(frame_mod, text='Modificar',
                   command=lambda: modificar_info(nome_aluno_editor.get(), data_nasc_editor.get(),
                                                  self.pesquisa.get(),
                                                  rg_editor.get(), sexo_editor.get(), responsavel_editor.get(),
                                                  endereco_editor.get(), cep_editor.get(), bairro_editor.get(),
                                                  fone_editor.get(), socio_editor.get(), modalidade_editor.get(),
                                                  faixa_editor.get(), horario_editor.get(), dia_editor.get(),
                                                  professor_editor.get(), bolsa_editor.get(),
                                                  valor_matricula, valor_editor.get(),
                                                  mensalidadePaga_editor.get())).grid(row=19, column=0, padx=10,
                                                                                      pady=10,
                                                                                      sticky=W, columnspan=2)

        else:
            # horários de manhã
            manha = ["6:00", "7:00", "8:00", "9:00", "9:40", "10:00", "10:20", "11:00", "12:00", "13:00"]
            horario_manha = False
            # Verifica se é um horário matinal
            for hora in manha:
                if self.horario.get() == hora:
                    horario_manha = True
                    break
            if self.horario.get() == self.horarios_dic["vazio"] or self.dia.get() == self.dias_aulas_dic["vazio"]:
                # Caso a Hora ou o Dia não estejam selecionados
                messagebox.showerror("Erro na seleção", "Horário ou Dia não selecionados")
            elif self.dia.get() == self.dias_aulas_list[1] and horario_manha:
                # Se for escolhido segunda num horário de manhã
                messagebox.showerror("Erro na seleção", "O horário da manhã é indisponível durante às segundas")
            else:
                # Caso os dois estejam selecionados
                resposta = messagebox.askquestion("Confirmar informações", "O sistema pode verificar as informações?")
                if resposta == "yes":
                    # Atualizar a data para a atual
                    # modificar_data = 1
                    # Chama a classe Aluno
                    aluno_registrado = Aluno(self.nome_aluno.get(), self.data_nasc.get(), self.cpf.get(), self.rg.get(),
                                             self.sexo.get(), self.resp.get(), self.responsavel.get(),
                                             self.endereco.get(), self.bairro.get(), self.cep.get(), self.fone.get(),
                                             self.social.get(),
                                             self.mat.get(),
                                             self.mod.get(), self.idade.get(), self.horario.get(), self.dia.get(),
                                             self.professor.get(), self.bolsista.get(), self.matricula.get(),
                                             self.mensalidade.get())

                    # Envia os dados para a verificação e BD
                    aluno_registrado.enviar_dados()


# ==============================================================================
# 1- Classe Alunos
class Aluno:
    # Classe para verificar se os dados do aluno estão completos
    def __init__(self, aluno_str, data_nascimento, cpf_num, rg_num, sexo_str, resp_bol, responsavel_str,
                 endereco_str, bairro_str, cep_num, telefone_num, socio_bol, mat_bol,
                 mod_str, idade_str, horario_str, dia_aula_str, professor_str, bolsista_bol,
                 matricula_num, mensalidade_num):
        self.nome_aluno = aluno_str
        self.data_nasc = data_nascimento
        self.cpf = cpf_num
        self.rg = rg_num
        self.sexo = sexo_str
        self.resp = resp_bol
        self.responsavel = responsavel_str
        self.endereco = endereco_str
        self.bairro = bairro_str
        self.cep = cep_num
        self.fone = telefone_num
        self.socio = socio_bol
        self.mat = mat_bol
        self.mod = mod_str
        self.idade = idade_str
        self.horario = horario_str
        self.dias_das_aulas = dia_aula_str
        self.professor = professor_str
        self.bolsista = bolsista_bol
        self.valor_matricula = matricula_num
        self.valor_mensalidade = mensalidade_num

    # ==========================================================================
    def enviar_dados(self):
        """
        São 3 fases para enviar os dados
        1- Verificação dos dados
        2- Envio para o banco de dados
        3- Gerar o recibo
        """
        if Aluno.verificacao(self):
            if Aluno.bd_enviar_dados(self):
                Aluno.recibo(self)

    def verificacao(self):
        # --------------------------------------------------------------------------
        """
        Objetivo: Verificaçar das informações antes de enviar para o BD
        1- Verificar se as caixas de texte estão preenchidas
        com as informações corretas;
        2- Informar quais as caixas de texto com problemas, caso haja alguma;
        3- Envia as informações para o BD.
        """
        # --------------------------------------------------------------------------
        # 1-Verificação de textos
        # Verificação para o nome do aluno
        nome_aluno_verif = str(self.nome_aluno).strip()  # strip()
        # Verifica se o nome está com letra maiúscula em cada nome
        if nome_aluno_verif.istitle() and any(
                CHR.isdigit() for CHR in nome_aluno_verif) == False and nome_aluno_verif.replace(" ", "").isalpha():
            nome_aluno_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O Nome do Aluno não está no padrão certo!\n Favor, revise esta caixa de texto.")
            nome_aluno_verif = False
        # --------------------------------------------------------------------------
        # Verificação para o nome do responsável, caso tenha um
        if self.resp == 0:
            # Caso não tenha um responsável
            self.responsavel = "Sem Responsável"
            responsavel_verif = True
        else:
            # Caso tenha responsável,
            responsavel_verif = str(self.responsavel).strip()
            # Verifica se o nome está com letra maiúscula em cada nome, se possui números e se todos os caracteres
            # são alfabéticos
            if responsavel_verif.istitle() and any(
                    CHR.isdigit() for CHR in responsavel_verif) == False and responsavel_verif.replace(" ",
                                                                                                       "").isalpha():
                responsavel_verif = True
            else:
                messagebox.showerror("Erro de entrada de dados",
                                     "O Nome do Responsável não está no padrão certo!\n Favor, revise esta caixa de "
                                     "texto.")
                responsavel_verif = False
                # --------------------------------------------------------------------------
        # Verificação para o Professor
        professor_verif = str(self.professor).strip()  # strip()
        # Verifica se o nome está com letra maiúscula em cada nome
        if professor_verif.istitle() and any(
                CHR.isdigit() for CHR in professor_verif) == False and professor_verif.replace(" ", "").isalpha():
            professor_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O nome do PROFESSOR não está no padrão certo!\n Favor, revise esta caixa de texto.")
            professor_verif = False
        # Dicionário com os caracteres para retirar (endereço e bairro)
        retirar_dic1 = {',': None, '.': None, ' ': None}
        # Verificação do endereço
        endereco_verif = str(self.endereco).strip()
        conversor = endereco_verif.maketrans(retirar_dic1)
        if endereco_verif.translate(conversor).isalnum():
            endereco_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O Endereço não está no padrão certo!\n Favor, revise esta caixa de texto.")
            endereco_verif = False
        # Verificação do bairro
        bairro_verif = str(self.bairro).strip()
        conversor = bairro_verif.maketrans(retirar_dic1)
        if bairro_verif.translate(conversor).isalpha():
            bairro_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O Bairro não está no padrão certo!\n Favor, revise esta caixa de texto.")
            bairro_verif = False
        # --------------------------------------------------------------------------
        # 2-Verificação de variáveis numéricas
        # Dicionário com os caracteres para retirar (Todos os números)
        retirar_num_dic = {'(': None, ')': None, '.': None, ' ': None, '-': None, '/': None}
        # Verificação Data de Nascimento
        data_nasc_verif = str(self.data_nasc).strip()
        conversor = data_nasc_verif.maketrans(retirar_num_dic)
        if data_nasc_verif.translate(conversor).isnumeric() and len(data_nasc_verif.translate(conversor)) == 8:
            data_nasc_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "A Data de Nascimnto não está no padrão certo!\n Favor, revise esta caixa de texto.")
            data_nasc_verif = False
        # --------------------------------------------------------------------------
        # Verificação CPF
        cpf_verif = str(self.cpf).strip()
        conversor = cpf_verif.maketrans(retirar_num_dic)
        if cpf_verif.translate(conversor).isnumeric():
            cpf_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O CPF não está no padrão certo!\n Favor, revise esta caixa de texto.")
            cpf_verif = False
        # --------------------------------------------------------------------------
        # Verificação RG
        rg_verif = str(self.rg).strip()
        conversor = rg_verif.maketrans(retirar_num_dic)
        if rg_verif.translate(conversor).isnumeric() and len(rg_verif.translate(conversor)) == 7:
            rg_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O RG não está no padrão certo!\n Favor, revise esta caixa de texto.")
            rg_verif = False
        # --------------------------------------------------------------------------
        # Verificação do CEP
        cep_verif = str(self.cep).strip()
        conversor = cep_verif.maketrans(retirar_num_dic)
        if cep_verif.translate(conversor).isnumeric() and len(cep_verif.translate(conversor)) == 8:
            cep_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O CEP não está no padrão certo!\n Favor, revise esta caixa de texto.")
            cep_verif = False
        # --------------------------------------------------------------------------
        # Verificação do Telefone
        tel_verif = str(self.fone).strip()
        conversor = tel_verif.maketrans(retirar_num_dic)
        if tel_verif.translate(conversor).isnumeric() and len(tel_verif.translate(conversor)) == 11:
            tel_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O Telefone não está no padrão certo!\n Favor, revise esta caixa de texto.")
            tel_verif = False
        # --------------------------------------------------------------------------
        # Verificação de Mensalidade
        mensalidade_verif = str(self.valor_mensalidade).strip()
        conversor = mensalidade_verif.maketrans(retirar_num_dic)
        if mensalidade_verif.translate(conversor).isnumeric():
            mensalidade_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O valor da Mensalidade não está no padrão certo!\n Favor, revise esta caixa de texto.")
            mensalidade_verif = False
        # --------------------------------------------------------------------------
        # Verificação de Valor da matrícula
        matricula_verif = str(self.valor_matricula).strip()
        conversor = matricula_verif.maketrans(retirar_num_dic)
        if matricula_verif.translate(conversor).isnumeric():
            matricula_verif = True
        else:
            messagebox.showerror("Erro de entrada de dados",
                                 "O valor da Matrícula não está no padrão certo!\n Favor, revise esta caixa de texto.")
            matricula_verif = False
        # --------------------------------------------------------------------------
        # 3-Verificação das aulas (necessário para a modificação das infos)
        # Dicionário com os caracteres do clube
        # Modalidades
        modalidades_dic = {'natação': "Natação",
                           'hidro': "Hidroginástica",
                           'polo': "Polo Aquático"}

        modalidade_verif = False
        for k in modalidades_dic:
            if self.mod == modalidades_dic[k]:
                modalidade_verif = True
                break
        # --------------------------------------------------------------------------
        # Idades
        idades_dic = {'baby': "Gorro Branco", 'amarelo': "Gorro Amarelo",
                      'laranja': "Gorro Laranja", 'verde': "Gorro Verde", 'vermelho': "Gorro Vermelho",
                      'infanto': "Infanto", 'adulto': "Adulto"}

        idades_verif = False
        for k in idades_dic:
            if self.idade == idades_dic[k]:
                idades_verif = True
                break
        # --------------------------------------------------------------------------
        # Horário
        horarios_list = ["8:20", "9:40", "10:20", "14:40", "15:20", "16:40", "17:20",
                         "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00",
                         "13:00", "14:00", "15:00", "18:00", "19:00", "20:00"]
        horarios_verif = False
        for itens in horarios_list:
            if self.horario == itens:
                horarios_verif = True
                break
        # --------------------------------------------------------------------------
        # Dias das Aulas
        dias_aulas_list = ["2ª, 4ª e 6ª", "3ª, 4ª e 6ª",
                           "3ª e 5ª", "4ª e 6ª", "Sábado"]
        dias_aulas_verif = False
        for itens in dias_aulas_list:
            if self.dias_das_aulas == itens:
                dias_aulas_verif = True
                break
        # ======================================================================
        # Retorna True se todas as respostas foram positivas
        if all([nome_aluno_verif, responsavel_verif, professor_verif, cpf_verif, rg_verif, endereco_verif, bairro_verif,
                data_nasc_verif, cep_verif, tel_verif, mensalidade_verif, matricula_verif,
                modalidade_verif, idades_verif, horarios_verif, dias_aulas_verif]):
            # Confirma se as informações estão corretas
            resposta_verificacao = messagebox.askquestion("Confirmar informações",
                                                          "As informações deste aluno foram verificadas com "
                                                          "sucesso.\n Você confirma estas informações?")
            if resposta_verificacao == 'yes':
                return True
            else:
                messagebox.showinfo("Cancelamento de envio",
                                    "Informações CANCELADAS com sucesso.")
                return False

        else:
            messagebox.showerror("Erro na matrícula",
                                 "Algumas informações foram escritas fora do padrão.\n Favor, verificar as "
                                 "informações corretamente.")
            return False

    def bd_enviar_dados(self):
        """
        Enviando as informações para o BD
        Com as informações verificadas, o sistema busca as informações finais
        de professores e mensalidades para as aulas selecionadas
        """
        # Caso haja algum erro ao enviar os dados
        try:
            # Fórmula para pagar a mensalidade no final do sistema
            mensalidade_paga = 'Sim'

            # Data de Hoje para mostrar quando foi feito a matrícula
            [data_hj, _, _] = data_hora()

            # Caso seja a primeira matrícula
            if self.mat:
                # Atualiza a data de pagamento e a mensalidade paga
                conn = sqlite3.connect('remo_data1.db')
                c = conn.cursor()
                c.execute('''UPDATE alunos SET
                
                data_pagamento = :data_pgt,
                valor_matricula = :valor_matricula,
                mensalidade_paga = :mensalidade_paga
                
                WHERE CPF = :cpf''',
                          {
                              'data_pgt': data_hj,
                              'valor_matricula': int(self.valor_matricula),
                              'mensalidade_paga': mensalidade_paga,
                              'cpf': int(self.cpf)
                          })
                conn.commit()
                conn.close()
            else:
                # Se conecta ao BD pré-existente
                conn = sqlite3.connect('remo_data1.db')
                c = conn.cursor()

                # Inserir os dados na Tabela do BD
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

                # Commit
                conn.commit()
                # Fechar
                conn.close()
                messagebox.showinfo("Processo concuído", "Informações entregues com sucesso!")
                return True

        except:
            messagebox.showerror("Processo cancelado", "Ocorreu algum erro ao enviar as informações.")
            return False

    # ==========================================================================
    # ==========================================================================
    def recibo(self):
        # Caso o recibo gerado seja por um aluno antigo
        if self.mat:
            # Lógica para add pago = "sim" e data de pagamento = hj
            Aluno.bd_enviar_dados(self)

        # Retirar a data do pagamento
        [data_pagamento, _, _] = data_hora()
        # Caixa de texto para as informações do recibo
        recibo = Toplevel()
        recibo.title('Informações do Aluno')
        frame_recibo = LabelFrame(recibo, text="Informações para Recibo:", padx=10, pady=10)
        frame_recibo.grid(padx=10, pady=10, row=0, column=0)
        # Informações do aluno
        info_rec = ''
        info_rec += (
                "Valor: R$ {} \n".format(str(int(self.valor_mensalidade) + int(self.valor_matricula))) +
                "Aluno: {} \n".format(str(self.nome_aluno)) +
                "Professor: {} \n".format(str(self.professor)) +
                "Horário: {} \n".format(str(self.horario)) +
                "Dias: {} \n".format(str(self.dias_das_aulas)) +
                "Belém: {}".format(data_pagamento)
        )
        query_label = Label(frame_recibo, text=info_rec)
        query_label.grid(row=0, column=0)
        # ----------------------------------------------------------------------
        # Fechar página
        fechar_btn = Button(recibo, text="Fechar", command=recibo.destroy)
        fechar_btn.grid(row=1, column=0)

# ======================================================================================================================
# ======================================================================================================================
