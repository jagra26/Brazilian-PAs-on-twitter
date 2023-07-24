#from wordcloud import STOPWORDS
start = '2022-01-01T00:00:00Z'  # begin date
end = '2022-12-31T23:59:59Z'  # end date
path = "./results/"
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAARjOQEAAAAAjCsNvbp%2BvU6p3cc6BFpkJPayGWQ%3DH0c7iKKk97AxW9NGACcMM0a2zhMCHLqJaGLFRXNyq6K5p03aL2'
# recent search or all time search
search_url = "https://api.twitter.com/2/tweets/search/all"
# search query
query = 'lang:pt -is:retweet ("Unidade de conservação" OR "Area protegida" OR "Parque Nacional" OR "Parque estadual" OR "Parque natural municipal" OR "Parque municipal" OR "Estação ecológica" OR "Reserva biológica" OR "Monumento natural" OR "Refúgio da vida silvestre" OR "Reserva extrativista" OR "Área de proteção ambiental" OR "Floresta nacional" OR "Floresta estadual" OR "Floresta municipal" OR "Reserva de desenvolvimento sustentável" OR "Área de relevante interesse" OR "Reserva Particular do Patrimônio Natural")'
# tweet infos
tweet_fields = 'author_id,created_at,geo,id,in_reply_to_user_id,public_metrics'
user_fields = 'name,username,verified'
expansions = 'geo.place_id,entities.mentions.username,author_id'
place_fields = 'country,country_code,place_type'
# results per pages
max_results = '500'
# wordcloud stop words
'''stopwords = set(STOPWORDS)
stopwords.update(["https", "Unidade de conservação", "Area protegida",
                  "Parque Nacional", "Estação ecológica", "Reserva biológica",
                  "Monumento natural", "Refúgio da vida silvestre",
                  "Reserva extrativista", "Área de proteção ambiental",
                  "Floresta nacional", "Reserva de desenvolvimento sustentável",
                  "Área de relevante interesse", "Reserva Particular do Patrimônio Natural",
                  "do", "de", "da", "para", "e", "t", "co", "uma", "o", "a", "pra",
                  "para", "um", "dos", "das", "é"])'''
opencage_key = '1c93c92bf19a43db9bf9be43aaf28066'
