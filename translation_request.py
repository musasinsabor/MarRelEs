import re
import pandas as pd

tags = pd.read_csv('metadata.csv')
spanish_tags = list(tags["spanish"])
french_tags = list(tags["french"])
tagsets = dict()
for i in range(0, len(french_tags)):
    try:
        item = tagsets.get(french_tags[i])
        new = item+"|"+spanish_tags[i]
        tagsets[french_tags[i]] = new
    except:
        tagsets[french_tags[i]] = spanish_tags[i]
requests = pd.read_csv('request.csv')
french_requests = requests["TXM requete"]
spanish_requests = french_requests.copy()
for i in range(0, len(spanish_requests)):
    for k,v in tagsets.items():
        langue = re.sub("fr", "spanish", spanish_requests[i])
        subs = re.sub(k, str(v), langue)
        spanish_requests[i] = subs

list(spanish_requests)
# print(spanish_requests)
requests["spanish requests"] = spanish_requests
requests.to_csv("spanish_request.csv")