from fast_checker import *
import sys

if len(sys.argv)!=3:
    quit("usage : test_checker.py corpus element")

if __name__ == "__main__":
    test = CTProjection(sys.argv[1])
    if sys.argv[2] in test.set_terms_extended:
        print("yes")
    else:
        print("nope")

