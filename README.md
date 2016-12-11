# GDA Web App [deprecated]
#### Grupo de Avaliação Discente (GDA) da Faculdade de Engenharia Elétrica e de Computação (FEEC) da Universidade de Campinas (Unicamp)

Visite nossa página: http://tiny.cc/gda

Conheça nossa história: http://www.cabs.fee.unicamp.br/?t=52_GDA

Nosso trabalho é reunir informações sobre as disciplinas ministradas a cada semestre e apresentá-las de forma compreensível e construtiva para os alunos e professores da Faculdade. Essa página foi feita para substituir os antigos guias impressos.

Estamos atualmente em nossa versão inicial. Ainda temos muito que melhorar! 

Descrevemos abaixo um pouco do que usamos para fazer esse projeto e como você pode ajudar. Nenhum conhecimento prévio é necessário, apenas seu interesse e sua disposição. Ficou interessado? Fale conosco.

Ali Faraj [faraj7 at gmail dot com]

Raul Cecato [raulcecato at gmail dot com]
 
## 1. Como você pode ajudar

* Assuntos acadêmicos : como usar os dados obtidos para melhorar nosso curso e nossa faculdade
* Desenvolvimento de aplicações Web : back-end, programação em Python e SQL
* Planejamento de interfaces : design, identidade visual, front-end (html, css, js)


## 2. Como o projeto foi feito
Nesta versão de desenvolvimento contamos com as seguintes ferramentas:

* [Web.py](https://github.com/webpy/webpy) *framework web* em linguagem Python
* [SQLalchemy](http://www.sqlalchemy.org/), ferramenta para bancos de dados com suporte à ORM (mapeamento relacional de objetos)
* [LXML](http://lxml.de/), biblioteca para processamento de HTML e XML
* [Requests](http://docs.python-requests.org/en/latest), biblioteca para requisições HTTP 
* [Bootstrap](http://getbootstrap.com), famosa biblioteca de *front-end*


Para a execução local da Web App é necessário instalar:

 1. [Python 2.x](https://www.python.org)
 2. [Web.py](https://github.com/webpy/webpy)
 3. [SQLalchemy](http://www.sqlalchemy.org/)
 

## 3. Organização deste repositório
Este repositório está organizado como segue, qualquer submissão de conteúdo (commit) deve obedecer esta organização.

```
./
   README.md (Este documento)
   LICENSE (Nossa licença - GPL 3.0)
   net/ (web app)
   app.py (Aplicação Web, páginas)
   models.py (Classes para ORM)
   constants.py (Configuração básica do servidor)
   test.db (Banco de dados SQLite para testes)
   templates/ (HTML das páginas de apresentação)
   static/ (Conteúdo estático - img, css, etc)
   sessions/ (armazena informações de login)
   api/ (Aplicações secundárias - parsers, crawlers, etc)

```
