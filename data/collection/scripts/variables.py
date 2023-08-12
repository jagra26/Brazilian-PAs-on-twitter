# File to store variables used in the project
start = '2022-01-01T00:00:00Z'  # begin date
end = '2022-12-31T23:59:59Z'  # end date
path = "./results/"
bearer_token = ''
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
opencage_key = ''
