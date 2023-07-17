import datetime

sales_Dict = {}
class Sales:
    def __init__(self, customer_id, bought_products, sales_id):
        self.__customer_id = customer_id
        self.__sales_id = sales_id
        self.__transaction_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.__bought_product = bought_products
        self.__status = "pending"

    def get_customer_id(self):
        return self.__customer_id

    def get_sales_id(self):
        return self.__sales_id

    def get_transaction_date(self):
        return self.__transaction_date

    def get_bought_products(self):
        return self.__bought_product

    def get_sales_amt(self):
        sales_amt = 0
        for i in self.__bought_product:
            added_amt = float(i['Product'].get_Price())*int(i['Quantity'])
            sales_amt += added_amt

        return sales_amt

    def get_status(self):
        return self.__status

    def set_status(self):
        if self.__status == "pending":
            self.__status = "completed"
        else:
            self.__status = "pending"
