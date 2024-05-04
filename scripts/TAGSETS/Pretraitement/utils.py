import re
def parsing_in_patterns(patterns):
    elements = []
    for pattern in patterns:
        try:
            determinants = re.sub('DET indefinido|DET definido|DET', '[spanishpos="ART"]', pattern)
            XYelement = re.sub('X|Y', '[spanishpos="NC|NMON|NMEA|NP"]?[]{0,3}', determinants)
            slash = re.sub('\/', '|', XYelement)
            if re.search('ser', slash):
                sub_verb_be = re.sub('ser', '[spanishpos="VS.*"]', slash)
                elements.append(sub_verb_be)
            else:
                elements.append(slash)
        except:
            elements.append(pattern)
    return elements