import sqlite3
import urllib.request, urllib.parse, urllib.error
import ssl
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Create an SSL context to ignore certificate verification
scontext = ssl.create_default_context()
scontext.check_hostname = False
scontext.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Pages 
    (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT, 
     error INTEGER, old_rank REAL, new_rank REAL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Links 
    (from_id INTEGER, to_id INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE)''')

# Check if a crawl is already in progress
cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
if row is not None:
    print("Restarting existing crawl. Remove spider.sqlite to start a fresh crawl.")
else:
    starturl = input('Enter web url or enter: ')
    if len(starturl) < 1:
        starturl = 'http://www.dr-chuck.com/'
    if starturl.endswith('/'):
        starturl = starturl[:-1]
    web = starturl
    if starturl.endswith('.htm') or starturl.endswith('.html'):
        pos = starturl.rfind('/')
        web = starturl[:pos]

    if len(web) > 1:
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES (?)', (web,))
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (?, NULL, 1.0)', (starturl,))
        conn.commit()

# Get the current webs
cur.execute('SELECT url FROM Webs')
webs = [str(row[0]) for row in cur]

print(webs)

many = 0
while True:
    if many < 1:
        sval = input('How many pages:')
        if len(sval) < 1:
            break
        many = int(sval)
    many = many - 1

    cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    if row is None:
        print("No unretrieved HTML pages found")
        break

    fromid = row[0]
    url = row[1]
    print(fromid, url, end=" ")

    # If retrieving this page, remove existing links
    cur.execute('DELETE from Links WHERE from_id=?', (fromid,))

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        document = urllib.request.urlopen(req, context=scontext)
        html = document.read()

        if document.getcode() != 200:
            print("Error on page:", document.getcode())
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url))

        if 'text/html' not in document.info().get_content_type():
            print("Ignore non text/html page")
            cur.execute('DELETE FROM Pages WHERE url=?', (url,))
            cur.execute('UPDATE Pages SET error=0 WHERE url=?', (url,))
            conn.commit()
            continue

        print("("+str(len(html))+")", end=" ")

        soup = BeautifulSoup(html, "html.parser")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user...")
        break
    except:
        print("Unable to retrieve or parse page")
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url,))
        conn.commit()
        continue

    cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url))
    conn.commit()

    # Retrieve all anchor tags
    tags = soup('a')
    count = 0
    for tag in tags:
        href = tag.get('href', None)
        if href is None:
            continue

        up = urlparse(href)
        if len(up.scheme) < 1:
            href = urljoin(url, href)
        ipos = href.find('#')
        if ipos > 1:
            href = href[:ipos]
        if href.endswith(('.png', '.jpg', '.gif', '/')):
            continue

        found = any(href.startswith(web) for web in webs)
        if not found:
            continue

        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (?, NULL, 1.0)', (href,))
        count += 1
        conn.commit()

        cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', (href,))
        row = cur.fetchone()
        if row is None:
            print("Could not retrieve id")
            continue
        toid = row[0]

        cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES (?, ?)', (fromid, toid))

    print(count)

cur.close()
