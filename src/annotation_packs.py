import pandas as pd
import math
import argparse
import json
import spanish_translate

def create_samples(data, sample_size=100, random_state=42):
    """
    Create multiple samples from a DataFrame.

    Parameters:
    - data (pd.DataFrame): The original DataFrame.
    - sample_size (int): The number of rows in each sample.
    - num_samples (int): The number of samples to create.
    - random_state (int): Seed for random state to ensure reproducibility.

    Returns:
    - samples (list): List of DataFrames, each representing a sample.
    - remaining_data (pd.DataFrame): DataFrame after removing selected rows.
    """

    # Copy the original DataFrame to avoid modifying the input
    preprocessed_data = data.copy()

    # List to store the samples
    samples = []

    # Iteratively create samples
    len_av = len(data) / sample_size
    num_samples = math.floor(len_av)
    for _ in range(num_samples):
        # Get a random sample from the DataFrame
        sample = preprocessed_data.sample(n=sample_size, random_state=random_state)

        # Add the sample to the list
        samples.append(sample)

        # Remove the selected rows from the original DataFrame
        preprocessed_data = preprocessed_data.drop(sample.index)

    # Return the list of samples and the remaining data
    return samples, preprocessed_data


def annotation_lots(ann_data):
    """
    Creation des lots d'annotation
    :param ann_data: data path to the csv file
    :return:
    """
    rest = dict()
    lots = dict()
    fields = list(pd.unique(ann_data["field"]))
    for field in fields:
        filted_data = ann_data.loc[ann_data["field"].str.contains(field)]
        samples, remaining_data = create_samples(filted_data)
        rest[f"{field}_rest"] = remaining_data
        lots[f"{field}"] = samples
    all_rest_df = []
    for df in rest.values():
        all_rest_df.append(df)
    df_concat = pd.concat(all_rest_df)
    rest_samples, remaining_data_last = create_samples(df_concat)
    lots["mix"] = rest_samples
    return remaining_data_last, lots


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
    ## translation subrelation
    with open(args.type_translated) as file2:
        d = json.load(file2)

    new_df = spanish_translate.translation_types(df, d)

    ## changes in data
    new_df["relation"] = "meronimia"
    new_df.rename(columns={"type": "subrelation"}, inplace=True)
    df_subset = new_df.loc[:, ["relation", "subrelation", "field", "context", "sentence"]]

    rem, lots = annotation_lots(df_subset)
    print("Lots created")
    for k, v in lots.items():
        for i in range(0, len(v)):
            file_name = f"data/data_annotation/{k}_{i+1}_data.xlsx"
            v[i].to_excel(file_name, index=False)
    print("Lots saved")