#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import re
import sys

from collections import Counter
from operator import add
from functools import reduce

date_converter = mdates.strpdate2num('%d.%m.%Y')

def fill_blanks(d):
    prev_k = None
    for k, v in sorted(d.items(), key=lambda a: a[0]):
        if prev_k is not None:
            for k2 in range(prev_k, k):
                d[k2] = d[prev_k]
        prev_k = k
    return d

def load_balance(path):
    balance = {}
    with open(path) as f:
        reader = csv.reader(f, delimiter=';')
        for l in reader:
            date = int(date_converter(l[0]))

            b = re.sub(r'\.', '', l[5])
            b = re.sub(r',', '.', b)
            b = float(b)

            balance[date] = b

    return fill_blanks(balance)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: {} account1.csv, account2.csv, ...".format(sys.argv[0]))
        sys.exit(1)

    accounts = (load_balance(a) for a in sys.argv[1:])
    balance  = reduce(add, (Counter(dict(x)) for x in accounts))
    items    = sorted(balance.items(), key=lambda a: a[0])

    fig = plt.figure()
    plt.plot_date(*zip(*items), fmt='r-')
    plt.ylabel('DKK')
    plt.grid(True)
    plt.show()

    fig.savefig('plot.png')
    fig.savefig('plot.pdf')
