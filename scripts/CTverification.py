from fast_checker import *
import sys

"""Candidate-term verification returns 'yes' if the CT is in the list of CT and 'not' if isn't"""

if len(sys.argv) != 3:
    quit("usage : CTverification.py corpus element")

if __name__ == "__main__":
    test = CTProjection(sys.argv[1])
    if sys.argv[2] in test.set_terms_extended:
        print("yes")
    else:
        print("not")
