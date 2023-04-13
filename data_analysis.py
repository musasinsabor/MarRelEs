import hyperonym_patterns.fast_checker as fast_checker

def pivot_elements(pivots):
    full_tags_list = []
    for pivot in pivots:
        words = []
        tags = []
        lemmas = []
        try:
            element = pivot.split( )
            for e in element:
                sub_e = e.split("_")
                words.append(sub_e[0])
                tags.append(sub_e[1])
                lemmas.append(sub_e[2])
            occ_tag = " ".join(tags)
            full_tags_list.append(occ_tag)
            words = []
            tags = []
            lemmas = []
        except:
            full_tags_list.append(pivot)
    return full_tags_list

def freq_elements(elements):
    freq=dict()
    for element in elements:
        try:
            freq[element] = freq.get(element, 0) + 1
        except:
            e = " ".join(element)
            freq[e] = freq.get(e, 0) + 1
    return freq


def freq_tags(tags):
    freqs = []
    all_freq_tags = freq_elements(tags)
    for tag in tags:
        freqs.append(all_freq_tags.get(tag, 0))
    return freqs


def variables_creation(path, sep=','):
    df = fast_checker.build_df_from_data(path, sep)
    tags = pivot_elements(df['Pivot'])
    df["tags"] = tags
    full_freq_tags = freq_tags(tags)
    df["global_freq"] = full_freq_tags
    df.to_csv(path, index=False)
    return df


def assisted_annotation(path, annotated_data, subcorpus, cmid):
    new_annotation = []
    df = fast_checker.build_df_from_data(path, sep=",")
    all_df = fast_checker.build_df_from_data(annotated_data, sep=",")
    oui_annotation = all_df[(all_df["annotation"] == "« OUI »") & (all_df["topic"] == subcorpus) & (all_df["id"] == cmid)]
    oui_annotation = oui_annotation.reset_index(drop=True)
    oui_pivots = set(oui_annotation["Pivot"])
    uu = None
    for new_pivot in list(df["Pivot"]):
        if new_pivot in oui_pivots:
            new_annotation.append('« OUI »')
        else:
            for i in range(0, len(oui_annotation["Pivot"])):
                if i == len(oui_annotation["Pivot"])-1:
                    if new_pivot in oui_annotation["Pivot"][i]:
                        uu = True
                    if uu == True:
                        new_annotation.append('« OUI »')
                    else:
                        new_annotation.append('« NON »')
                    uu= None
                elif new_pivot in oui_annotation["Pivot"][i]:
                    uu = True
                else:
                    pass
    df["annotation"] = new_annotation
    tags = pivot_elements(df['Pivot'])
    df["tags"] = tags
    full_freq_tags = freq_tags(tags)
    df["global_freq"] = full_freq_tags
    df.to_csv(path, index=False)
    print(f'annotated data saved in {path}')
    return df
