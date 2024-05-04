import pandas as pd
import re

freq = dict()
data = pd.read_csv("spanish_patterns.csv")
data = data.dropna(subset=["id"])
data.where(data.notnull(), None)
spanish_patterns = data["sp_pattern"]

# french_patterns = data["fr_pattern"]
ext_variables = list(data["extended_variables"])
ori_variables = list(data["original_variables"])
for i in range(0, len(spanish_patterns)):
    try:
        if pd.isna(ext_variables[i]):
            var = list(ori_variables[i].split(","))
            for o_var in var:
                if "'" not in o_var:
                    # print([f'{o_var}'])
                    o = str([f'{o_var}'])
                    freq[o] = freq.get(o, 0) + 1
                else:
                    freq[o_var] = freq.get(o_var, 0) + 1
            #     print(o_var, type(var), ori_variables[i])
        else:
            # for e_var in ext_variables[i]:
            # freq[ext_variables[i]] = freq.get(ext_variables[i], 0) + 1
            var = list(ext_variables[i].split(","))
            for e_var in var:
                if "'" not in e_var:
                    # print([f'{o_var}'])
                    e = str([f'{e_var}'])
                    freq[e] = freq.get(e, 0) + 1

                # print(e_var, type(var), ext_variables[i])
                else:
                    freq[e_var] = freq.get(e_var, 0) + 1
    except:
        pass

# for t in freq:
#     print(t, freq[t], sep="\t")
# print(ext_variables[i])
# for var in mar:
#         freq[var] = freq.get(var, 0) + 1
#
data.to_csv("spanish.csv", index=False)
liste = sorted(freq, key=freq.get, reverse=True)
n = 0
for mot in liste:
    n = n + freq[mot]
    print(mot, freq[mot], n, sep="\t")
