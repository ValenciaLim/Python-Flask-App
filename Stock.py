class Stock:
    stockID = 0
    def __init__(self, date, suppliername, companyname, productname, costprice, quantity, description):
        Stock.stockID += 1
        self.__stockID = Stock.stockID
        self.__date = date
        self.__suppliername = suppliername
        self.__companyname = companyname
        self.__productname = productname
        self.__costprice = costprice
        self.__quantity = quantity
        self.__description = description
        self.__status = "sufficient stock"

    def get_stockID(self):
        return self.__stockID

    def get_date(self):
        return self.__date

    def get_suppliername(self):
        return self.__suppliername

    def get_companyname(self):
        return self.__companyname

    def get_productname(self):
        return self.__productname

    def get_costprice(self):
        return self.__costprice

    def get_quantity(self):
        return self.__quantity

    def get_description(self):
        return self.__description

    def get_status(self):
        return self.__status

    def set_stockID(self, stockID):
        self.__stockID = stockID

    def set_date(self, date):
        self.__date = date

    def set_suppliername(self, suppliername):
        self.__suppliername = suppliername

    def set_companyname(self, companyname):
        self.__companyname = companyname

    def set_productname(self, productname):
        self.__productname = productname

    def set_costprice(self, costprice):
        self.__costprice = costprice

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_description(self, description):
        self.__description = description

    def set_status(self, status):
        self.__status = status
