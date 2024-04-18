import json
import pandas as pd
import argparse

def translation_types(df, dict_translation):
    types = df["type"]
    new_types = []
    # Iterate in "type" values
    for c_type in types:
        # Verify and replace value
        if c_type in dict_translation:
            new_types.append(dict_translation[c_type])
        else:
            # If not that value, keep it the same
            new_types.append(c_type)

    # replace the values
    df["type"] = new_types
    return df

if __name__ == "__main__":
    # args parser config
    xparser = argparse.ArgumentParser(description="Process txt files in a directory.")
    xparser.add_argument(
        "data", help="Path to the directory containing the csv file with the data"
    )
    xparser.add_argument(
        "type_translated",
        help="Path to the file containing the json file with the data translated",
    )
    # args parser
    args = xparser.parse_args()
    df = pd.read_csv(args.data)
    with open(args.type_translated) as file2:
        d = json.load(file2)

    new_df = translation_types(df, d)


