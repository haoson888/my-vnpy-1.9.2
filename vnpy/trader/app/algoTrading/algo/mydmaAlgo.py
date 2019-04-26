# encoding: UTF-8

from __future__ import division
from collections import OrderedDict

from vnpy.trader.vtConstant import (DIRECTION_LONG, DIRECTION_SHORT,
                                    OFFSET_OPEN, OFFSET_CLOSE,
                                    PRICETYPE_LIMITPRICE, PRICETYPE_MARKETPRICE,
                                    STATUS_REJECTED, STATUS_CANCELLED, STATUS_ALLTRADED)
from vnpy.trader.uiQt import QtWidgets
from vnpy.trader.app.algoTrading.algoTemplate import AlgoTemplate
from vnpy.trader.app.algoTrading.uiAlgoWidget import AlgoWidget, QtWidgets

from six import text_type

from vnpy.trader.app.algoTrading.AlgoUiHelper import generateWidgetClass

STATUS_FINISHED = set([STATUS_ALLTRADED, STATUS_CANCELLED, STATUS_REJECTED])


########################################################################

class MyDmaAlgo(AlgoTemplate):
    """梯形算法"""

    templateName = u'My 阶梯算法'

    #----------------------------------------------------------------------
    def __init__(self, engine, setting, algoName):
        """Constructor"""
        super(MyDmaAlgo, self).__init__(engine, setting, algoName)

        # 参数，强制类型转换，保证从CSV加载的配置正确
        self.vtSymbol = str(setting['vtSymbol'])            # 合约代码
        self.direction = text_type(setting['direction'])    # 买卖
        self.offset = text_type(setting['offset'])          # 开平
        self.priceType = text_type(setting['priceType'])    # 价格类型
        self.price = float(setting['price'])                # 开始价格
        self.volume =  float(setting['volume'])            #每次手数
        self.totalVolume = float(setting['totalVolume'])    # 限制总数量
        self.spread = float(setting['spread'])  # 平仓价差
        self.interval = int(setting['interval']) # 梯形间隔

        self.vtOrderID = ''     # 委托号
        self.tradedVolume = 0   # 成交数量
        self.orderStatus = ''   # 委托状态
        self.lastTick = None     # 最新Tick

        self.subscribe(self.vtSymbol)

        # 下起始单
        self.openOrder(self.price)

        self.paramEvent()
        self.varEvent()

    #----------------------------------------------------------------------
    def onTick(self, tick):
        """"""
        # 行情
        # 发出委托
        # self.lastTick = tick

        # 多头
        '''
        if self.direction == DIRECTION_LONG:
            # 如果没有委托，则发单
            if (not self.vtOrderID):
                if (self.lastTick.bidPrice1 <= self.price):
                    self.buyOrder()
            # 如果最新行情买价高于委托价格，则撤单

            elif self.price > self.lastTick.bidPrice1:
                self.cancelAll()
        # 空头
        if self.direction == DIRECTION_SHORT:
            if not self.vtOrderID:
                #self.sellBestLimit()
                pass
            elif self.orderPrice != self.lastTick.askPrice1:
                #self.cancelAll()
                pass


        # 更新变量

        self.varEvent()
        '''

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """"""
        # 成交
        # 开仓成交后，立即加上平仓价差平仓
        if self.vtOrderID == '':
            self.closeOrder(self.price + self.spread)
            # 然后按梯形间隔下开仓委托
            self.price = self.price - self.interval
            self.openOrder(self.price)

        # self.tradedVolume += trade
        self.varEvent()

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """"""
        # 委托

        self.tradedVolume = order.tradedVolume
        self.orderStatus = order.status

        if self.orderStatus in STATUS_FINISHED:
            # self.stop()
            self.vtOrderID = ''

        self.varEvent()

    #----------------------------------------------------------------------
    def onTimer(self):
        """"""
        '''
        self.count += 1
        if self.count < self.interval:
            return

        self.count = 0

        # 取最新报价
        activeTick = self.getTick(self.vtSymbol)

        spreadbidPrice = self.price -  activeTick.bidPrice1

        if spreadbidPrice <= 0.01:
            self.activeOrderID = self.buy(self.vtSymbol, activeTick.bidPrice1,1.0)


        self.varEvent()
        '''

    #----------------------------------------------------------------------
    def onStop(self):
        """"""
        self.writeLog(u'停止算法')
        self.varEvent()

    #----------------------------------------------------------------------
    def varEvent(self):
        """更新变量"""
        d = OrderedDict()
        d[u'算法状态'] = self.active
        d[u'委托号'] = self.vtOrderID
        d[u'成交数量'] = self.tradedVolume
        d[u'委托状态'] = self.orderStatus
        d['active'] = self.active
        self.putVarEvent(d)

    #----------------------------------------------------------------------
    def paramEvent(self):
        """更新参数"""
        d = OrderedDict()
        d[u'代码'] = self.vtSymbol
        d[u'方向'] = self.direction
        d[u'价格'] = self.price
        d[u'总量'] = self.totalVolume
        d[u'价格类型'] = self.priceType
        d[u'开平'] = self.offset
        d[u'数量'] = self.volume
        d[u'价差'] = self.spread
        d[u'间隔'] = self.interval
        self.putParamEvent(d)

    def openOrder(self, openprice):
        self.vtOrderID = self.buy(self.vtSymbol, openprice, self.volume,
                                  self.priceType,self.offset)


    def closeOrder(self,closeprice):
        self.vtOrderID = self.sell(self.vtSymbol, closeprice,self.volume,
                                   self.priceType, OFFSET_CLOSE)


# 生成我们的UI类
class MyDmaWidget(AlgoWidget):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, algoEngine, parent=None):
        """Constructor"""
        super(MyDmaWidget, self).__init__(algoEngine, parent)

        self.templateName = MyDmaAlgo.templateName

    #----------------------------------------------------------------------
    def initAlgoLayout(self):
        """"""
        self.lineSymbol = QtWidgets.QLineEdit()

        self.comboDirection = QtWidgets.QComboBox()
        self.comboDirection.addItem(DIRECTION_LONG)
        self.comboDirection.addItem(DIRECTION_SHORT)
        self.comboDirection.setCurrentIndex(0)

        self.spinPrice = QtWidgets.QDoubleSpinBox()
        self.spinPrice.setMinimum(0)
        self.spinPrice.setMaximum(1000000000)
        self.spinPrice.setDecimals(8)

        self.spinTotalVolume = QtWidgets.QDoubleSpinBox()
        self.spinTotalVolume.setMinimum(0)
        self.spinTotalVolume.setMaximum(1000000000)
        self.spinTotalVolume.setDecimals(6)

        self.comboPriceType = QtWidgets.QComboBox()
        self.comboPriceType.addItems([PRICETYPE_LIMITPRICE, PRICETYPE_MARKETPRICE])
        self.comboPriceType.setCurrentIndex(0)

        self.comboOffset = QtWidgets.QComboBox()
        self.comboOffset.addItems(['', OFFSET_OPEN, OFFSET_CLOSE])
        self.comboOffset.setCurrentIndex(0)

        self.spinSpread = QtWidgets.QDoubleSpinBox()
        self.spinSpread.setMinimum(0)
        self.spinSpread.setMaximum(1000000000)
        self.spinSpread.setDecimals(8)

        self.spinInterval = QtWidgets.QDoubleSpinBox()
        self.spinInterval.setMinimum(0)
        self.spinInterval.setMaximum(1000000000)
        self.spinInterval.setDecimals(6)

        self.spinVolume = QtWidgets.QDoubleSpinBox()
        self.spinVolume.setMinimum(0)
        self.spinVolume.setMaximum(1000000000)
        self.spinVolume.setDecimals(6)

        buttonStart = QtWidgets.QPushButton(u'启动')
        buttonStart.clicked.connect(self.addAlgo)
        buttonStart.setMinimumHeight(100)

        Label = QtWidgets.QLabel

        grid = QtWidgets.QGridLayout()
        grid.addWidget(Label(u'代码'), 0, 0)
        grid.addWidget(self.lineSymbol, 0, 1)
        grid.addWidget(Label(u'方向'), 1, 0)
        grid.addWidget(self.comboDirection, 1, 1)
        grid.addWidget(Label(u'价格'), 2, 0)
        grid.addWidget(self.spinPrice, 2, 1)
        grid.addWidget(Label(u'数量'), 3, 0)
        grid.addWidget(self.spinVolume, 3, 1)
        grid.addWidget(Label(u'类型'), 4, 0)
        grid.addWidget(self.comboPriceType, 4, 1)
        grid.addWidget(Label(u'开平'), 5, 0)
        grid.addWidget(self.comboOffset, 5, 1)
        grid.addWidget(Label(u'价差'),6,0)
        grid.addWidget(self.spinSpread,6,1)
        grid.addWidget(Label(u'间隔'),7,0)
        grid.addWidget(self.spinInterval,7,1)
        grid.addWidget(Label(u'总手数'),8,0)
        grid.addWidget(self.spinTotalVolume,8,1)

        return grid

    #----------------------------------------------------------------------
    def getAlgoSetting(self):
        """"""
        setting = OrderedDict()
        setting['templateName'] = MyDmaAlgo.templateName
        setting['vtSymbol'] = str(self.lineSymbol.text())
        setting['direction'] = text_type(self.comboDirection.currentText())
        setting['price'] = float(self.spinPrice.value())
        setting['volume'] = float(self.spinVolume.value())
        setting['totalVolume'] = float(self.spinTotalVolume.value())
        setting['priceType'] = text_type(self.comboPriceType.currentText())
        setting['offset'] = text_type(self.comboOffset.currentText())
        setting['spread'] = float(self.spinSpread.value())
        setting['interval'] = float(self.spinInterval.value())

        return setting




########################################################################



