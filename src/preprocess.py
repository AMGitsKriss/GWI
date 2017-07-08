import pandas as pd
import numpy as np

# Loading the file. If not csv, assumes hdf
def load_data(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, index_col=0)
    else:
        return pd.read_hdf(filename, key='df')

# Return a version of the dataset with only the first occurence of each row
def drop_duplicates(dataset):
    return dataset.groupby(dataset.index).nth(0) 

# Save the dataframe. duh.
def save_dataframe(dataset, filename):
    try:
        dataset.to_csv(filename)
    except IOError:
        print("<Error writing file> Is it already open?")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Path to a CSV or HDF file')
    args = parser.parse_args()
    df = load_data(args.filename)

    # Note - You specified to drop duplicates before you specified to drop NaNs. 
    # If there are two rows for a respondant, and the first one contains a NaN, both will be dropped.
    df = drop_duplicates(df)
    df = df.dropna(subset=['q2', 'q4'])

    save_dataframe(df, "dropped_"+args.filename)

if __name__ == '__main__':
    main()
