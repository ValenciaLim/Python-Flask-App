class Account:
    def __init__(self,username, password, email, mobileNo, gender):
        self.__username = username
        self.__password = password
        self.__email = email
        self.__mobileNo = mobileNo
        self.__gender = gender


    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_mobileNo(self):
        return self.__mobileNo

    def get_gender(self):
        return self.__gender

    def set_username(self,username):
        self.__username = username

    def set_password(self,password):
        self.__password = password


class Admin(Account):
    def __init__(self, username, password, email, mobileNo, gender):
        super().__init__(username, password, email, mobileNo, gender)
        self.__i_d = "A" + "0"

    def get_i_d(self):
        return self.__i_d

    def set_i_d(self, i_d):
        self.__i_d = "A" + str(i_d)

class Customer(Account):
    def __init__(self, username, password, email, mobileNo, gender):
        super().__init__(username,password, email, mobileNo, gender)
        self.__address = ""
        self.__wishlist = []
        self.__i_d = "C" + "0"

    def get_i_d(self):
        return self.__i_d

    def get_wishlist(self):
        return self.__wishlist

    def set_i_d(self, i_d):
        self.__i_d = "C" + str(i_d)

    def set_wishlist(self, wishlist):
        self.__wishlist = wishlist
