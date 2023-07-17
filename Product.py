class Product:
    def __init__(self, i_d, description, name, price, image):
        self.__i_d = i_d
        self.__description = description
        self.__name = name
        self.__price = price
        self.__quantity = 1
        self.__image = image

    def get_i_d(self):
        return self.__i_d

    def get_description(self):
        return self.__description

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def get_image(self):
        return self.__image

    def set_quantity(self, quantity):
        self.__quantity = quantity
