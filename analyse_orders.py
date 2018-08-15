import csv
import re
import sys

'''
Analyse Amazon orders

Use "Amazon Order History Reporter" Chrome extension, https://chrome.google.com/webstore/detail/amazon-order-history-repo/mgkilgclilajckgnedgjgnfdokkgnibi?hl=en

Download "All years" as CSV (or individual years)


'''
# TODO download all history files
# TODO parse file names for person and year
# TODO command-line option for plain text output


if len(sys.argv) != 2:
    print "Usage: %s <filename>" % (sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'rb') as f:
    reader = csv.reader(f)
    headers = []
    kindle_orders = []
    other_orders = []
    year = 0
    line_count = 0
    for row in reader:
        if line_count == 0:
            headers = row
        else:
            if row[0].startswith("D01"):
                kindle_orders.append(row)
            else:
                other_orders.append(row)
            row_date = row[3]
            match = re.search(r"(\d+)/(\d+)/(\d+)", row_date)
            if (match):
                row_year = match.group(3)
                if year == 0:
                    year = row_year
                elif row_year != year:
                    print "\033[93mYear mismatch: previous row had %d, this row has %d\n%s\n \x1b[0m" % (int(year), int(row_year), str.join(",", row))

        line_count += 1

    print "%d\tTotal orders: %d\tKindle orders: %d\tOther orders: %d" % (int(year), line_count-1, len(kindle_orders), len(other_orders))

