import sys

#

if __name__ == "__main__":
    tags = [1]
    all_tags = []
    # tags = tags.split(" ")
    for tag in sys.argv[1:]:
        all_tags.append('[spanishpos='+'"'+tag+'"]')

    print("".join(all_tags), sep=" ")