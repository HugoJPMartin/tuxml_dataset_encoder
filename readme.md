# TuxML Dataset Encoder

This docker image image purpose is to have a standard way to encode and merge csv datasets from [TuxML](https://github.com/TuxML).

The script inside will delete non-ternary options from the dataset, encode the "y" as 1 and "n" and "m" as 0, then encode them as numpy.int8 data format to save a lot of memory.

All columns with only one value are deleted.

At least, the dataset is exported as a pandas DataFrame in a pickle file.

Are also exported the name of the columns that have been deleted from the dataset, either due to being non-ternary options, or for having only one value.

___

The image needs 2 volumes to work : 
 * "csv" containing the csv files containing the data to encode
 * "output" which will receive the encoded dataset as well and json files containing lists of the deleted columns

```
docker run -v $(pwd)/csv:/app/csv -v $(pwd)/output:/app/output:Z hmartinirisa/tuxml_dataset_encoder
```