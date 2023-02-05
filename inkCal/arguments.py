import argparse

def get():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="warning", help="Log level, INFO, WARN, ERROR, DEBUG.")
    return parser.parse_args()
