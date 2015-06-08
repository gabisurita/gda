## Tutorial - Instalando Python 

### 0. Introdução
Python possui uma grade gama de distribuições e pacotes. Aqui segue um breve tutorial de como instalar o interpretador padrão junto com alguns pacotes que serão necessários durante o curso. 

Uma lista não extensiva de softwares que usaremos durante o curso é apresentada a seguir:

* CPython
* NumPy
* SciPy
* Matplotlib
* SymPy
* QtPy4
* Ipython Notebook
* Urllib3
* Web.py
* MyHDL

Tutoriais de instalação para diversos sistemas operacionais são apresentados a seguir.

### 1. Linux
As instruções aqui apresentadas cobrem distribuições de Linux baseadas em Debian e Fedora com gerenciadores de pacotes **yum** ou **apt-get**. Os comandos devem ser executados através de um terminal. Serão necessários privilégios de administrador.


#### 1.1 Interpretador Python
Uma grande opções de Linux disponibilizam  o interpretador Python v2.x pré-instalado, porém você pode instalá-lo ou atualizá-lo com os seguintes comandos:

Com **yum**:

`sudo yum install python`

Com **apt-get**:

`sudo apt-get install python`

**Opcional:** Para instalar também as versões 3.x da linguagem, use os comandos:

`sudo yum install python3`

Ou

`sudo apt-get install python3`


#### 1.2 Bibliotecas para análise numérica: Numpy e Scipy e Matplotlib
Algumas bibliotecas essenciais no use de Python para computação científica são Numpy (possui modelos matriciais eficientes e funções matemáticas), Scipy (incluí diversas funções matemáticas complexas) e Matplotlib (permite criação de gráficos de maneira rápida). 

Com **yum**:

`sudo yum install numpy scipy python-matplotlib`

Com **apt-get**:

`sudo apt-get install python-numpy python-scipy python-matplotlib`


#### 1.3 Instalação de biblioteca de interface gráfica: Qt4
Instalação de uma biblioteca de insterface gráfica multiplataforma.

Com **yum**:

`sudo yum install PyQt4`

Com **apt-get**:

`sudo apt-get install python-qt4`

#### 1.4 Gerenciador de pacotes: Pip
Um eficiente gerenciador de pacotes para Python é o Pip. Que permite instalação de pacotes com apenas um comando.
 
Com **yum**:

`sudo yum install python-pip`

Com **apt-get**:

`sudo apt-get install python-pip`


#### 1.5 Instalação de pacotes adicionais
Agora usaremos "pip" para instalar os demais pacotes adicionais necessários no curso.

`sudo pip install web.py myhdl urllib3 sympy`


#### 1.6 Instalação do Ipython
O Ipython é uma "capa" do interpretador Python que incorpora impressões de funções matemáticas, HTML e outras comodidades.

`sudo pip install ipython ipython[notebook]`




### 2. MAC OS X
A descrição a seguir deve funcionar para qualquer versão de MAC OS recente, porém não foi testada e pode conter alguns erros.

#### 2.1 Interpretador Python
O interpretador Python v2.x também é pré-instalado no MAC OS, porém é preciso atualiza-lo para a versão mais nova. Para isto, o jeito mais fácil envolve instalar um gerenciador de pacotes. A recomendação é instalar o **Homebrew**, que já incluí o gerenciador de pacotes Python Pip. Para isto, abra um terminal (/Applications/Utilities/Terminal).

O comando a seguir instala o **Homebrew**, siga quaisquer passos necessários:

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)`

Precisaremos também de um compilador C:

`brew install gcc`

Após a instalação, podemos atualizar o interpretador de Python com o comando:

`brew install python`

**Opcional:** Para instalar também as versões 3.x da linguagem, use o comando:

`brew install python3`

#### 2.2 Bibliotecas para análise numérica: Numpy e Scipy e Matplotlib
Algumas bibliotecas essenciais no use de Python para computação científica são Numpy (possui modelos matriciais eficientes e funções matemáticas), Scipy (incluí diversas funções matemáticas complexas) e Matplotlib (permite criação de gráficos de maneira rápida). Para instalar o Scipy, é necessário possuir um compilador de Fortran, para isto utilize os seguintes comandos:

`brew install gfortran`
`pip install numpy scipy matplotlib`


#### 2.3 Instalação de biblioteca de interface gráfica: Qt4
Instalação de uma biblioteca de insterface gráfica multiplataforma.

`brew install pyqt`


#### 2.4 Instalação de pacotes adicionais
Agora usaremos "pip" para instalar os demais pacotes adicionais necessários no curso.

`sudo pip install web.py myhdl urllib3 sympy`


#### 2.5 Instalação do Ipython
O Ipython é uma "capa" do interpretador Python que incorpora impressões de funções matemáticas, HTML e outras comodidades.

`sudo pip install ipython ipython[notebook]`



### 3. Windows
A abordagem de instalação no Windows difere um pouco dos sistemas baseados em Unix uma vez que não existe um instalador integrado neste sistema, sendo assim é necessário instalar programas compilados (.exe) manualmente. Felizmente, existem diversos projetos que encapsulam os pacotes mais comuns de Python juntos ao compilador em apenas um arquivo.

#### 3.1 Instalação do Portable Python
Usaremos o **Portable Python**, que incluí diversas ferramentas como as bibliotecas de programação científica e interface gráfica. Faça o download de sua versão de Python 2.7.x no [site do projeto](http://www.portablepython.com).

Execute o script e instale-o com todos os adicionais em um **diretório facilmente acessível**. Recomenda-se algo como `C:\\PortablePython\`. Siga as instruções e faça a instalação completa.


#### 3.2 Pacotes adicionais
Infelizmente utilizar o 'pip', como foi feito nos sistemas baseados em Linux não é nada trivial no Windows, porém podemos usar um script chamado 'easy_install' incluído no **Portable Python**.

Para utilizá-lo abra uma linha de comando (cmd). Um jeito de fazê-lo é via Super+R (Super é a tecla com símbolo do Windows) e digitando o comando `cmd`.

Após abrir o **cmd** navegue até os Scripts de instalação pelo comando `cd`, no nosso exemplo de diretório:

`cd C:\\PortablePython\App\Scripts`

**Obs:** Se parte do endereço conter espaços, é necessário específicá-la entre " ". Exemplo:  `cd C:\\"Portable Python"\App\Scripts`


E execute os seguintes comandos, um após a execução do outro:

 
`easy_install.exe sympy`

`easy_install.exe myhdl`

`easy_install.exe urllib3`

`easy_install.exe web.py`
     


