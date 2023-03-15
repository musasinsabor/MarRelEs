import pandas as pd
import re

freq = dict()
data = pd.read_csv("First_vertion_marrel.csv")
data = data.dropna(subset=["id"])
spanish_patterns = data["sp_pattern"]
french_patterns = data["fr_pattern"]
data["variables"] = " "
for i in range(0, len(spanish_patterns)):
    lexical_mar = re.findall(r"{(.*)}", spanish_patterns[i])
    if lexical_mar:
        data["variables"][i] = lexical_mar
        for mar in lexical_mar:
            freq[mar] = freq.get(mar, 0) + 1

data.to_csv("spanish_patterns.csv", index=False)
liste = sorted(freq, key=freq.get, reverse=True)
for mot in liste:
    if freq[mot] > 1:
        print(mot, freq[mot], sep="\t")

