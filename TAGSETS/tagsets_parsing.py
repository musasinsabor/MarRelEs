def get_tagset(lexique_path):
    fichier_lexique = open(lexique_path, mode="r")
    tags = dict()
    tags_list = []
    for ligne in fichier_lexique:
        ligne = ligne.rstrip("\n")
        try:
            l = ligne.split("\t")
            tags_list.append(l[0])
            # tags[l[0]]={l[0]:l[1]}
        except:
            l = ligne.split(" ")
            tags_list.append(l[0])
    fichier_lexique.close()
    return tags_list

def get_tagsetx(lexique_path):
    fichier_lexique = open(lexique_path, mode="r")
    tags = dict()
    for ligne in fichier_lexique:
        ligne = ligne.rstrip("\n")
        try:
            l = ligne.split("\t")
            tags[l[0]]={l[0]:l[1]}
        except:
            l = ligne.split(" ")
            tags[l[0]] = {l[1]: l[0]}
    fichier_lexique.close()
    return tags


def create_tagset(tagset1, tagset2):
    full_tagset1 = get_tagset(tagset1)
    full_tagset2 = get_tagset(tagset2)
    for i in range(0, len(full_tagset2)):
        if full_tagset2[i] in full_tagset1[i]:
            print(full_tagset2[i])


spanish_ts = create_tagset("TAGSETS/spanish-tagset.txt","TAGSETS/Tagset FR.txt")

# for t in t3:
#     if t not in lexique:
#         print(t)
print(spanish_ts)