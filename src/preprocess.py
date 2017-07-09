import pandas as pd
import numpy as np

# Loading the file. If not csv, assumes hdf
def load_data(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, index_col=0)
    else:
        return pd.read_hdf(filename, key='df')

# Load the specified file as a series (squeeze), then name it q3 so it's easy to merge.
def load_series(filename):
    return pd.read_csv(filename, index_col=0, squeeze=True, names=["q3"])

# Return a version of the dataset with only the first occurence of each row
def drop_duplicates(dataset):
    return dataset.groupby(dataset.index).nth(0) 

# Save the dataframe. duh.
def save_dataframe(dataset, filename):
    try:
        dataset.to_csv(filename)
    except IOError:
        print("<Error writing file> Is it already open?")

# Merge new data into the existing dataframe by appending columns, not rows.
def merge_new(dataset, new_column):
    return pd.concat([dataset, new_column], axis=1)

def main():
    # Borrowing this from the code you sent me
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dfname', help='Path to a dataframe CSV or HDF file')
    parser.add_argument('seriesname', help='Path to a series CSV file')
    args = parser.parse_args()

    #Load main table, drop the duplicates, then drop the NaNs
    df = load_data(args.dfname)
    df = drop_duplicates(df)
    df = df.dropna(subset=['q2', 'q4'])

    #Load the q3 series and add it to the main dataframe
    q3 = load_series(args.seriesname)
    df = merge_new(df, q3)

    # Validate that the data structures were merged completely before saving
    if(df.q3.count() == q3.count()):
        save_dataframe(df, "complete.csv")
        print("Done!")
    else:
        print("The q3 values weren't copied correctly.")

if __name__ == '__main__':
    main()
