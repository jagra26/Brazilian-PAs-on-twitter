from searchtweets import ResultStream,  gen_request_parameters, load_credentials
import csv
import pandas as pd
import time
SEARCH_QUERY = "snow" #'lang:pt -is:retweet ("Unidade de conservação" OR "Area protegida" OR "Parque Nacional" OR "Estação ecológica" OR "Reserva biológica" OR "Monumento natural" OR "Refúgio da vida silvestre" OR "Reserva extrativista" OR "Área de proteção ambiental" OR "Floresta nacional" OR "Reserva de desenvolvimento sustentável" OR "Área de relevante interesse" OR "RPPN")'
RESULTS_PER_CALL = 500  # 100 for sandbox, 500 for paid tiers
TO_DATE = '2011-01-31'  # format YYYY-MM-DD HH:MM (hour and minutes optional)
FROM_DATE = '2011-01-01'  # format YYYY-MM-DD HH:MM (hour and minutes optional
FILENAME = FROM_DATE + "_" + TO_DATE
TWEET_FIELDS = 'lang,created_at,author_id,conversation_id,in_reply_to_user_id,referenced_tweets,attachments,geo,entities,public_metrics'
EXPANSIONS = 'referenced_tweets.id,attachments.media_keys'
def writecsv(fpath, row, type='w'):
	with open(fpath, type, newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(row)
		file.close()
def getrow(tweet):
	row = []
	row.append(tweet.get("id"))
	row.append(tweet.get("text"))
	row.append(tweet.get("author_id"))
	row.append(tweet.get("created_at"))
	row.append(tweet.get("in_reply_to_user_id"))
	row.append(tweet.get("geo"))
	row.append(tweet.get("lang"))
	if tweet.get("public_metrics") is not None:
		if tweet.get("public_metrics").get("retweet_count") is not None:
			row.append(tweet.get("public_metrics").get("retweet_count"))
		else:
			row.append(None)
		if tweet.get("public_metrics").get("reply_count") is not None:
			row.append(tweet.get("public_metrics").get("reply_count"))
		else:
			row.append(None)
		if tweet.get("public_metrics").get("like_count") is not None:
			row.append(tweet.get("public_metrics").get("like_count"))
		else:
			row.append(None)
		if tweet.get("public_metrics").get("quote_count") is not None:
			row.append(tweet.get("public_metrics").get("quote_count"))
		else:
			row.append(None)
	else:
		row.append(None)
		row.append(None)
		row.append(None)
		row.append(None)
	return row
premium_search_args = load_credentials("./twitter_keys.yaml",
                                       yaml_key="search_tweets_v2_academic",
                                       env_overwrite=False)
query = gen_request_parameters(SEARCH_QUERY, results_per_call=RESULTS_PER_CALL,
	tweet_fields=TWEET_FIELDS,
	start_time=FROM_DATE, end_time=TO_DATE)
print(query)
header = ['id', 'text', 'author_id', 'created_at', 'in_reply_to_user_id',
					'geo', 'lang', 'public_metrics.retweet_count',
					'public_metrics.reply_count', 
					'public_metrics.like_count', 'public_metrics.quote_count']
writecsv(FILENAME+".csv", header)
'''rs = ResultStream(request_parameters=query,
                    max_results=500,
                    **premium_search_args)
print(rs)
tweets = list(rs.stream())
next_token = rs.next_token
print("\n-----\nnext_token: " + next_token + "\n-----\n")
print(tweets[0].get("id"))
page = 1
print("page: ", page)
for tweet in tweets:
	row = getrow(tweet)
	writecsv(FILENAME+".csv", row, type='a')'''
page = 0
nexts = []
next_token = '0'
while next_token is not None:
	try:
		if page == 0: next_token = None
		rs = ResultStream(request_parameters=query,
                    max_results=500,
                    **premium_search_args, next_token=next_token)
		tweets = list(rs.stream())
		print(len(tweets))
		next_token = rs.next_token
		nexts.append(next_token)
		print("\n-----\nnext_token: " + next_token + "\n-----\n")
		print(tweets[0].get("id"))
		page += 1
		print("page: ", page)
		for tweet in tweets:
			row = getrow(tweet)
			writecsv(FILENAME+".csv", row, type='a')
		print("wait for 6 seconds")
		time.sleep(6)
	except:
		print("error")
		break
# Reading the csv file
pcsv = pd.read_csv(FILENAME + '.csv')

# saving xlsx file
excel = pd.ExcelWriter(FILENAME + '.xlsx')
pcsv.to_excel(excel, index=False)

excel.save()

print('done')