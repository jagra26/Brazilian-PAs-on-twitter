# Download-Tweets
Este repositório tem o intuito de baixar e processar
dados do registro histórico do Twitter.

## Tabela de conteúdos
- [Tabela de conteúdos](#tabela-de-conteúdos)
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

As variáveis *start* e *end* se referem ao intervalo de busca.
Altere para o intervalo desejado, mantendo o padrão.

A variável *path* se refere a pasta que os tweets serão salvos.
Por padrão está setada para [results](results/)

A variável *bearer_token* se refere ao token dado pela API do Twitter.
Pode ser gerada no [dashboard](https://developer.twitter.com/en/portal/dashboard)
do seu projeto

A variável *search_url* se refere a forma de busca dentro da API.
Por padrão está setado para busca histórica. Caso queira fazer a busca
só nos últimos 30 dias troque "all" por "recent" na url. Lembre-se de 
respeitar o intervalo.

A váriavel *query* se refere ao que é efetivamente buscado, siga a [documentação](https://developer.twitter.com/en/docs/tutorials/building-high-quality-filters)
do Twitter para chegar ao resultado desejado.

As variáveis terminadas em *fields* e a variável *expansions*
se referem ao campos opcionais que serão retornados pela API. 
Siga o que consta na [documentação](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream).

A variável *max_results* se refere a quantidade de tweets 
que cosntará em cada página. Por padrão o valor é 500, números muito altos
gerarão erros de excesso de requisições.

## Uso

Após tudo instalado e configurado, inicie buscando os tweets.
Executando o programa [full-archive-search.py](full-archive-search.py):
```
python3 full-archive-search.py
```
Este programa busca e salva os tweets, um arquivo .txt para cada página buscada.
Que ficam salvos no diretório referente ao intervalo buscado.

Para reunir a informação de todas as páginas em um único arquivo, 
utilize o programa [convert.py](convert.py):
```
python3 full-archive-search.py
```
Este programa gera duas tabelas, uma .csv e outra .xlsx
Ambas contém a informação de todas páginas anteriormente 
baixadas. Estes formatos facilitam a análise e elaboração
de gráficos.

## Autores

Carolina Neves
  * [Lattes](http://lattes.cnpq.br/6552839552231088)
  * [Github](https://github.com/carolinaneves-ufal) 

João Almeida
  * [Lattes](http://lattes.cnpq.br/7977737909149890)
  * [Github](https://github.com/jagra26)

## Licença

O projeto utiliza [licença MIT](LICENSE.txt)
