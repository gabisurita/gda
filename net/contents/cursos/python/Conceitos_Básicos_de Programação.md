##Conceitos básicos de programação
Texto por Rodrigo Cacilhas 

# 

Quando as pessoas começam a se interessar por programação, podem ficar confusas com tantos conceitos novos. Mas pior que isso, parece que cada grupo define cada conceito de forma diferente, atribuindo conotações positivas e negativas indiscriminadamente segundo seus interesses.

A confusão gerada por essa briga de egos é enorme e pode levar muitos incautos por caminhos tortuosos, então é preciso muito bom senso.

Vamos tentar aqui apresentar algumas poucas definições da forma mais imparcial possível – o que incrivelmente pode ofender alguns mais afoitos.

###Básico da programação

Programação pode ser definido como o ato de descrever um algoritmo que resolva um problema proposto de forma aplicável. Não é a única definição, não é a melhor, mas é muito boa, não?

Um algoritmo é uma sequência de passos a ser executada para se chegar a um objeto, no caso, a solução de um problema proposto. Para que a descrição do algoritmo seja aplicável, tem de ser feita usando um protocolo linguístico que o executor reconheça. Este protocolo é chamado linguagem de programação.

Como utilizamos computadores para realizar a execução do programa, a linguagem de programação precisa ser reconhecida pelo computador que realizará aquela tarefa específica.

Essencialmente computadores reconhecem apenas uma linguagem específica, formada por instruções relacionadas a microinstruções registradas no microprograma do processador. Esta linguagem é chamada linguagem ou código de máquina e é extremamente incompreensível. =P

No entanto é preciso que o programa esteja em linguagem de máquina para que o computador possa executá-lo, o que é um problema e tanto.

A forma usada para solucionar a questão é relativamente simples: a criação de «tradutores» que permitam que o programa seja escrito em linguagens mais inteligíveis para então ser «traduzido» para a linguagem de máquina. Há alguns tipos diferentes de tradução, como montagem, compilação, interpretação e interpilação. Veremos mais a frente.

###Nível de abstração

O uso de tradutores permite que a linguagem usada para a programação apresente um certo nível de abstração da forma como a máquina funciona. Linguagens que se aproximam muito do funcionamento da máquina são chamadas de baixo nível, já linguagens que se afastam do funcionamento são chamados de alto nível.

Por exemplo, a linguagem Assembly possui uma instrução para cada instrução de máquina, sendo assim uma linguagem de baixo nível. Isso traz dois inconvenientes: ¹é preciso entender como cada processador funciona para a criação do programa e ²o programa se torna pouco portável, sendo necessário reescrevê-lo para cada tipo de diferente de processador.

Por outro lado, traz uma grande vantagem: como não há uma «tradução» propriamente dita, apenas uma conversão de símbolos (tokens), a execução do programa se torna extremamente eficiente.

Isso ocorre porque toda tradução semântica gera verborragia, ou seja, excesso de comandos para fazer coisas simples. Quanto maior a diferença entre a linguagem original e a de destino, maior a probabilidade de verborragia, mas não necessariamente.

Quando definimos nível de abstração, entramos numa questão delicada, pois há um tremendo mal entendido sobre o que seja uma linguagem de alto nível.

Por exemplo: a linguagem C é uma linguagem de alto nível, pois abstrai do funcionamento da máquina, se aproximando da linguagem matemática. No entanto pessoas com dificuldade em matemática não entende isso.

###Tipos de «tradução»

Há muitas variações de como a tradução de uma linguagem de mais alto nível para a linguagem de máquina é feita.

A mais simples é a montagem, que é quando cada instrução da linguagem de mais alto nível é traduzida diretamente para uma instrução da linguagem de máquina. O programa que faz esta montagem é chamado montador. Ex.: Assembly.

Um pouco mais complicada é a compilação: a partir do programa em linguagem de mais alto nível é gerado um programa de mais baixo nível equivalente, que é montado, gerando o código objeto (programa em código de máquina). Ex.: C.

Na compilação há em geral mais de um programa trabalhando, basicamente o compilador, que gera um objeto que faz chamadas a procedimentos que não possui, e o linkeditor, que liga ao objeto outros objetos, chamados bibliotecas, que possuem os procedimentos necessários, gerando o objeto final ou código de máquina.

Outra alternativa é a interpretação. Há um programa chamado interpretador que funciona como se fosse uma máquina virtual, com suas próprias instruções, e o programa é feito usando tais instruções. Ex.: Tcl/Tk.

Por final, há variações destas três formas citadas.

Por exemplo, há linguagens cuja compilação não gera código de máquina, mas um código intermediário, chamado bytecode, que é interpretado por um interpretador chamado máquina virtual (pois é… máquina virtual é um tipo de interpretador). Por exemplo, Java trabalha assim.

Uma variação deste tipo de compilação é a usada em Smalltalk, pois não é gerado um bytecode, mas a compilação altera o comportamento da máquina virtual.

Por último existe a interpilação, que possui duas variações: ¹o interpilador recebe o código e gera um objeto em código de máquina, mas somente em memória, e este objeto é executado diretamente da memória (ex.: Perl); ou ²o interpilador recebe o código e gera um bytecode em memória que é executado por uma máquina virtual (como Python e Lua).

Algumas linguagens podem trabalhar com traduções diferentes. Por exemplo, Perl pode ser interpilado ou compilado. Python e Lua podem ser interpilados com máquina virtual, ou compilados para bytecode (que será também interpretado por uma máquina virtual).

###Manipulação de dados

A principal parte da programação é a manipulação de dados: armazenamento, leitura e alteração.

Para armazenamento e leitura usamos posições de memória e registradores do processador.

Em linguagens de mais baixo nível, usamos os próprios endereços de memória e o nomes do registrador, mas em linguagens de nível mais alto, usamos variáveis, que são «apelidos» para tais endereços e nomes.

Também é necessário saber que quantidade de memória cada dado ocupa e como ele deve se comporta. Isso é chamado tipagem.

###Transferência de informações

Muitas vezes é necessário que um determinado dado seja transferido de uma variável para outra. Esta transferência é camada passagem e há dois tipos de passagem: passagem por valor e passagem por referência.

####Passagem por valor


A passagem por valor ocorre quando cada variável contém o dado em si. Assim quando passamos um dado de uma variável para outra o dado é duplicado para a segunda variável.

Então a alteração do dado na variável de destino não altera o dado na variável de origem.

####Passagem por referência


A passagem por referência ocorre quando a variável não contém o dado em si, mas um ponteiro para a posição de memória onde o dado se encontra. Assim quando passamos uma referência de uma variável para outra o dado não é duplicado, apenas as duas variáveis apontam para a mesma posição de memória.

Então a alteração do dado na variável de destino altera consequentemente o dado na variável de origem, pois ambos são o mesmo dado.

Algumas linguagens, como C/C++, permitem o programador escolher usar valores ou ponteiros, enquanto outras linguagens (na verdade a maioria delas) usam valor para alguns tipos determinados e ponteiro (na verdade referência, que é um ponteiro implícito) para outros.

###Tipagem

Tipagem é a definição da quantidade de memória que um determinado dado ocupa e como esse dado deve interagir com os demais.

Há duas classificações de tipagem, veremos a seguir.

###Tipagem estática × tipagem dinâmica


Esta é uma definição discreta. Há duas formas distintas de tratar os tipos de dados: ou o tipo está associado ao dado, ou está associado à variável que o referencia.

Quando o tipo está associado ao dado em si, chamamos de tipagem dinâmica.
Quando o tipo está associado à variável, chamamos de tipagem estática.

Dizemos dinâmica ou estática em relação à variável, ou seja, na tipagem dinâmica uma mesma variável pode conter dados de tipos diferentes, dinamicamente, enquanto na tipagem estática uma variável conterá sempre dados do mesmo tipo.

Por outro lado na tipagem dinâmica o dado sempre se comportará da mesma forma independente da variável à qual foi associado e na tipagem estática o dado se comportará de formas diferentes de acordo com a variável que o referencia.

Enquanto falamos de valores, pode parecer que a tipagem estática seja superior, mas quando falamos de ponteiros/referências, a tipagem dinâmica passa a levar vantagem.

Isso ocorre porque queremos que um determinado dado se comporte sempre da mesma forma.

No entanto a tipagem dinâmica é mais difícil de ser trabalhada, pois exige atenção redobrada.

Em suma, ambos as tipagens possuem vantagens e desvantagens, cabendo ao programador (veja bem: ao programador, não ao professor do programador, à comunidade, ao livro ou qualquer outro fator externo) decidir qual lhe satisfaz melhor.

###Tipagem fraca × tipagem forte


Ao contrário da anterior, está uma definição contínua. Há duas direções: tipagem fraca indica menor quantidade de tipos e/ou menor distinção entre os tipos e tipagem forte indica maior quantidade de tipos e/ou maior distinção entre os tipos.

Assim como a definição de nível de abstração, há linguagens de tipagem mais forte e outras de tipagem mais fraca.

Por exemplo, C é uma linguagem de tipagem fraca, pois, apesar de possuir quatro tipos (int, char, float e double) e algumas variações (long, unsigned, struct, union…), os tipos se confundem, ou seja, a distinção entre os tipos não é perfeitamente clara.

Um exemplo de tipagem ainda mais fraca é Perl, que além de possuir apenas três tipos (escalar, vetor e hash), os tipos se confundem.

Vamos agora a linguagens de tipagem mais forte…

C++ possui os mesmos tipos de C, mais as classes (que se comportam de forma semelhante a tipos), e ainda faz uma boa distinção entre os tipos.

Java possui alguns tipos, mais classes (como C++), e tem uma distinção bem forte.

Python possui apenas dois tipos reais: tipo e objeto, no entanto tipo e objeto se comportam da mesma forma e as classes (variantes de tipo e de objeto) se comportam como tipos. Resumindo, Python possui uma tipagem tremendamente forte, pois na prática possui mais de trinta tipos perfeitamente distintos entre si.

Lua é uma linguagem a meio caminho, pois possui sete tipos bem distintos entre si, mas a conversão é facilitada.

Novamente não há uma escolha certa, forte ou fraco… tudo depende de com que o programador se identifica.


###Observação séria

Alguns evangelizadores fazem desinformação proposital para convencer as pessoas de suas crenças pessoais, divulgando inverdades.

Algumas inverdades clássicas são:

* Tipagem dinâmica é ruim, estática é boa.
* Tipagem fraca é ruim, forte é boa.
* Tipagem fraca é o mesmo que tipagem dinâmica.
* Não existe essa de tipagem mais ou menos forte, tipagem é fraca ou forte e pronto.
* Compilação é melhor que interpretação.
* Interpretação por máquina virtual não é interpretação, é compilação.
* Apenas Java usa máquina virtual.
* C não é portável porque não usa máquina virtual.
* Toda linguagem interpretada (o que exclui Java) é scripting.


Há outras clássicas, veremos mais a frente. O importante é não acreditar.

###Paradigmas de programação

Paradigma de programação é a forma como o programador enxerga a solução do problema. Tem mais a haver com a estruturação.

Em outras palavras, paradigma é a metodologia de solução.

Inicialmente os programadores não se preocupavam com paradigma algum. Então os programas eram simples sequências de procedimentos. Hoje em dia chamamos isso de programação sequencial e exclui automaticamente todos os demais paradigmas.

Mais tarde foi desenvolvido o paradigma procedimental e a programação estruturada.

####Programação estruturada


Programação estruturada é baseada na estruturação do código.

A idéia é que o programa seja divido em pequenos procedimentos estruturados, chamados subrotinas ou funções. O programa é desenvolvido a partir das funções mais abstratas e terminando pelas mais específicas (desenvolvimento top-down).

Deu origem à modularização e à programação procedimental.

####Programação procedimental


Erroneamente chamada programação procedural (procedural é procedimental em inglês), programação procedimental é a programação baseada em procedimentos.

O conceito é usado normalmente em oposição a programação funcional e às vezes se confunde com programação estruturada ou com programação imperativa.

####Programação funcional


O foco deste paradigma está nas funções matemáticas.

Um programa então é uma associação de funções matemáticas.


####Programação orientada a objetos


Na orientação a objetos o programa não se baseia em procedimentos, mas na relação entre objetos.

Objetos são representações de «coisas» que executam funções (chamadas métodos). Estas «coisas» são quase microuniversos independentes.

Da interação entre os objetos resulta a solução do problema proposto.

Por exemplo, uma porta é um objeto que, através de sua interação com o portal, a tranca e a chave permite que determinadas pessoas entram e saiam enquanto outras não.

**Importante:** os evangelizadores da desinformação pregam que a orientação a objetos exclui outros paradigmas e que seja o paradigma definitivo, no entanto não é possível usar orientação a objetos sem programação estruturada, ou seja, o código precisa estar estruturado para ser orientado a objetos.

Aliás a programação estruturada é pré-requisito para a maioria dos demais paradigmas.

####Programação orientada a eventos


A orientação a eventos pressupõe a orientação a objetos, pois implica em criar objetos que reajam a determinados eventos.

Geralmente é criado loop principal que intercepta os eventos, repassando-os para os objetos registrados. Algumas linguagens (ou módulos) oferecem uma implementação pronta do loop principal.

####Outros paradigmas


Em tese pode haver tantos paradigmas quanto programadores, visto que paradigma é a forma como o programador vê a solução do programa.

Apenas alguns dos mais clássicos são:

* Programação declarativa
* Programação restritiva × programação lógica
* Orientação a aspecto
* Programação genérica


###Scripting


Há ainda outro conceito, que é a programação scripting, que consiste no desenvolvimento de scripts.

Script é um código interpretado ou interpilado (muitas vezes por máquina virtual) que consiste em agregar componentes pré-compilados.

Pela definição, a grande maioria das linguagens modernas são linguagens de scripting (inclusive Java).

No entanto há pessoas que usam o termo scripting com sentido estritamente pejorativo, sem entender exatamente o significado. Essas pessoas nunca aceitam que sua linguagem seja chamava de linguagem de scripting. Às vezes distorcem a descrição do conceito, às vezes mentem sobre o funcionamento de sua linguagem e muitas vezes apenas negam sistematicamente, sem qualquer argumento real.

Na prática «linguagem de scripting» é só um conceito arbitário usado ou pejorativamente para malfalar alguma linguagem ou para dizer que uma linguagem é muito fácil de ser aprendida.

###Conclusão

Esta foi apenas um exposição superficial de alguns conceitos básicos de programação, mas mais importante, é um alerta aos programadores incautos que acabam por crer na evangelização de pessoas que têm por objetivo desinformar e fanatizar.

Estejam sempre atentos e, mais importante, mente sempre aberta. =)


