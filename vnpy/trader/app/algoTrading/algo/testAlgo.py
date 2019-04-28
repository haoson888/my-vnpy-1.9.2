# encoding: UTF-8

import csv
import os


def writeOrder():
    path = os.path.abspath(os.path.dirname(__file__))
    with open('trader.csv','w+', encoding="utf-8") as f:
        pass

def readOrder():
    path = os.path.abspath(os.path.dirname(__file__))
    result =[]
    with open("trader.csv", 'r') as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
        print (fieldnames)
        csv_reader = csv.DictReader(f,fieldnames=fieldnames)
        for row in csv_reader:
            d = {}
            for k, v in row.items():
                d[k] = v
            print (d)
            result.append(d)

if __name__ == '__main__':
    readOrder()
    pass
