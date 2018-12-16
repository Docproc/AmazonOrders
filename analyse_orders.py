# -*- coding: utf-8 -*-

import csv
import sys

'''
Analyse Amazon orders

See README.md
'''

# Convert pound 1.23 string to float
# Just chop off the first character to get around pound sign encoding weirdness
def cost_to_float(str_cost):
    cost = str_cost[2:]
    try:
        return float(cost)
    except ValueError:
        return 0.0


# Extract the name and year from the filename
# Assumed format name_year_XXX.csv
def name_and_year_from_filename(file_name):
    bits = file_name.split('_')
    if not str(bits[1]).isdigit():
        print "Error: filename should be in the format name_year_XXX.csv", bits[1]
        sys.exit(1)
    return bits[0], bits[1]



if len(sys.argv) != 2:
    print "Usage: %s <filename>" % (sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

POUND = unichr(163)

with open(filename, 'rb') as f:
    reader = csv.DictReader(f)
    kindle_orders = []
    other_orders = []
    kindle_cost = 0.00
    other_cost = 0.00
    (name, year) = name_and_year_from_filename(filename)
    for line_count, row in enumerate(reader):
        if row['order id'].startswith("D01"):
            kindle_orders.append(row)
            kindle_cost += cost_to_float(row['total'])
        else:
            other_orders.append(row)
            other_cost += cost_to_float(row['total'])

    total_cost = kindle_cost + other_cost

    print "%s %d\tTotal: %d\t%s%1.2f\tKindle: %d\t%s%1.2f\tOther: %d\t%s%1.2f" % (
        name, int(year), line_count, POUND, total_cost, len(kindle_orders), POUND, kindle_cost, len(other_orders),
        POUND, other_cost)
