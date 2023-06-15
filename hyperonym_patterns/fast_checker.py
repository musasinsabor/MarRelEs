import pandas as pd
import re
import os
import sys

sys.path.append("../")
import manual_annotation


def build_df_from_data(path: str, sep=","):
    """
    Function to create a pandas dataframe from a csv file
    :param path: string with the file path
    :param sep: separator identification to create the pandas dataframe to use in the pd.read_csv()
    :return: pd.DataFrame
    """
    try:
        data = pd.read_csv(path, sep=sep)
        return data
    except:
        data = pd.read_csv(path, engine="python", sep=sep, encoding="utf-8", quoting=3)
        return data


class CTProjection:
    """
    Class to project a list the CT using parsed data with TreeTagger Models Parser with TXM
    """

    def __init__(self, corpus: str):
        """
        :param corpus (str): name with the corpus according to the settings fixed in terminology_settings.
        """
        self.df_terms = None
        self.set_terms = None
        self.set_terms_extended = None
        self.dict_terms = None
        self.corpus = corpus
        self.terminology_settings(self.corpus)
        self.cm_delimiter = None

    def set_dict(self):
        """
        Method to create a with the CT availables
        :return: dict
        """
        terms_candidat = self.df_terms["Candidat de regroupement"]
        terms_variant = self.df_terms["Variantes orthographiques"]
        full_variants = dict()
        for i in range(0, len(terms_variant)):
            var = terms_variant[i].split("___")
            full_variants[terms_candidat[i]] = var
        return full_variants

    def candidate_terms_settings(self, ct_file_path: str):
        """
        set the attributes related with the specific corpus (self.set_terms, self.set_terms_extended and self.dict_terms)
        :param ct_file_path: (str) with a path file to the CT
        """
        self.df_terms = pd.read_csv(ct_file_path, sep="\t", encoding="latin-1")
        self.set_terms = set(
            [term.lower() for term in self.df_terms["Candidat de regroupement"]]
        )
        self.dict_terms = self.set_dict()
        variants = set(element for lst in self.dict_terms.values() for element in lst)
        self.set_terms_extended = self.set_terms | variants

    def get_target_path(self, path, root=False):
        """
        get path from this directory
        :param path:
        :return:
        """
        if root:
            current_dir = os.path.abspath(os.getcwd())
            root_dir = os.path.abspath(os.path.join(current_dir, "../"))
            target_path = os.path.join(root_dir, path)
            return target_path
        else:
            path = path
            target_path = os.path.join(os.path.dirname(__file__), path)
            return target_path

    def terminology_settings(self, corpus):
        """
        Full creation of the CT attributes. From a corpus name, settings the CT with self.candidate_terms_settings()
        :param corpus: string with a value from the available list of spanish (economy or medicine) or a candidate-terms
                        list exported from TermoStats.txt
        """
        if corpus == "economy":
            self.candidate_terms_settings(
                self.get_target_path("candidats_terms_economy.txt")
            )
        elif corpus == "medicine":
            self.candidate_terms_settings(
                self.get_target_path("candidats_terms_medicine.txt")
            )
        else:
            self.candidate_terms_settings(self.get_target_path(corpus))

    def get_cm_delimiter(self):
        """
        Get a parsed dict with the CM delimiters and its type.
        :return:
        """
        marc = build_df_from_data(
            self.get_target_path("marqueurs_hyp.csv", root=True), sep=","
        )
        idd = list(marc["id"])
        el = list(marc["main_element"])
        t = list(marc["type_element"])
        rel = list(marc["relational_semantic_type"])
        delimiters = dict()
        for i in range(0, len(idd)):
            if isinstance(idd[i], str):
                if "," in el[i]:
                    elements = el[i].split(",")
                    p = elements
                    delimiters[idd[i]] = {
                        "element": p,
                        "type": t[i],
                        "relational_semantic_type": rel[i],
                    }
                else:
                    delimiters[idd[i]] = {
                        "element": el[i],
                        "type": t[i],
                        "relational_semantic_type": rel[i],
                    }
        return delimiters

    def patron_parsing(self, path, element, element_type):
        """
        use the concordance output file from TXM to get all the DET X elements
        :param element: main element to separate the CM.
                        Use string if is just one element (Example: "ser") or use a tuple for up-3 elements.
        :param element_type: type of element included in the element parameter.
                        Use "lemma" if it's a lemma and "tag" if it's a tag or a set with tags
        :param path: name file from an TXM output file.
        :return: list with only the nominal groups
        """

        try:
            data = pd.read_csv(
                path, engine="python", sep="\t", encoding="utf-8", quoting=3
            )
            CRC = list(data["Pivot"])
        except:
            data = pd.read_csv(path, sep=",")
            CRC = list(data["Pivot"])
        nominal_groups = []
        nominal_groups_right = []
        for pattern in CRC:
            if element_type == "lemma":
                ng1 = re.search(rf"(.*)( .*_{element})(.*)", pattern)
                if ng1:
                    nominal_groups.append(ng1.group(1))
                    nominal_groups_right.append(ng1.group(3))
                else:
                    pass
            else:
                if isinstance(element, str):
                    ng1 = re.search(rf"(.*)(._{element}_.)(.*)", pattern)
                    if ng1:
                        nominal_groups.append(ng1.group(1))
                        nominal_groups_right.append(ng1.group(3))
                    else:
                        pass
                else:
                    ng1 = re.search(rf"(.*)(._{element[0]}_.)(.*)", pattern)
                    ng2 = re.search(rf"(.*)(._{element[1]}_.)(.*)", pattern)
                    if ng1:
                        nominal_groups.append(ng1.group(1))
                        nominal_groups_right.append(ng1.group(3))
                    elif ng2:
                        nominal_groups.append(ng2.group(1))
                        nominal_groups_right.append(ng2.group(3))
                    if len(element) == 3:
                        ng3 = re.search(rf"(.*)(._{element[2]}_.)(.*)", pattern)
                        if ng3:
                            nominal_groups.append(ng3.group(1))
                            nominal_groups_right.append(ng3.group(3))
                    else:
                        pass
        return nominal_groups, nominal_groups_right

    def pivot_det(self, nominal_groups):
        """
        from a list of nominal groups extracts only the main lemmas
        :param nominal_groups: list with nominal groups.
        :return:
        """

        forms = []
        temporal = ""
        for candidat in nominal_groups:
            for match in re.finditer(
                r"([á|é|í|ó|ú|ü|\w]+)_([A-Z]+|[A-Z]+[a-z]+?)_([á|é|í|ó|ú|ü|\w]+)",
                candidat,
            ):
                lemma = match.group(1)
                temporal = temporal + " " + lemma
            forms.append(temporal)
            temporal = ""
        return forms

    def terms_checker(self, terms_candidats, terms):
        valid_candidats = []
        non_valid_candidats = []
        parsing_summary = []
        candidats = []
        for cand in terms_candidats:
            if cand.lower() in terms:
                valid_candidats.append(cand)
                candidats.append(cand)
                parsing_summary.append(True)
            else:
                non_valid_candidats.append(cand)
                candidats.append(cand)
                parsing_summary.append(False)
        return valid_candidats, non_valid_candidats, parsing_summary, candidats

    def terms_checker2(self, terms_candidats, terms):
        candidats = []
        for cand in terms_candidats:
            cand_cropped = cand.split()
            temporal = [None]
            for taille in range(1, 4 + 1):
                for i in range(0, len(cand_cropped) - taille + 1):
                    cand = cand_cropped[i : i + taille]
                    joined_cand = " ".join(cand)
                    if joined_cand in terms:
                        temporal.append(joined_cand)
            if temporal != [None]:
                temporal = [i for i in temporal if i != None]
            candidats.append(temporal)
            temporal = [None]
        return candidats

    def percentage(self, terms):
        n = 0
        for t in terms:
            if t != [None]:
                n = n + 1
        percentage = 100 * float(n) / float(len(terms))
        return str(percentage) + "%"

    def complete_fast_checker(self, path, lemma, element_type):
        patrons = self.patron_parsing(path, lemma, element_type)
        left_pivots = self.pivot_det(patrons[0])
        right_pivots = self.pivot_det(patrons[1])
        left_checking = self.terms_checker2(left_pivots, self.set_terms_extended)
        print("total occurrences", len(left_checking))
        print(
            "terms in left:",
            self.percentage(left_checking),
        )
        right_checking = self.terms_checker2(right_pivots, self.set_terms_extended)
        print(
            "terms in right:",
            self.percentage(right_checking),
        )
        return left_checking, right_checking, left_pivots, right_pivots

    def patterns_comparison(self, terms_list1, terms_list2):
        terms_silenced_in_list2 = []
        terms_found_in_list1 = set(terms_list1[0][0])
        terms_found_in_list2 = terms_list2[0][0]
        for element in terms_found_in_list2:
            if element not in terms_found_in_list1:
                terms_silenced_in_list2.append(element)
        if len(terms_silenced_in_list2) == 0:
            return (
                f"{len(terms_list1[0][2])} examples found in the first query ({len(terms_list1[0][0])} terms) and "
                f"{len(terms_list2[0][2])} examples found in the second query ({len(terms_list2[0][0])} terms)"
            )
        else:
            return terms_silenced_in_list2

    def presence_parsing(self, terms):
        presence_right_terms = terms[1]
        presence_left_terms = terms[0]
        presence_in_the_two = []
        for i in range(0, len(presence_left_terms)):
            if presence_right_terms[i] != [None] and presence_left_terms[i] != [None]:
                presence_in_the_two.append("both")
            elif presence_right_terms[i] != [None] and presence_left_terms[i] == [None]:
                presence_in_the_two.append("right")
            elif presence_right_terms[i] == [None] and presence_left_terms[i] != [None]:
                presence_in_the_two.append("left")
            else:
                presence_in_the_two.append("none")
        return presence_in_the_two

    def update_data(self, path, terms):
        data = pd.read_csv(path, engine="python", sep="\t", encoding="utf-8", quoting=3)
        presence = self.presence_parsing(terms)
        occurrence = self.pivot_det(data["Pivot"])
        data["presence"] = presence
        data["candidate_term_left"] = terms[0]
        data["candidate_term_right"] = terms[1]
        data["occurrence"] = occurrence
        newpath = re.sub(r"(.+)\.csv", r"\1_annotated.csv", path)
        data.to_csv(newpath, index=False)

    def ct_projection(self, path, cm_id):
        """
        FULL CT projection and saving file as a path_annotated.csv
        :param path: (str) file path with examples. Expected file in .csv
        :param cm_id: (str) CM identification (example: H01)
        :return: pd.DataFrame with CT projections.
        """
        try:
            m = self.get_cm_delimiter()
            checker = self.complete_fast_checker(
                path, m[cm_id]["element"], m[cm_id]["type"]
            )
            print(f"{path} CM projected")
            self.update_data(path, checker)
            newpath = re.sub(r"(.+)\.csv", r"\1_annotated.csv", path)
            try:
                data = manual_annotation.create_annotation_file(
                    newpath,
                    ",",
                    cm_id,
                    self.corpus,
                    m[cm_id]["relational_semantic_type"],
                )
                print(f"{path} saved")
                return data
            except:
                print(
                    f'annotation file non created, try create_annotation_file({newpath}, {","}, {cm_id}, {self.corpus}, {m[cm_id]["relational_semantic_type"]})'
                )
                return checker
        except:
            print(f"{path} something went wrong")
