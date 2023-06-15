from fast_checker import *
import sys

"""Candidate-term projection in the corpus results"""

if len(sys.argv) != 4:
    quit("usage : CTprojection.py corpus path cm_id")

if __name__ == "__main__":
    ctclass = CTProjection(sys.argv[1])
    projection = ctclass.ct_projection(sys.argv[2], sys.argv[3])
    print(projection)
