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
    cost = val[1:]
    try:
        return float(cost)
    except ValueError:
        return 0.0


# Extract the name and year from the filename
# Assumed format name_year_XXX.csv
def name_and_year_from_filename(file_name):
    bits = file_name.split('_')
    if not str(bits[1]).isdigit():
        print("Error: filename should be in the format name_year_XXX.csv", bits[1])
        sys.exit(1)
    return bits[0], bits[1]


if len(sys.argv) != 2:
    print("Usage: {0} <filename>".format(sys.argv[0]))
    sys.exit(1)

filename = sys.argv[1]

POUND = chr(163)

(name, year) = name_and_year_from_filename(filename)

df = pd.read_csv(filename)

# Remove orders which were refunds (refund column not empty)
#df = df.loc[pd.isnull(df['refund'])]

total_count = len(df)

total_cost = df['total'].apply(convert_currency).sum()

kindle_df = df.loc[df['order id'].str.startswith('D01')]

kindle_count = len(kindle_df)

kindle_cost = kindle_df['total'].apply(convert_currency).sum()

other_df = df.loc[df['order id'].str.slice(0, 3) != 'D01']

other_count = len(other_df)

other_cost = other_df['total'].apply(convert_currency).sum()

print("{name} {year:5d}\tTotal: {total_count:d}\t{pound}{total_cost:.2f}\tKindle: {kindle_count:d}\t{pound}{kindle_cost:.2f}\tOther: {other_count}\t{pound}{other_cost:.2f}".format(
    name=name, year=int(year), total_count=total_count, pound=POUND, total_cost=total_cost, kindle_count=kindle_count, kindle_cost=kindle_cost, other_count=other_count, other_cost=other_cost))
