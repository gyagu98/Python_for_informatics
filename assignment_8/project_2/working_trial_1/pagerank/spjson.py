import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

print("Creating JSON output on spider.js...")

# Ask user how many nodes they want
howmany = int(input("How many nodes? "))

# Fetch Pages with existing PageRank values
cur.execute('''
    SELECT COUNT(from_id) AS inbound, COALESCE(old_rank, 0), COALESCE(new_rank, 0), id, url 
    FROM Pages LEFT JOIN Links ON Pages.id = Links.to_id
    WHERE html IS NOT NULL AND error IS NULL
    GROUP BY id ORDER BY new_rank DESC LIMIT ?''', (howmany,))

fhand = open('spider.js', 'w')
nodes = list()
maxrank = None
minrank = None

# Fix: Ensure we correctly get min/max rank and handle missing values
for row in cur:
    nodes.append(row)
    rank = row[2] if row[2] is not None else 0  # Avoid None values

    if maxrank is None or rank > maxrank:
        maxrank = rank
    if minrank is None or rank < minrank:
        minrank = rank

# Fix: Ensure we don't divide by zero
if maxrank == minrank or maxrank is None or minrank is None:
    print("❌ Error: PageRank values are missing or uninitialized. Run sprank.py again!")
    quit()

fhand.write('spiderJson = {"nodes":[\n')
count = 0
map = {}
ranks = {}

for row in nodes:
    if count > 0:
        fhand.write(',\n')

    rank = row[2] if row[2] is not None else minrank  # Avoid None
    normalized_rank = 19 * ((rank - minrank) / (maxrank - minrank))

    fhand.write(f'{{"weight":{row[0]},"rank":{normalized_rank},')
    fhand.write(f' "id":{row[3]}, "url":"{row[4]}"}}')

    map[row[3]] = count
    ranks[row[3]] = normalized_rank
    count += 1

fhand.write('],\n')

# Fetch links and create JSON structure
cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
fhand.write('"links":[\n')

count = 0
for row in cur:
    if row[0] not in map or row[1] not in map:
        continue
    if count > 0:
        fhand.write(',\n')

    fhand.write(f'{{"source":{map[row[0]]},"target":{map[row[1]]},"value":3}}')
    count += 1

fhand.write(']};')
fhand.close()
cur.close()

print("✅ JSON output saved to spider.js! Open `spider.html` in a browser to view the visualization.")
