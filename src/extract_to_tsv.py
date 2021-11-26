import os
import argparse
import json
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-n', '--num_posts', type=int, default=1000)

    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        lines = f.readlines()

    max = args.num_posts if args.num_posts <= len(lines) else len(lines)

    posts = random.sample(lines, max)

    result = ['id\ttweet\tcoding\n']
    for post in posts:
        p = json.loads(post)
        text = p['text']
        text = text.replace('\n', ' ').replace('\t', ' ')
        result.append(f'{p["id"]}\t{text}\t\n')

    with open(args.output, 'w', encoding='utf-8') as f:
        f.writelines(result)


if __name__ == '__main__':
    main()
