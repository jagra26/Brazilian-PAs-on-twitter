from searchtweets import ResultStream,  gen_request_parameters, load_credentials
import csv
import pandas as pd
import time
SEARCH_QUERY = "snow"
RESULTS_PER_CALL = 500  # 100 for sandbox, 500 for paid tiers
TO_DATE = '2012-12-31'  # format YYYY-MM-DD HH:MM (hour and minutes optional)
FROM_DATE = '2012-01-01'  # format YYYY-MM-DD HH:MM (hour and minutes optional
FILENAME = "test"
premium_search_args = load_credentials("./twitter_keys.yaml",
                                       yaml_key="search_tweets_v2",
                                       env_overwrite=False)
query = gen_request_parameters(SEARCH_QUERY, results_per_call=10)
print(query)
rs = ResultStream(request_parameters=query,
                    max_results=10,
                    max_pages=10,
                    **premium_search_args)

with open(FILENAME + '.csv', 'w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(['id', 'text'])
	tweets = list(rs.stream())
	nextp = rs.next_token
	print(nextp)
	print(len(tweets))
	for tweet in tweets:
		text = tweet.get("text")
		uid = tweet.get("id")
		print(uid)
		writer.writerow([uid, text])
	file.close()
i = 1
print(i)
while nextp != None or i < 5:
	i+=1
	rs = ResultStream(request_parameters=query,
	                    max_results=10,
	                    max_pages=10,
	                    **premium_search_args, next_token = nextp)
	tweets = list(rs.stream())
	print(len(tweets))
	with open(FILENAME + '.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		tweets = list(rs.stream())
		print(len(tweets))
		for tweet in tweets:
			text = tweet.get("text")
			uid = tweet.get("id")
			print(uid)
			writer.writerow([uid, text])
		file.close()
	nextp = rs.next_token
	print(nextp)
	print(i)
	print("delay 10s\n")
	time.sleep(10)

'''tweets = list(rs.stream())
nextp = rs.next_token 
print(nextp)
print(tweets[0].get("text"))
rs = ResultStream(request_parameters=query,
                    max_results=10,
                    max_pages=10,
                    **premium_search_args, next_token = nextp)
tweets = list(rs.stream())
print(rs.next_token)
print(tweets[0].get("text"))'''
'''
with open(FILENAME + '.csv', 'w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(['id', 'text', 'created_at', 'author_id', 'in_reply_to_user_id', 
					'referenced_tweets.type', 'referenced_tweets_id',
					'attachments.media_keys', 'geo', 'geo.coordinates', 
					'geo.coordinates.coordinates', 'entities.urls',
					'entities.hashtags.tag', 'entities.mentions', 'public_metrics.retweet_count',
					'public_metrics.reply_count', 'public_metrics.like_count', 'public_metrics.quote_count', 'lang'])
	while True:
		tweets = list(rs.stream())
		nextp = rs.next_token
		for tweet in tweets:
			#print(type(tweet))
			print(tweet.get('id'))
			id = tweet.get("id")
			text = tweet.get("text")
			author_id = tweet.get("author_id")
			created_at = tweet.get("created_at")
			in_reply_to_user_id = tweet.get("in_reply_to_user_id")
			attachments_media_keys = tweet.get("attachments.media_keys")
			geo = tweet.get("geo")
			lang = tweet.get("lang")
			if tweet.get("referenced_tweets") is not None:
				referenced_tweets_id = tweet.get("referenced_tweets.id")
				referenced_tweets_type = tweet.get("referenced_tweets.id")
			else:
				referenced_tweets_id = None
				referenced_tweets_type = None
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
					if tweet.get("entities").get("hashtags")[1] is not None:
						entities_hashtags_tag = tweet.get("hashtags")[1]
					else:
						entities_hashtags_tag = None
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
			writer.writerow([id, text, created_at, author_id, in_reply_to_user_id, referenced_tweets_type,
				referenced_tweets_id, attachments_media_keys, geo, geo_coordinates, geo_coordinates_coordinates,
				entities_urls, entities_hashtags_tag, entities_mentions, public_metrics_retweet_count,
				public_metrics_reply_count, public_metrics_like_count, public_metrics_quote_count, lang])
			print(text)
		print(tweets[0])

		rs = ResultStream(request_parameters=query,
	                max_results=10,
	                max_pages=10,
	                **premium_search_args, next_token = nextp)
		if nextp is None:
			break
file.close()
'''
# Reading the csv file
pcsv = pd.read_csv(FILENAME + '.csv')

# saving xlsx file
excel = pd.ExcelWriter(FILENAME + '.xlsx')
pcsv.to_excel(excel, index=False)

excel.save()

print('done')