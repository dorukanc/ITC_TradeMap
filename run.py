from functools import reduce
import spider
from parser import remake
from toJson import toJson
import pandas as pd
import json
from setlog import setlog

logging = setlog()

__version__ = '1.0'


'''
Execution steps:
1. Web scraping
2. Parsing
3. Converting to JSON
'''

# Login credentials
ac = "chroma.favours@icloud.com"
pw = "PKNrKASJRZzYt4?*=)"
pdir = "./pickle/"  # Directory for storing pickle files

# Records and Indicators: Placeholder arrays for exporting/importing data
Records = Indicators = [1, 2]  # Both Records and Indicators arrays are set as [1, 2]
recs = ["ex", "im"]  # Labels for export (ex) and import (im)
inds = ["val", "qty"]  # Labels for values (val) and quantities (qty)

# List of product codes
products = ["020711", "020712", "020714", "040700"]  # Product codes for scraping
options = [[3, 10, 10], [4], [5], [1, 5, 12, 10]]  # Options for selecting different products in the spider

# Initialize the web scraper (spider)
s = spider.TradeSpider()

try:
    s.setDriver()  # Set up the web driver for automation
    s.login(ac, pw)  # Log in using the provided credentials
    s.setTimePage()  # Set up the time page for data collection

    # Initialize product index
    p = 0

    # Loop through products and scrape data
    for index, o in enumerate(options):
        for n in o:
            s.selectProducts(n)  # Select the product based on the options provided

        # Loop through records and indicators to scrape data
        for r in Records:
            for i in Indicators:

                # Set records and indicators in the scraper
                s.setRecords(r)
                s.setIndicators(i)
                s.save(pdir + str(p))  # Save the scraped data as a pickle file

                # Load and parse the saved data
                df = pd.read_pickle(pdir + str(p) + '.pickle')  # Load the data as a pandas DataFrame
                value_header = "{}_{}".format(recs[r-1], inds[i-1])  # Create a header for the values based on the record and indicator
                item = products[index]  # Get the current product code

                # Parse and reformat the data using the remake function
                re_df = remake(df, item, value_header)
                re_df.to_pickle(pdir + str(p) + '.pickle')  # Save the parsed data as a pickle file
                p += 1  # Increment the product index

finally:
    s.close()  # Ensure that the web scraper is closed properly

# Merge and concatenate the data

n = 16  # Number of data frames to process (4 products x 2 records x 2 indicators)
df_all = pd.DataFrame()  # Initialize an empty DataFrame to hold all the data

# Merge every four data frames and concatenate the result into df_all
for x in range(0, n, 4):
    data_frames = [
        pd.read_pickle(pdir + str(i) + '.pickle') for i in range(x, x + 4)
    ]

    # Merge the data frames on specific columns and fill missing values with 0.0
    df_merge = reduce(lambda left, right: pd.merge(left, right, on=["country_a", "country_b", "date", "item_no"],
                                                   how='outer'), data_frames).fillna(0.0)
    df_all = pd.concat([df_all, df_merge])  # Concatenate the merged data into df_all

# Convert the transaction records to a pandas DataFrame
df_all.to_pickle(pdir + "df_all.pickle")  # Save the complete DataFrame as a pickle file

# Convert the DataFrame to JSON
jsonData = toJson(df_all)
with open("map_result.json", "w") as file:  # Write the JSON data to a file
    file.write(json.dumps(jsonData, ensure_ascii=False, indent=2))