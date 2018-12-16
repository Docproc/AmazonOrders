# -*- coding: utf-8 -*-

import sys

import pandas as pd

'''
Analyse Amazon orders

See README.md
'''


def convert_currency(val):
    """
    Convert the string number value to a float
     - Remove first char (to avoid pound sign coding weirdness)
     - Convert to float type
    """
    cost = val[2:]
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

(name, year) = name_and_year_from_filename(filename)

df = pd.read_csv(filename)

total_count = len(df)

total_cost = df['total'].apply(convert_currency).sum()

kindle_df = df.loc[df['order id'].str.startswith('D01')]

kindle_count = len(kindle_df)

kindle_cost = kindle_df['total'].apply(convert_currency).sum()

other_df = df.loc[df['order id'].str.slice(0, 3) != 'D01']

other_count = len(other_df)

other_cost = other_df['total'].apply(convert_currency).sum()

print "%s %d\tTotal: %d\t%s%1.2f\tKindle: %d\t%s%1.2f\tOther: %d\t%s%1.2f" % (
    name, int(year), total_count, POUND, total_cost, kindle_count, POUND, kindle_cost, other_count, POUND, other_cost)
