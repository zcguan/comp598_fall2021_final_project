import argparse
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        with open(args.output, 'w', encoding='utf-8') as o:
            for line in f:
                line = line.split('\t')
                # if len(line) < 6:
                #     print(line)
                #     return
                text = line[3]
                text = re.sub(r'\bhttps:.*\b', '', text)
                text = re.sub(r'\s+', ' ', text)
                # re.sub(r'\W+', ' ', text)
                # words = text.split()
                o.write(text+'\n\n')

            


if __name__ == '__main__':
    main()
