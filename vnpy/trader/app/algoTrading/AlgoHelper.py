# encoding: UTF-8

# import csv
import os
import time
# python2下支持unicode csv
import unicodecsv as csv


def getOrder(order):
    d = {}
    d['orderID'] = order.orderID
    d['orderTime'] = order.orderTime
    d['symbol'] = order.symbol
    d['direction'] = str(order.direction)
    d['offset'] = str(order.offset)
    d['price'] = order.price
    d['status'] = order.status
    d['totalVolume'] = order.totalVolume
    d['tradedVolume'] = order.tradedVolume
    d['cancelTime'] = order.cancelTime
    d['exchange'] = order.exchange
    d['frontID'] = order.frontID
    d['gatewayName'] = order.gatewayName
    d['sessionID'] = order.sessionID
    return d

def getTrade(trader):
    d = {}
    d['orderID'] = trader.orderID
    d['tradeID'] = trader.tradeID
    d['tradeTime'] = trader.tradeTime
    d['symbol'] = trader.symbol
    d['direction'] = trader.direction
    d['offset'] = trader.offset
    d['price'] = trader.price
    d['volume'] = trader.volume
    d['exchange'] = trader.exchange
    d['gatewayName'] = trader.gatewayName
    return d
    pass

# csvtype是trade 交易, order 委托, tick 行情
# writetype: w+, a, a+ 添加
def writeCSV(csvtype, listInfo, writertype):
    today = time.strftime("%Y%m%d", time.localtime())
    path = os.path.abspath(os.path.dirname(__file__))

    listInfo = [{'orderID': '46', 'status': u'\u5168\u90e8\u6210\u4ea4', 'orderTime': '14:49:55', 'cancelTime': '', 'gatewayName': 'CTP', 'exchange': 'DCE', 'price': 2570.0, 'tradedVolume': 1, 'direction': '\xe5\xa4\x9a', 'sessionID': -1621174879, 'offset': '\xe5\xbc\x80\xe4\xbb\x93', 'frontID': 1, 'symbol': 'm1909', 'totalVolume': 1},
                {'orderID': '48', 'status': u'\u5168\u90e8\u6210\u4ea4', 'orderTime': '14:51:07', 'cancelTime': '', 'gatewayName': 'CTP', 'exchange': 'DCE', 'price': 2568.0, 'tradedVolume': 1, 'direction': '\xe5\xa4\x9a', 'sessionID': -1621174879, 'offset': '\xe5\xbc\x80\xe4\xbb\x93', 'frontID': 1, 'symbol': 'm1909', 'totalVolume': 1}]



    if len(listInfo) == 0:
        return
    # w+, w, a , a+ ->追加
    with open(csvtype + today +'.csv',writertype) as f:
        headers = [k for k in listInfo[0]]
        print(headers)
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for dictionary in listInfo:
            print(dictionary)
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
    writeCSV('order', None, 'a+')
    pass
