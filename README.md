# Download-Tweets
Este repositório tem o intuito de baixar e processar
dados do registro histórico do Twitter.

## Tabela de conteúdos
- [Tabela de conteúdos](#tabeladeconteudos)
- [Estrutura](#estrutura)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Autores](#autores)
- [Citação](#citação)
- [Licença](#licença)

## Estrutura
Os dois principais scripts do projeto são 
[full-archive-search](full-archive-search.py) e
[convert](convert.py).
São baseados na [API do twitter](https://github.com/twitterdev/Twitter-API-v2-sample-code),
e em [Pandas](https://pandas.pydata.org) 

Há também um [arquivo](variables.py) de configuração.

Os resultados são salvos na pasta [results](results/).
Cada intervalo buscado é salvo em uma subpasta.

A pasta [old](old/) contém experimentos anteriores mal-sucedidos,
utilizando a biblioteca [search-tweets](https://github.com/twitterdev/search-tweets-python/tree/v2)

## Instalação

Primeiro, instale o [python 3](https://realpython.com/installing-python/)

Instale o [pip](https://pip.pypa.io/en/stable/installing/)

Em seguida instale o [git](https://git-scm.com/downloads)

Clone o repositório: 
 
 ```
git clone https://github.com/jagra26/Download-Tweets.git
 ```

Instale os requerimentos:

 ```
pip install -r requirements.txt
 ```

## Configuração

Abra o [arquivo](variables.py) de configuração.

As duas primeiras linhas se referem ao intervalo de busca.
Altere para o intervalo desejado, mantendo o padrão.

