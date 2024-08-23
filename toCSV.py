import pandas as pd
from collections import defaultdict
import json

folder = "./sample-data/"

def toCSV(df):
    '''
    Input: A pandas DataFrame parsed from ITC Trade Map HTML trade records.
    Output: Data saved in CSV format.
    '''

    # Initialize output structure
    output = []

    # Get mapping from JSON files
    with open(folder + "ch_country_mapping.json", "r") as file:
        country_map = json.load(file)
    with open(folder + "hs_cname_mapping.json", "r") as file:
        cname_map = json.load(file)

    # Values
    df_sum = df.groupby(["item_no", "date", "country_b"]).sum()

    trade_info_fields = ["ex_val", "im_val", "ex_qty", "im_qty"]
    for trade_info in trade_info_fields:
        for index, row in df_sum.iterrows():
            item_no = index[0]
            date = index[1]
            country = country_map[index[2]]
            value = row[trade_info]

            if value > 0:
                output.append([item_no, cname_map[item_no], date, country, trade_info, value])

    # Convert output to DataFrame
    csv_df = pd.DataFrame(output, columns=["Item Number", "Product Name", "Date", "Country", "Trade Info", "Value"])

    return csv_df

if __name__ == "__main__":
    # Load DataFrame from a pickle file
    df = pd.read_pickle(folder + 'df_1015_sample.pickle')

    # Convert DataFrame to CSV format
    csv_df = toCSV(df)
    print(csv_df.head())  # Display the first few rows of the DataFrame

    # Save DataFrame as CSV
    csv_df.to_csv("trade_data.csv", index=False, encoding="utf-8-sig")

