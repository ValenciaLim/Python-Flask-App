class User:
    countID = 0
    def __init__(self, suppliername, companyname, address, contactno, email, remarks):
        User.countID +=1
        self.__supplierID = User.countID
        self.__suppliername = suppliername
        self.__companyname = companyname
        self.__address = address
        self.__contactno = contactno
        self.__email = email
        self.__remarks = remarks

    def get_supplierID(self):
        return self.__supplierID

    def get_suppliername(self):
        return self.__suppliername

    def get_companyname(self):
        return self.__companyname

    def get_address(self):
        return self.__address

    def get_contactno(self):
        return self.__contactno

    def get_email(self):
        return self.__email

    def get_remarks(self):
        return self.__remarks


    def set_supplierID(self, supplierID):
        self.__supplierID = supplierID

    def set_suppliername(self, suppliername):
        self.__suppliername = suppliername

    def set_companyname(self, companyname):
        self.__companyname =companyname

    def set_address(self, address):
        self.__address = address

    def set_contactno(self, contactno):
        self.__contactno = contactno

    def set_email(self, email):
        self.__email = email

    def set_remarks(self, remarks):
        self.__remarks = remarks
