# Base de Conhecimento
- Projeto para a disciplina de Inteligência Artiificial
- Implementação de uma base de conhecimento utilizando uma rede semântica 
- [Vídeo com o funcionamento](https://youtu.be/TUZhv-JGYxk)

## Autores e Distribuição de Tarefas:
Bruno Machado Ferreira `Troubleshooting e Documentação do Projeto`

Ernani Mendes da Fonseca Neto `Tratamento de dados dos animais e lógica das perguntas`

Fábio Gomes de Souza `Backend e Pesquisa sobre os animais usados`

Ryan Henrique Nantes `Frontend e Grafos de Ontologia`

## Introdução
O projeto tem como objetivo criar um sistema capaz de responder perguntas relacionadas às espécies de animais utilizando informações extraídas de umas base de dados interna. 
A ideia é que o usuário possa inserir as perguntas e receba respostas com base nas informações disponíveis na base de conhecimentos.
A estrutura da aplicação será dividida em três módulos principais: Frontend, Backend e Base de Dados. 
A interface recebe uma pergunta do usuário, realiza a requisição de informações e exibi-las ao usuário. 
Além disso, o repositório contará com a implementação de uma rede semântica para armazenamento e pesquisa de informações.

## Requisitos
- Ubuntu 22.04 ou 23.04 LTS
- (mini)Conda
- [Python 3.10](https://www.python.org/downloads/release/python-3100/) 
- [graphviz 0.20.1](https://pypi.org/project/graphviz/0.20.1/) 

## Preparando o ambiente
Agora, vamos criar o ambiente Conda e ativá-lo. Em um terminal aberto na pasta que contém o projeto, execute `conda create -n basecon python==3.10 -y && conda activate basecon`.
Em seguida, instale graphviz usando `pip install graphviz==0.20.1`. Em alguns casos, o sistema pode retornar um erro referente ao graphviz não estar no PATH. Para contornar isso, certifique-se de instalar a dependência diretamente no sistema usando `sudo apt-get install graphviz`. 
Para verificar que tudo está instalado, execute `python` para ativar o prompt interativo do Python e em seguida, `import tkinter` e `import graphviz`. Se tudo estiver certo, nenhum erro será retornado.
Feche o prompt interativo apertando Ctrl+Z e execute `python main.py` para começar!

## Implementação
Para implementar, fizemos uso de arquivos separados para as perguntas e os animais. Os dados foram tratados como dicionários Python a fim de facilitar o trabalho de passar informações ao programa

## Uso e funcionamento
Ao executar o arquivo main.py, você verá uma janela com um campo de perguntas, outro de respostas e vários botões. 

Um dos métodos é fazer perguntas diretamente no campo de texto e clicar em "Perguntar". A pergunta DEVE conter termos registrados na rede semântica, senão a resposta será inadequada e poderá travar o programa. 

Ao fazer perguntas diretas, o programa responderá de acordo e iniciará um grafo. Este grafo será incrementado com dados extraídos pelas perguntas do usuário.

Para testes com mais precisão, confira os termos já configurados e os animais registrados clicando, respectivamente em "Ver as propriedades" e "Ver os animais". 

O botão "Comparar dois animais" vai solicitar ao usuário dois animais dentro da rede semântica. Ao preencher os campos, o programa abrirá uma janela nova para mostrar os dados na base de conhecimento referente aos animais escolhidos.

O botão "Visualizar rede semântica completa" faz o programa criar e abrir um arquivo que contém toda a ontologia registrada, com os grafos interligados em todas as combinações. 

Atenção! A rede semântica completa é uma imagem MUITO grande. O zoom é limitado pelo hardware local.

Os arquivos "animais.py" e "perguntas.py" são os componentes do backend, armazenando os dados da base de conhecimento e configurando a flexibilidade dos termos usados para fazer perguntas.


### Referências
- [Conhecimento inicial sobre Bases de Conhecimento](https://github.com/XinTongBUPT/Knowledge-Base)
- [Youtube do professor Hemerson Pistori](https://www.youtube.com/@HemersonPistori)
- [Frederico Luiz Gonçalves de Freitas, "Ontologias e a Web Semântica"](http://www.inf.ufsc.br/~fernando.gauthier/EGC6006/material/Aula%203/Ontologia_Web_semantica%20Freitas.pdf?authuser=3)
