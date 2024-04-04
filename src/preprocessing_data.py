import re
import pandas as pd
import argparse
import glob


def elements_extractor(column):
    """
    Extract both elements tags and tokens from the IULA corpus tagged
    :param column: column name where the data is
    :return: 2 lists (one with tokens and the other with the tags)
    """
    all_sent_tags = []
    all_sent_words = []
    for sentence in column:
        sent_tags = []
        sent_words = []
        elements = sentence.split()
        for element in elements:
            separation = element.split(sep="/")
            if separation[1] == "AMS" and separation[0] == "l":
                sent_words.append("el")
                sent_tags.append(separation[1])
            else:
                sent_words.append(separation[0])
                sent_tags.append(separation[1])
        all_sent_tags.append(sent_tags)
        all_sent_words.append(sent_words)
    return all_sent_words, all_sent_tags


def field_extractor(column):
    """
    From the code used in the text_id, predict its field value using a dict with these equivalences extracted from Brawned
    :param column: column name where the data is
    :return: list with a value as string per type_id
    """
    fields = []
    fields_dict = {
        "e": "economy",
        "m": "medicine",
        "i": "computer_science",
        "a": "environment",
        "d": "law",
        "g": "general",
        "l": "linguistics",
    }
    for text_id in column:
        field = re.search(r"(.*) (\w).*", text_id)
        if field:
            current_field = field.group(2)
            fields.append(fields_dict[current_field])
        else:
            fields.append("unk")
    return fields


def data_format(file_path):
    """
    Transform a file got from Brawnet with data from IULA to a df
    :param file_path: path with the file
    :return: df
    """
    # Define the regex pattern
    pattern = r"(\s\d+).\s+<(.*)>:\s+(.*)##(.*)##(.*)$"
    cm_pattern = r"(.*)\/(.*).txt"
    cm_ext = re.search(cm_pattern, file_path)
    cm = cm_ext.group(2)
    # Open the file and read its contents
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Initialize lists to store extracted information
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []

    # Loop through each line, apply regex pattern, and extract information
    for line in lines:
        match = re.search(pattern, line)
        if match:
            col1.append(match.group(1))
            col2.append(match.group(2))
            col3.append(match.group(3))
            col4.append(match.group(4))
            col5.append(match.group(5))

    fields = field_extractor(col2)
    target_words, target_tags = elements_extractor(col4)
    left_words, left_tags = elements_extractor(col3)
    right_words, right_tags = elements_extractor(col5)
    all_context_tokens = []
    all_sentence_tokens = []
    for i in range(0, len(right_words)):
        context = (
            " ".join(left_words[i])
            + " ".join(target_words[i])
            + " ".join(right_words[i])
        )
        target_sentence = " ".join(target_words[i])
        all_context_tokens.append(context)
        all_sentence_tokens.append(target_sentence)

    # Create a DataFrame from the extracted information
    data = {
        "cm": cm,
        "field": fields,
        "text_id": col2,
        "target_tokens": target_words,
        "target_tags": target_tags,
        "sentence": all_sentence_tokens,
        "context": all_context_tokens,
    }
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    # args parser config
    xparser = argparse.ArgumentParser(description="Process txt files in a directory.")
    xparser.add_argument("directory", help="Path to the directory containing txt files")
    # args parser
    args = xparser.parse_args()

    dirs = glob.glob(f"{args.directory}/*")
    all_data = []
    for path in dirs:
        test = data_format(path)
        all_data.append(test)
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df_sorted = combined_df.sort_values(by='cm')
    combined_df_sorted.to_csv('data/combined_data.csv', index=False)

