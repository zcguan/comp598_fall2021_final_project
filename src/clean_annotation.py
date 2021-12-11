import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-r', '--remain')

    args = parser.parse_args()

    df = pd.read_csv(args.input, sep='\t')

    if not df[df['sentiment'].isnull() & df['coding'].notnull()].empty:
        print('rows with missing sentiment:')
        print(df[df['sentiment'].isnull() & df['coding'].notnull()])
        return

    if not df[df['sentiment'].notnull() & df['coding'].isnull()].empty:
        print('rows with missing coding:')
        print(df[df['sentiment'].notnull() & df['coding'].isnull()])
        return
    
    annotated = df[df['sentiment'].notnull() & df['coding'].notnull()]
    annotated.to_csv(args.output, sep='\t', index=False)

    if args.remain:
        remain = df.loc[df.index.difference(annotated.index)]
        remain.to_csv(args.remain, sep='\t', index=False)

if __name__ == '__main__':
    main()
