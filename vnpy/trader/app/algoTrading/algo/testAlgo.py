# encoding: UTF-8

import csv
import os
import time


def writeOrder():
    today = time.strftime("%Y%m%d", time.localtime())
    path = os.path.abspath(os.path.dirname(__file__))
    testdata = [{'date': '2019-4-28', 'time': '11:22:00', 'symbol': 'm1909', 'direction': '买', 'offset': '开仓', 'priceType': '市价', 'price': '2289.0', 'volume': '1'},
                {'date': '2019-4-28', 'time': '13:42:00', 'symbol': 'm1909', 'direction': '买', 'offset': '开仓', 'priceType': '市价', 'price': '2299.0', 'volume': '1'},
                {'date': '2019-4-28', 'time': '13:45:00', 'symbol': 'm1909', 'direction': '买', 'offset': '开仓', 'priceType': '市价', 'price': '2279.0', 'volume': '1'},
                {'date': '2019-4-27', 'time': '14:02:00', 'symbol': 'm1909', 'direction': '买', 'offset': '开仓', 'priceType': '市价', 'price': '2269.0', 'volume': '1'},
                {'date': '2019-4-27', 'time': '14:32:00', 'symbol': 'm1909', 'direction': '买', 'offset': '开仓', 'priceType': '市价', 'price': '2259.0', 'volume': '1'}]
    # w+, w, a ->追加
    with open('trader'+ today +'.csv','w+', encoding='utf-8') as f:
        headers = [k for k in testdata[0]]
        print(headers)
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for dictionary in testdata:
            writer.writerow(dictionary)
        pass

def readOrder():
    path = os.path.abspath(os.path.dirname(__file__))
    result =[]
    with open("trader.csv", 'r',encoding='utf-8') as f:
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
    print(result)

if __name__ == '__main__':
    #readOrder()
    writeOrder()
    pass
