import hyperonym_patterns.fast_checker as fast_checker


def get_context(ocurrence):
    lc = ocurrence["LeftContext"].to_string(index=False)
    pivot = ocurrence["occurrence"].to_string(index=False)
    rc = ocurrence["RightContext"].to_string(index=False)
    context = lc + pivot + rc
    return context


def create_annotation_file(annotated_file, sep, marc_id, corpus, cm_type):
    """
    :param annotated_file: new file name with annotations
    :param sep:
    :param marc_id: pretraited file name
    :return:
    """
    all_contexts = []
    data = fast_checker.build_df_from_data(annotated_file, sep)
    meta = add_id(marc_id, data["occurrence"], corpus, cm_type)
    subids = meta[1]
    data["id"] = meta[0]
    data["subid"] = subids
    data["topic"] = meta[2]
    data["relational_semantic_type"] = meta[3]
    for i in range(0, len(subids)):
        row = data[data["subid"] == subids[i]]
        context = get_context(row)
        if context:
            all_contexts.append(context)
        else:
            all_contexts.append(None)
    data["full_context"] = all_contexts
    filtered_data = data[['id', 'subid', 'topic', 'relational_semantic_type','presence', 'candidate_term_left', 'candidate_term_right', 'Pivot','occurrence', 'full_context']]
    filtered_data.to_csv(annotated_file, index=False)
    return filtered_data


def add_id(marc_id, data, corpus, cm_type):
    ids = []
    subids = []
    topics = []
    cm_types = []
    for i in range(0, len(data)):
        subids.append(f"{marc_id}_{i + 1}")
        ids.append(f"{marc_id}")
        topics.append(f"{corpus}")
        cm_types.append(f"{cm_type}")
    return ids, subids, topics, cm_types


def calPercent(x, y, integer = False):
   percent = x /  100 * y
   if integer:
       return int(round(percent))
   return round(percent)

def annotate(annotation_dict, occ_id, annotation):
    parsing_annotations = {'1': 'NON',
                           '2': 'OUI',
                           '3': 'PLUTÔT OUI',
                           '4': 'PLUTÔT NON',
                           '5': 'INDETERMINE'}
    annotation_dict.update({occ_id : parsing_annotations[annotation]})
    return annotation_dict
