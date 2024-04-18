import argparse
import pandas as pd


def data_selection_from_variables(df, column, n_values):
    if column == "selection_features":
        # verify the bool data as str
        mask = df.applymap(type) != bool
        d = {True: "TRUE", False: "FALSE"}

        df = df.where(mask, df.replace(d))
        # creation the selection features variable
        df["selection_features"] = df["cm"] + "_" + df["field"]
    # creation dict to get the filtered
    not_filtered_data = set()
    for k, v in df["cm"].value_counts().items():
        if v > n_values:
            pass
        else:
            not_filtered_data.add(k)
    # random selection
    v_uniques = list(df[column].unique())
    selected_rows = {value: pd.DataFrame() for value in v_uniques}
    selected_values = []
    column_values = []
    included = set()
    not_filtered_v_uniques = []
    filtered_v_uniques = []
    for value in v_uniques:
        # Select n_values random rows  for each value in 'column'
        rows_with_value = df[df[column] == value]
        if value[:3] in not_filtered_data:
            selected = rows_with_value
        else:
            selected = rows_with_value.sample(
                min(n_values, len(rows_with_value)), random_state=10, replace=True
            )

        # Include selected rows in the dict
        selected_rows[value] = pd.concat([selected_rows[value], selected])
        column_values.extend([column] * len(selected))

    # Concat all rows
    combined_df = pd.concat(selected_rows.values(), ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["cm", "sentence"])
    return combined_df


if __name__ == "__main__":
    # args parser config
    xparser = argparse.ArgumentParser(description="Process txt files in a directory.")
    xparser.add_argument(
        "data", help="Path to the directory containing the csv file with the data"
    )
    # args parser
    args = xparser.parse_args()
    df = pd.read_csv(args.data)
    random_data = data_selection_from_variables(df, "selection_features", 5)
    random_data.to_csv("data/random_combined_data_filtered.csv", index=False)
    print("random data created", len(random_data))
