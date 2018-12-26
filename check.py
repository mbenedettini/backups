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
query = """SELECT nspname || '.' || relname AS "relation",
    pg_total_relation_size(C.oid) AS "total_size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
    AND C.relkind <> 'i'
    AND nspname !~ '^pg_toast'
  ORDER BY pg_total_relation_size(C.oid) DESC, nspname ASC
  LIMIT 10
"""
cur.execute(query)
actual_sizes = cur.fetchall()

all_good = True

if len(actual_sizes) == 0:
    all_good = False

for s in actual_sizes:
    name = s[0]
    if name in reference_sizes:
        reference_size = reference_sizes[name]
        if not s[1] >= reference_size:
            all_good = False
            msg = f"WRONG SIZE FOR {name}"
            print(msg)
    else:
        all_good = False
        print(f"NOT FOUND {name}")

if (all_good):
    sys.exit(0)
else:
    sys.exit(1)
