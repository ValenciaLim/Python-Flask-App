class Laptop:
    countID = 0

    def __init__(self, Name, Price, Quantity, Cpu, Graphic, Weight, Image):
        Laptop.countID += 1
        self.__laptopID = Laptop.countID
        self.__Name = Name
        self.__Price = Price
        self.__Quantity = Quantity
        self.__Cpu = Cpu
        self.__Graphic = Graphic
        self.__Weight = Weight
        self.__Image = Image


    def get_laptopID(self):
        return self.__laptopID
    def get_Name(self):
        return self.__Name
    def get_Price(self):
        return self.__Price
    def get_Quantity(self):
        return self.__Quantity
    def get_Cpu(self):
        return self.__Cpu
    def get_Graphic(self):
        return self.__Graphic
    def get_Weight(self):
        return self.__Weight
    def get_Image(self):
        return self.__Image


    def set_laptopID(self, laptopID):
        self.__laptopID = laptopID
    def set_Name(self, Name):
        self.__Name = Name
    def set_Price(self, Price):
        self.__Price = Price
    def set_Quantity(self, Quantity):
        self.__Quantity = Quantity
    def set_Cpu(self, Cpu):
        self.__Cpu = Cpu
    def set_Graphic(self, Graphic):
        self.__Graphic = Graphic
    def set_Weight(self, Weight):
        self.__Weight = Weight
    def set_Image(self, Image):
        self.__Image = Image
