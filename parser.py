from matplotlib.cbook import flatten
import pandas as pd

def parser_row_val(df, row_no, item_no):
    '''
    Parses data from each row of a DataFrame and converts trade volumes to kilograms.

    Parameters:
    df (DataFrame): The DataFrame obtained from reading an HTML table using pd.read_html.
    row_no (int): The row number in the HTML table to parse.
    item_no (str): The product item number.

    Returns:
    allrow (list): A list of lists containing parsed and converted data for the specified row.
    '''
    
    # Function to convert units to kilograms or standardized units
    def unit_transform(arg):
        if (arg[0] == "0") or (arg[0] == 'No Quantity'):
            return 0.0  # If the quantity is 0 or 'No Quantity', return 0.0
        elif arg[1] == "Tons":
            return float(arg[0]) * 907.18474  # Convert tons to kilograms
        elif arg[1] == "Pounds":
            return float(arg[0]) * 0.45359237  # Convert pounds to kilograms
        elif arg[1] == "Hundreds units":
            return float(arg[0]) * 100  # Convert hundreds of units to actual units
        elif arg[1] == "Thousands units":
            return float(arg[0]) * 1000  # Convert thousands of units to actual units
        elif arg[1] in ["Dozens", "Heads"]:
            return 0.0  # Return 0 for non-quantifiable units like Dozens and Heads
        elif arg[1] in ["Kilograms", 'Units', 'Unit', 'Mixed']:
            return float(arg[0])  # If already in standardized units, return the quantity directly

    country_a = "world"  # Default value for the source country
    country_b = df.loc[row_no][1]  # The destination country from the specified row in the DataFrame
    row_val = df.loc[row_no][2:].tolist()  # All data from the row except for the country names

    date_list = df.loc[0][2:].dropna().tolist()  # Extracts date information from the first row
    if "in" in date_list[0]:
        date_list = [x.split("in ")[1] for x in date_list]  # Extract only the date, removing any prefix like "in "
    date_list = list(flatten(zip(date_list, date_list)))  # Duplicate each date to match the format in row_val

    # Parse and convert each value in row_val
    allrow = []
    for i in range(0, len(row_val), 2):
        arg = (row_val[i], row_val[i + 1])  # Each 'arg' is a tuple of quantity and unit
        v = unit_transform(arg)  # Convert the quantity to kilograms or standardized units
        row = [country_a, country_b, item_no, date_list[i], v]  # Construct the parsed row data
        allrow.append(row)  # Add the row data to the list of all rows
    return allrow  # Return the list of parsed and converted rows

def remake(df, item_no, value_header):
    '''
    Processes the DataFrame to clean and reorganize it, returning a new DataFrame with the desired format.

    Parameters:
    df (DataFrame): The DataFrame obtained from reading an HTML table using pd.read_html.
    item_no (str): The product item number, e.g., "020711", "020712".
    value_header (str): Trade information header, e.g., "ex_qty", "im_qty", "ex_val", "im_val".

    Returns:
    df2 (DataFrame): A DataFrame with columns ['country_a', 'country_b', 'item_no', 'date', value_header].
    '''
    
    columns = ['country_a', 'country_b', 'item_no', 'date', value_header]  # Define the new DataFrame's column names

    records = []  # Initialize a list to hold all processed records
    for row_no in range(2, len(df)):  # Start from the third row since the first two rows contain headers
        allrow = parser_row_val(df, row_no, item_no)  # Parse each row in the DataFrame
        for row in allrow:
            records.append(row)  # Add each parsed row to the records list

    df2 = pd.DataFrame.from_records(records, columns=columns)  # Create a new DataFrame from the records list
    return df2  # Return the cleaned and reorganized DataFrame

if __name__ == "__main__":
    df = pd.read_pickle('./pickle/test.pickle')  # Load a DataFrame from a pickle file
    df2 = remake(df, "020712", "im_qty")  # Process the DataFrame for a specific product item and value header
    print(df2)  # Print the resulting DataFrame