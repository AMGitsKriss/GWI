import pandas as pd
import numpy as np

QUOTAS = (
    ([0, 0], 1000),
    ([0, 1], 2000),
    ([0, 2], 3000),
    ([1, 0], 5000),
    ([1, 1], 8000),
    ([1, 2], 3000),
)


# Iterating over the target values, campare them to the actual values.
# Calculate how much they need scaling by, then return the results.
def get_factor_weights(quotas, counts):
    factors = []
    for (q2, q4), quota_size in quotas:
        count = counts.loc[(q2, q4)]
        factor = quota_size/count
        factors.append(((q2, q4), factor))
    return factors

# Set the value of each q2-q4 pair to it's respective factor. 
def distribute_factors(df, factors):
    for (q2, q4), factor in factors:
        df.loc[(df['q2'] == q2) & (df['q4'] == q4), 'weighting'] = factor
    return df

# Loading the file. If not csv, assumes hdf
def load_data(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, index_col=0)
    else:
        return pd.read_hdf(filename, key='df')

# Get the counts for every q2-q4 pair.
def groupby_factors(df):
    return df.groupby(['q2', 'q4']).q2.count()

# Gets real pop values, target values, then scale.
def assign_weights(df):
    counts = groupby_factors(df)
    factors = get_factor_weights(QUOTAS, counts)
    dfp = distribute_factors(df, factors)
    return dfp

# Add up the new values and print them alongside the target values. 
def validate_weights(df):
    sums = df.groupby(['q2', 'q4']).weighting.sum()
    for (q2, q4), quota_size in QUOTAS:
        print('(q2, q4): ({}, {})\t'.format(q2, q4),
              sums.loc[(q2, q4)], '\t', quota_size
             )

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Path to a CSV or HDF file')
    args = parser.parse_args()
    df = load_data(args.filename)
    dfp = assign_weights(df)
    validate_weights(dfp)

if __name__ == '__main__':
    main()
