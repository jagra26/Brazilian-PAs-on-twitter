import requests
import os
import json
import time
import variables as var
import glob
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = var.bearer_token
search_url = var.search_url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    headers = create_headers(bearer_token)
    end = False
    begin = True
    start = var.start
    end = var.end
    folder_name = start[0:10] + "_" + end[0:10]
    path = var.path + folder_name
    if not os.path.exists(path):
        os.mkdir(path)
    files = glob.glob(path+"/*")
    for f in files:
        os.remove(f)
    page = 0
    while True:
        filename = "/" + str(page) + '.txt'
        if begin:
            next_token = None
            begin = False
        # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        query_params = {'query': var.query, 'tweet.fields': var.tweet_fields, 'start_time': start, 'end_time': end,
        'max_results': var.max_results, 'next_token': next_token, 'user.fields': var.user_fields,
        'place.fields': var.place_fields, 'expansions': var.expansions}
        json_response = connect_to_endpoint(search_url, headers, query_params)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        with open(path + filename, 'w') as file:
            json.dump(json_response, file, indent=4, sort_keys=True)
            file.close()
        if json_response['meta'].get('next_token') is None:
            break
        else:
            next_token = json_response['meta']['next_token']
        print("wait 10 seconds")
        time.sleep(10)
        page += 1

if __name__ == "__main__":
    main()