import pandas as pd
import numpy as np

# Loading the file. If not csv, assumes hdf
def load_data(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, index_col=0)
    else:
        return pd.read_hdf(filename, key='df')

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

# Merge new data into the existing dataframe
def merge_new(dataset, new_column):
    return dataset.join(new_column)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dfname', help='Path to a dataframe CSV or HDF file')
    parser.add_argument('seriesname', help='Path to a series CSV file')
    args = parser.parse_args()

    df = load_data(args.dfname)
    df = drop_duplicates(df)
    df = df.dropna(subset=['q2', 'q4'])
    q3 = load_series(args.seriesname)
    df = pd.concat([df, q3], axis=1)

    # Validate that the data structures were merged properly
    if(df.q3.count() == q3.count()):
        save_dataframe(df, "complete.csv")
        print("Done!")
    else:
        print("The q3 values weren't copied correctly.")

if __name__ == '__main__':
    main()
