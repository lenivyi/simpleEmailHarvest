#!/usr/bin/env python
#
# simpleEmailHarvest.py
#

import urllib2
import re
import sqlite3 as lite
from sys import argv
from time import sleep
from google import search

keywords = argv[1]
database = argv[2]

con = lite.connect(database)
cur = con.cursor()
cur.execute("CREATE TABLE email_tbl(id INTEGER PRIMARY KEY, email TEXT)")

def write_to_db(result):
    insert = "INSERT INTO email_tbl(email) VALUES(\""+result+"\")"
    cur.execute(insert)
    con.commit()

def get_email(link):
    pattern = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b")
    get_link = urllib2.urlopen(link)
    content = get_link.read()
    raw_email = pattern.findall(content)
    for email in raw_email:
        print "an email has been added"
        write_to_db(email)
        
def get_url(key):
    for url in search(key, stop=0):
        get_email(url)
        
if __name__ == "__main__":
    try:
        get_url(keywords)
    except KeyboardInterrupt:
        print "\nProgram Exit !!"
    finally:
        con.close()
