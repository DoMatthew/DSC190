import os
import sys


def main():
    unused_variable = "this variable is assigned but never used anywhere in the code"
    x = None
    if x == None:
        print("Hello from dsc190! This line is intentionally very long to trigger the line-length rule in ruff, which flags lines over 79 characters by default.")


if __name__ == "__main__":
    main()
