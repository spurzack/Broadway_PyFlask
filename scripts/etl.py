import pandas as pd
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-eo",
        "--extract-only",
        help="Will not load data into DynamoDB",
        action="store_true"
    )

    args = parser.parse_args()
    return args



def main():
    args = parse_args()
    print(args)
    if args.extract_only:
        print("Success!")


if __name__ == "__main__":
    main()
