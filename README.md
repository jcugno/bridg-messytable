Dockerized messytable tool for quickly creating Hive/PrestoDB tables.

## Overview

Adds table to Hive from local file, guessing its schema and loading the data.

Intended for small amounts of data, typically sample data, standing data etc.
The entire local file is uploaded to the database server and inserted directly
to the table.


## Supported Data Formats

The data format is automatically detected and a best attempt is made to derive
the table data.

Works with Excel sheets, CSV and TSV. May work with JSON, XML and tables in PDF.

Expects column headers as the first row.


## Usage

```sh
docker run --rm -it \
  -v $PWD:/data \
  bridg/messytable \
    --database kim \
    --table sales \
    gross_sales.xlsx
```


## Building

```sh
docker build -t bridg/messytable .
```
