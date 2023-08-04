#James Carton
#April 2nd, 2023
import argparse

parser = argparse.ArgumentParser(description='Count lines in a text file.')
parser.add_argument('filename', help='Path to the text file')
parser.add_argument('-v', '--verbose', action='store_true', help='Print each line')

args = parser.parse_args()

line_count = 0

with open(args.filename, 'r') as f:
    for line in f:
        if args.verbose:
            print(line.strip())
        line_count += 1

print(f'Total lines: {line_count}')
