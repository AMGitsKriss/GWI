from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np

# Iterate over the provided dataframe and write line-by-line.
def write_dataframe(dataset):
	# New ES connection with default values, but a longer timeout (attempt to make up for the lack of system resources)
	es = Elasticsearch(timeout=60) 
	for index, row in dataset.iterrows():
		request = make_request(index, row)
		res = es.index(index="gwi", doc_type='respondant', body=request)
		if(res['created']):print(True)

# Build the request dict/json. 
# datum = column name, entry[datum] = value
def make_request(index, entry):
	output = {"respondant_index" : index}
	for datum in entry.keys():
		output[datum] = str(entry[datum])
	return output

# Loading the file. If not csv, assumes hdf
def load_data(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, index_col=0)
    else:
        return pd.read_hdf(filename, key='df')

def main():
	# Borrowing this from the code you sent me
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Path to a CSV or HDF file')
    args = parser.parse_args()
    df = load_data(args.filename)

    #Begin pushing rows to Elasticsearch
    write_dataframe(df)

if __name__ == '__main__':
    main()
