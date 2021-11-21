import os
from dotenv import load_dotenv
import argparse
import json
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

def get_response(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    endpoint_url = 'https://api.twitter.com/2/tweets/search/recent'

    keyword = ''
    start_time = '2021-11-17T00:00:00.000Z'
    end_time = '2021-11-20T00:00:00.000Z'
    max_results = 100
    params = {
        'query': keyword,
        'start_time': start_time,
        'end_time': end_time,
        'max_results': max_results,
        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
        'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
        'next_token': None
    }

    headers = auth_headers()

    json_response = get_response(endpoint_url, headers=headers, params=params)

if __name__ == '__main__':
    main()
