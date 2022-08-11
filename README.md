# Remo_app
Projeto para criar uma aplicação em Python com integração de banco de dados em PosgreSQL
***
## Arquivos
O projeto possui (atualmente) 4 arquivos em Python, sendo eles: Remo_Database, Remo_Login, Remo_Programa e Remo_Cadastro.

* Remo_Database

Cria um arquivo no formato "x.db" para armazanar os dados de cadastro dos novos alunos, login e senha e fazer o registro do usuários.

* Remo_Login

Login e senha base para entrar acessar o programa principal.

* Remo_Programa

Inicia o sistema

* Remo_Cadastro

Programa principal com o Remo_Login + atribuições do cadastro de novos alunos

## Sobre o Sistema
A aplicação está no seu estágio inicial e permite ao usuário:

* Criar um login e senha;

* Adicionar novos alunos ao arquivo "x.db";

* Modificar informações dos alunos registrados;

* Gerar recibos (apenas mensagem de texto) com as informações do aluno matriculado ou antigo;

* e criar um arquivo em excel com a movimentação financeira do dia.

## Próximos passos

* Fazer constantes melhorias ao sistema proposto (Retirada automática de alunos por falta de pagamento, situação do aluno sobre o pagamento(pago, pendente, atraso)
entre outros);

- [x] Colocar o sistema inicial no GitHub  

- [ ] Python + PosgreSQL

- [ ] Análise de Dados sobre os dados dos alunos registrados

- [ ] Gerar gráficos sobre esses dados e apresentá-los utilizando PowerBI
