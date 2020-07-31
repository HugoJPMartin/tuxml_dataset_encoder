import os
import json
import sys

import pandas as pd
import numpy as np


# Static information
tri_state_values = ['y', 'n', 'm']
size_methods = ["vmlinux", "GZIP-bzImage", "GZIP-vmlinux", "GZIP", "BZIP2-bzImage", 
              "BZIP2-vmlinux", "BZIP2", "LZMA-bzImage", "LZMA-vmlinux", "LZMA", "XZ-bzImage", "XZ-vmlinux", "XZ", 
              "LZO-bzImage", "LZO-vmlinux", "LZO", "LZ4-bzImage", "LZ4-vmlinux", "LZ4"]


# In order to keep having the same encoding for the same value, easier to interpret
# Note that in this version, module (m) and no (n) are encoded the same due to not counting into kernel size
def same_encode(x):
    return str(x).replace("y","1").replace("n","0").replace("m","0")

# Custom feature, about the number of activated options, noted as "y" and encoded at 1
def counting_activate_options(x):
    return x.value_counts()[1]

def encode_dataframe(df, non_tristate_columns):
    # Encoding the tristate options
    df_encoded = df.drop(columns= non_tristate_columns + size_methods).applymap(same_encode).astype(np.int8)
    
    # Custom features
    df_encoded["active_options"] = df_encoded.apply(counting_activate_options, axis=1)
    
    # Adding the size columns and the cid columns
    df_encoded[size_methods] = df[size_methods]
    df_encoded["cid"]=df["cid"]
    
    return df_encoded



# Directory with all the csv files
dirname = "csv"

# Output directory
output_dirname = "output"
try:
    os.mkdir(output_dirname)
except:
    pass

# Init for checking csv files integrity
csv_columns = -1

# Init the finale dataframe
df_merge = pd.DataFrame()

# Listing all csv files
for filename in os.listdir(dirname):
    
    # Must be a csv file
    if not filename.endswith(".csv"):
        continue
    
    print("importing "+ dirname + "/" + filename)
    # Importing the csv file as a dataframe
    df = pd.read_csv(dirname + "/" + filename)
        
    print("filtering "+ dirname + "/" + filename)
    # Filtering out compilation failures
    df = df[df["vmlinux"] > 0]
    
    
    
    print("encoding "+ dirname + "/" + filename)
    if len(df_merge.columns) > 0:
        
        # Checking csv files integrity
        if not csv_columns == len(df.columns):
            sys.exit('The columns number does not match in the csv files')
    
    # If it is the first csv file
    else:
        # Getting the number of columns
        csv_columns = len(df.columns)
        
        # Listing non tristate options
        non_tristate_columns = [col for col in df.columns if not all(x in tri_state_values for x in df[col].unique())]
    
    # Adding the encoded dataframe to the finale dataframe
    df_merge = df_merge.append(encode_dataframe(df, non_tristate_columns))
    
# Finding columns with only one value for all examples
unique_columns = [col for col in df_merge.columns if len(df_merge[col].unique()) == 1]

# Dropping the unique columns
df_merge = df_merge.drop(columns=unique_columns).sort_values("cid").reset_index(drop=True)

# Exporting the encoded dataset to pickle
df_merge.to_pickle(output_dirname+"/dataset.pkl")

# Exporting the deleted columns names
with open(output_dirname+"/non_tristate_columns.json", "w") as f:
    json.dump(non_tristate_columns, f)
    
with open(output_dirname+"/unique_columns.json", "w") as f:
    json.dump(unique_columns, f)