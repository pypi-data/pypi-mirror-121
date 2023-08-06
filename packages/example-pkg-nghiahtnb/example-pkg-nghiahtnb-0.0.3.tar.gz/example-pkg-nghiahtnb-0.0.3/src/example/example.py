import argparse


def add_one(number):
    print( number + 1)


if __name__=="__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-n", "--number", type=int)
    args = parse.parse_args()
    number = args.number
    add_one(number)