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

    result = ['id\tmetrics\ttweet\tcoding\tsentiment\n']
    for post in posts:
        p = json.loads(post)
        text = p['text']
        text = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        context = json.dumps(p['context_annotations']) if 'context_annotations' in p else ''
        result.append(f'{p["id"]}\t{json.dumps(p["public_metrics"])}\t{text}\t\t\n')

    with open(args.output, 'w', encoding='utf-8') as f:
        f.writelines(result)


if __name__ == '__main__':
    main()
