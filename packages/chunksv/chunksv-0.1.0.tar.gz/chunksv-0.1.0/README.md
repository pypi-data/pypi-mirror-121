# chunksv

Python wrapper for `csv.reader` that can process files in predefined chunks. 


## purpose

This library allows a user to partition a filestream into partitions of a predefined size. It was initially
motivated by the need to process large CSV files from AWS S3 while keeping application code clean.


## package installation and usage

The package is available on PyPI:

```shell
python -m pip install chunksv
```

The library can be imported and used as follows:

```python
import chunksv

with open("file.csv", "r") as f:
    rows = chunksv.reader(
        f, 
        max_bytes=<size of each partition>, 
        header=[<optional columns list>]
    )
```

When the `reader` object has consumed enough rows to reach the `max_bytes` limit, it will raise `StopIteration`. To 
consume more rows from the input stream, call `reader.resume()`:

```python

while not rows.empty:
    current_partition = [r for r in rows]
    < process partition here >
    rows.resume()
```