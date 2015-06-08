# GDA Web App
#### Grupo de Avaliação Discente (GDA) da Faculdade de Engenharia Elétrica e de Computação (FEEC) da Universidade de Campinas (Unicamp)
Olá, conheça a página de desenvolvimento do GDA.

Estamos atualmente em fase de desenvolvimento, sendo assim, o conteúdo aqui disponível ainda não está disponibilizado para usuários. Porém se você quer participar do desenvolvimento ou acompanhar o andamento do nosso trabalho, leia o conteúdo desta página.

## 1. Especificação
Para o lançamento da versão Beta, este projeto deve possuir as seguintes funcionalidades:

 1. Ferramenta de coleta da avaliação de disciplinas por estudantes de maneira anônima
 2. Ferramentas para análise dos dados coletados
 3. Mural de informações para publicação das análises


## 2. Linhas de desenvolvimento
O projeto do GDA atualmente consta com algumas linhas principais de desenvolvimento:

 1. Elaboração dos formulários de avaliação
 2. Desenvolvimento de aplicações Web
 3. Planejamento de interfaces
 4. Relações públicas


## 3. Ferramentas e requisitos
Nesta versão de desenvolvimento contamos com as seguintes ferramentas:

* [Google Forms](https://docs.google.com/forms/d/1kVaQlGR9AQPtNVwuB56Hqzo8EzI-fpofSHnAO8TEa1M/edit), utilizado na prototipagem do formulário
* [Web.py](https://github.com/webpy/webpy) *framework web* em linguagem Python
* [SQLalchemy](http://www.sqlalchemy.org/), ferramenta para bancos de dados com suporte à ORM (mapeamento relacional de objetos)
* [LXML](http://lxml.de/), biblioteca para processamento de HTML e XML
* [Requests](http://docs.python-requests.org/en/latest), biblioteca para requisições HTTP 
* [Bootstrap](http://getbootstrap.com), famosa biblioteca de *front-end*


Para a execução local da Web App é necessário instalar:

 1. [Python 2.x](https://www.python.org)
 2. [Web.py](https://github.com/webpy/webpy)
 3. [SQLalchemy](http://www.sqlalchemy.org/)
 

## 4. Organização deste repositório
Este repositório está organizado como segue, qualquer submissão de conteúdo (commit) deve obedecer esta organização.

```
./
   README.md (Este documento)
   LICENSE (Nossa licença - GPL 3.0)
   gdanet/ (web app)
     app.py (Aplicação Web, páginas)
     models.py (Classes para ORM)
     config.py (Configuração básica do servidor)
     test.db (Banco de dados SQLite para testes)
     templates/ (HTML das páginas de apresentação)
     static/ (Conteúdo estático - img, css, etc)
     sessions/ (armazena informações de login)
     api/ (Aplicações secundárias - parsers, crawlers, etc)
   
   old/ (conteúdo antigo, pré versão web)
   doc/ (qualquer documentação)
```
