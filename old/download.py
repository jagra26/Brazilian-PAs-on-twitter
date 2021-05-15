from searchtweets import ResultStream,  gen_request_parameters, load_credentials
import csv
import pandas as pd
import time
SEARCH_QUERY = 'lang:pt -is:retweet ("Unidade de conservação" OR "Area protegida" OR "Parque Nacional" OR "Estação ecológica" OR "Reserva biológica" OR "Monumento natural" OR "Refúgio da vida silvestre" OR "Reserva extrativista" OR "Área de proteção ambiental" OR "Floresta nacional" OR "Reserva de desenvolvimento sustentável" OR "Área de relevante interesse" OR "RPPN")'
RESULTS_PER_CALL = 500  # 100 for sandbox, 500 for paid tiers
TO_DATE = '2011-01-31'  # format YYYY-MM-DD HH:MM (hour and minutes optional)
FROM_DATE = '2011-01-01'  # format YYYY-MM-DD HH:MM (hour and minutes optional
FILENAME = FROM_DATE + "_" + TO_DATE
premium_search_args = load_credentials("./twitter_keys.yaml",
                                       yaml_key="search_tweets_v2_academic",
                                       env_overwrite=False)
query = gen_request_parameters(SEARCH_QUERY, results_per_call=RESULTS_PER_CALL,
	tweet_fields='lang,created_at,author_id,conversation_id,in_reply_to_user_id,referenced_tweets,attachments,geo,entities,public_metrics',
	start_time=FROM_DATE, end_time=TO_DATE)
#,expansions='referenced_tweets.id,attachments.media_keys'
print(query)
rs = ResultStream(request_parameters=query,
                    max_results=500,
                    **premium_search_args)
print(rs)
with open(FILENAME + '.csv', 'w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(['id', 'text', 'created_at', 'author_id', 'in_reply_to_user_id',
					'geo', 'geo.coordinates', 
					'geo.coordinates.coordinates', 'entities.urls',
					'entities.hashtags.tag', 'entities.mentions', 'public_metrics.retweet_count',
					'public_metrics.reply_count', 'public_metrics.like_count', 'public_metrics.quote_count', 'lang'])
	page = 1
	while True:
		try:
			tweets = list(rs.stream())
			next_token = rs.next_token
			print("\n-----\nnext_token: " + next_token + "\n-----\n")
			if next_token is None:
				break
			print("size of page:", len(tweets))
			print(tweets[0].get("id"))
			rs = ResultStream(request_parameters=query,
                    max_results=500,
                    **premium_search_args, next_token = next_token)
			for tweet in tweets:
				#print(type(tweet))
				#print(tweet.get('id'))
				id = tweet.get("id")
				text = tweet.get("text")
				author_id = tweet.get("author_id")
				created_at = tweet.get("created_at")
				in_reply_to_user_id = tweet.get("in_reply_to_user_id")
				#attachments_media_keys = tweet.get("attachments.media_keys")
				geo = tweet.get("geo")
				lang = tweet.get("lang")
				'''if tweet.get("referenced_tweets") is not None:
					referenced_tweets_id = tweet.get("referenced_tweets.id")
					referenced_tweets_type = tweet.get("referenced_tweets.id")
				else:
					referenced_tweets_id = None
					referenced_tweets_type = None'''
				if geo is not None:
					if tweet.get("geo").get("coordinates") is not None:
						geo_coordinates = tweet.get("geo").get("coordinates")
						if tweet.get("geo").get("coordinates").get("coordinates") is not None:
							geo_coordinates = tweet.get("geo").get("coordinates").get("coordinates")
						else:
							geo_coordinates_coordinates = None
					else:
						geo_coordinates = None
				else:
					geo_coordinates = None
					geo_coordinates_coordinates = None
				if tweet.get("entities") is not None:
					if tweet.get("entities").get("urls") is not None:
						entities_urls = tweet.get("entities").get("urls")
					else:
						entities_urls = None
					if tweet.get("entities").get("hashtags") is not None:
						entities_hashtags_tag = tweet.get("entities").get("hashtags")
						'''if tweet.get("entities").get("hashtags")[1] is not None:
							entities_hashtags_tag = tweet.get("hashtags")[1]
						else:
							entities_hashtags_tag = None'''
					else:
						entities_hashtags_tag = None
					if tweet.get("entities").get("mentions") is not None:
						entities_mentions = tweet.get("entities").get("mentions")
					else:
						entities_mentions = 0
				else:
					entities_urls = None
					entities_hashtags_tag = None
					entities_mentions = 0
				if tweet.get("public_metrics") is not None:
					if tweet.get("public_metrics").get("retweet_count") is not None:
						public_metrics_retweet_count = tweet.get("public_metrics").get("retweet_count")
					else:
						public_metrics_retweet_count =	0
					if tweet.get("public_metrics").get("reply_count") is not None:
						public_metrics_reply_count = tweet.get("public_metrics").get("reply_count")
					else:
						public_metrics_reply_count = 0
					if tweet.get("public_metrics").get("like_count") is not None:
						public_metrics_like_count = tweet.get("public_metrics").get("like_count")
					else:
						public_metrics_like_count = 0
					if tweet.get("public_metrics").get("quote_count") is not None:
						public_metrics_quote_count = tweet.get("public_metrics").get("quote_count")
					else:
						public_metrics_quote_count = 0
				else:
					public_metrics_retweet_count = 0
					public_metrics_reply_count = 0
					public_metrics_like_count = 0
					public_metrics_quote_count = 0
				writer.writerow([id, text, created_at, author_id, in_reply_to_user_id, geo, geo_coordinates, geo_coordinates_coordinates,
					entities_urls, entities_hashtags_tag, entities_mentions, public_metrics_retweet_count,
					public_metrics_reply_count, public_metrics_like_count, public_metrics_quote_count, lang])
				#print(text)
				#print(created_at)
			print(page)
			page += 1
			print("wait 10 seconds")
			time.sleep(10)
		except:
			print("erro")
			break
	file.close()

# Reading the csv file
pcsv = pd.read_csv(FILENAME + '.csv')

# saving xlsx file
excel = pd.ExcelWriter(FILENAME + '.xlsx')
pcsv.to_excel(excel, index=False)

excel.save()

print('done')