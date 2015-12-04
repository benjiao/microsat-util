import os
import argparse
from microsat_util import georef

def get_arguments():
    parser = argparse.ArgumentParser(description="Geo Reference an Image")
    parser.add_argument('input_filename', help='the file to be processed')
    args = parser.parse_args()

    return args

def main():
    args = get_arguments()
    print georef.process(args.input_filename)