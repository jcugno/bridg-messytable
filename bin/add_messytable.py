#! /usr/bin/env python3

import datetime
import sys
import tempfile
import subprocess
import argparse

import messytables


def canonicalize_column_name(name):
    return name.lower().replace(' ', '_')

def hive_column_type(col_type):
    return {
            messytables.types.StringType:   'STRING',
            messytables.types.DateType:     'TIMESTAMP',
    }[type(col_type)]


def proc(f, database_name, table_name):

    table_set = messytables.any_tableset(f)
    row_set = table_set.tables[0]

    # guess header names and the offset of the header:
    offset, headers = messytables.headers_guess(row_set.sample)
    row_set.register_processor(messytables.headers_processor(headers))
    row_set.register_processor(messytables.offset_processor(offset + 1))
    types = messytables.type_guess(row_set.sample, types=[
        messytables.types.StringType,
        messytables.types.DateType,
    ], strict=True)
    hive_data_file = tempfile.NamedTemporaryFile(mode='w')

    fields_ddl = ','.join([
        '  {0} {1}\n'.format(
            canonicalize_column_name(colName),
            hive_column_type(colType)
        )
        for colName, colType in zip(headers, types)
    ])
    hive_sql = '''
DROP TABLE IF EXISTS {0};

CREATE TABLE {0} (
{1}
)
STORED AS TEXTFILE
TBLPROPERTIES ("comment"="add_messytable on {3}");

LOAD DATA LOCAL INPATH '{2}' OVERWRITE INTO TABLE {0};
'''.format(table_name, fields_ddl, hive_data_file.name,
        datetime.datetime.now().isoformat())

    hive_cmd_file = tempfile.NamedTemporaryFile(mode='w')
    print(hive_sql, file=hive_cmd_file)
    hive_cmd_file.flush()

    row_set.register_processor(messytables.types_processor(types))

    for row in row_set:
        print('\001'.join(map(str, [ c.value for c in row])),
                file=hive_data_file)
    hive_data_file.flush()

    subprocess.call([
        'hive',
        '--database', database_name,
        '-f', hive_cmd_file.name,
    ])


def main():
    parser = argparse.ArgumentParser()
    aa = parser.add_argument

    aa('--database', '-d', required=True)
    aa('--table', '-t', required=True)
    aa('infiles', nargs='*', type=argparse.FileType('rb'))
    args = parser.parse_args()

    for f in args.infiles:
        proc(f, args.database, args.table)

if __name__ == '__main__':
    main()
