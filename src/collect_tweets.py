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


def get_params(keyword, start, end, max):
    params = {
        'query': keyword,
        'start_time': start,
        'end_time': end,
        'max_results': max,
        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
        'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source,context_annotations',
        'user.fields': 'id,name,username,location,created_at,description,public_metrics,verified',
        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
        'next_token': {}
    }
    return params

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-n', '--num_tweets', type=int)
    args = parser.parse_args()

    # minimum tweets is 10
    if args.num_tweets < 10:
        args.num_tweets = 10

    endpoint_url = 'https://api.twitter.com/2/tweets/search/recent'

    # keywords containing covid, vaccinations, and vaccine brands. Only original tweets
    keyword = '(covid OR covid19 OR coronavirus OR vaccination OR pfizer OR moderna OR astrazeneca) lang:en -is:retweet -is:reply -is:quote'
    start_periods = ['2021-11-23T00:00:00.000Z', '2021-11-24T00:00:00.000Z', '2021-11-25T00:00:00.000Z']
    end_periods = ['2021-11-24T00:00:00.000Z', '2021-11-25T00:00:00.000Z', '2021-11-26T00:00:00.000Z']
    max_results = 100 if args.num_tweets > 100 else args.num_tweets  # maximum 100 per request
    
    headers = auth_headers()

    total_count = 0
    result = []
    i = 0
    while i < len(start_periods):
        sub_count = 0
        start_time = start_periods[i]
        end_time = end_periods[i]
        next_token = None
        print('-'*100)
        print(f'collecting tweets from {start_time} to {end_time}')

        while sub_count < args.num_tweets:
            # reduce max_result if the next request will exceed the total count for this period
            # can differ up to 9 tweets
            if sub_count + max_results > args.num_tweets:
                max = args.num_tweets - total_count
                max_results = max if max > 10 else 10

            params = get_params(keyword, start_time, end_time, max_results)
            response = get_response(endpoint_url, headers=headers, params=params, next=next_token)
            result_count = response['meta']['result_count']

            if 'next_token' in response['meta']:
                # Save the token to use for next call
                next_token = response['meta']['next_token']
                if result_count is not None and result_count > 0 and next_token is not None:
                    result += response['data']
                    sub_count += result_count
                    total_count += result_count
                    time.sleep(5)
            # If no next token exists
            else:
                if result_count is not None and result_count > 0:
                    result += response['data']
                    sub_count += result_count
                    total_count += result_count
                break

            print(f'fetched: {result_count}')
            time.sleep(5)

        print(f'{sub_count} tweets fetched for the period from {start_time} to {end_time}')
        print('-'*100)
        i += 1

    print(f'total tweets fetched: {total_count}')
    
    with open(args.output, 'w', encoding='utf-8') as f:
        for tweet in result:
            f.write(json.dumps(tweet) + '\n')

if __name__ == '__main__':
    main()
