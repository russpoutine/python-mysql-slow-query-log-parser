#!/usr/bin/env python
"""
Parses MySQL slow log files. Output is in CSV.

# Time: 180705 12:34:56
# User@Host: root[root] @ localhost []
# Query_time: 13.123456  Lock_time: 0.01234 Rows_sent: 0  Rows_examined: 123456
SET timestamp=1530661285;
select * from mytable;
"""


import fileinput
import re
import csv
import sys

pat = """^# Time: (?P<time>\d{2}\d{2}\d{2} \d{2}:\d{2}:\d{2}\s?)
# User@Host: (?P<User_Host>.*?)\s?
# Query_time: (?P<Query_time>\d+\.\d+)\s+Lock_time: (?P<Lock_time>\d+\.\d+)\s+Rows_sent: (?P<Rows_sent>\d+)\s+Rows_examined: (?P<Rows_examined>\d+)\s?
(?P<Query>[^#]+)#?$"""

fields = ['Time', 'User_Host', 'Query_time', 'Lock_time', 'Rows_sent',
        'Rows_examined', 'Query']

lines = ''
for line in fileinput.input():
    lines = lines + line

writer = csv.writer(sys.stdout)
headers_printed = False
for match in re.finditer(pat, lines, re.MULTILINE | re.DOTALL):
    if not headers_printed:
        writer.writerow(fields)
        headers_printed = True
    writer.writerow(match.groups())
