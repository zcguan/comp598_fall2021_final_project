import os
from dotenv import load_dotenv
import argparse
import json
import time
import requests

BASE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.join(BASE_DIR, '..')
ENV_PATH = os.path.join(PARENT_DIR, '.env')

load_dotenv(ENV_PATH)

def auth_headers():
    """
    return headers to access Twitter API
    """
    bearer_token = os.getenv('BEARER_TOKEN')
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def get_response(url, headers, params, next=None):
    if next:
        params['next_token'] = next
    response = requests.get(url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-n', '--total', type=int)
    args = parser.parse_args()

    # minimum tweets is 10
    if args.total < 10:
        args.total = 10

    endpoint_url = 'https://api.twitter.com/2/tweets/search/recent'

    keyword = '(covid OR covid19 OR coronavirus OR vaccination OR pfizer OR moderna OR astrazeneca) lang:en -is:retweet'
    start_time = '2021-11-20T00:00:00.000Z'
    end_time = '2021-11-23T00:00:00.000Z'
    max_results = 100 if args.total > 100 else args.total
    params = {
        'query': keyword,
        'start_time': start_time,
        'end_time': end_time,
        'max_results': max_results,
        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
        'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
        'user.fields': 'id,name,username,location,created_at,description,public_metrics,verified',
        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
        'next_token': {}
    }
    headers = auth_headers()
    response = get_response(endpoint_url, headers=headers,
                            params=params)
    
    # return the entire response
    # with open(args.output, 'w') as f:
    #     json.dump(response, f)
    # return

    count = 0
    next_token = None
    result = []
    while count < args.total:
        # reduce max_result if the next request will exceed the total
        # can differ up to 9 tweets
        if count + max_results > args.total:
            max = args.total - count
            params['max_results'] = max if max > 10 else 10

        response = get_response(endpoint_url, headers=headers, params=params, next=next_token)
        result_count = response['meta']['result_count']

        if 'next_token' in response['meta']:
            # Save the token to use for next call
            next_token = response['meta']['next_token']
            if result_count is not None and result_count > 0 and next_token is not None:
                result += response['data']
                count += result_count
                time.sleep(5)
        # If no next token exists
        else:
            if result_count is not None and result_count > 0:
                result += response['data']
                count += result_count
            break

        print(f'tweets fetched: {count}')
        time.sleep(5)

    print(f'total tweets fetched: {count}')
    
    with open(args.output, 'w', encoding='utf-8') as f:
        for tweet in result:
            f.write(json.dumps(tweet) + '\n')

if __name__ == '__main__':
    main()
