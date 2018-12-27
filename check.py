import sys

reference_sizes_filename = sys.argv[1]
f = open(reference_sizes_filename, "r+")
lines = f.readlines()

reference_sizes = {}

for l in lines:
    fields = [f.strip() for f in l.split('|')]
    size = 0
    try:
        size = int(fields[1])
    except:
        pass

    is_data = len(fields) == 2 and size > 0
    if is_data:
        reference_sizes[fields[0]] = size

print(reference_sizes)

import psycopg2
conn = psycopg2.connect("dbname=restore user=restore host=127.0.0.1 port=5433")
cur = conn.cursor()

# Add count rows function
cur.execute("""create or replace function 
count_rows(schema text, tablename text) returns integer
as
$body$
declare
  result integer;
  query varchar;
begin
  query := 'SELECT count(1) FROM ' || schema || '.' || tablename;
  execute query into result;
  return result;
end;
$body$
language plpgsql;""")

# query count
query = """select 
  table_schema,
  table_name, 
  count_rows(table_schema, table_name)
from information_schema.tables
where 
  table_schema not in ('pg_catalog', 'information_schema') 
  and table_type='BASE TABLE'
order by 3 desc limit 10"""
cur.execute(query)
actual_sizes = cur.fetchall()

all_good = True

if len(actual_sizes) == 0:
    all_good = False

for s in actual_sizes:
    name = s[1]
    actual_size = s[2]
    if name in reference_sizes:
        reference_size = reference_sizes[name]
        if not actual_size >= reference_size:
            all_good = False
            msg = f"WRONG SIZE FOR {name} (expected: {reference_size}, actual: {actual_size})"
            print(msg)
    else:
        all_good = False
        print(f"NOT FOUND {name}")

if (all_good):
    sys.exit(0)
else:
    sys.exit(1)
