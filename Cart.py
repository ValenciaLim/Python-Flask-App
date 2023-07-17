class Cart:
    def __init__(self):
        self.__items = []

    def get_items(self):
        return self.__items

    def add_items(self, items):
        self.__items.append(items)

    def get_total_amt(self):
        total_amt = 0
        for i in self.__items:
            added_amt = int(i['Product'].get_Price())*int(i['Quantity'])
            total_amt += added_amt
        return total_amt

    def set_items(self):
        self.__items = []
