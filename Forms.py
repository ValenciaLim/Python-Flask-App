from wtforms import Form, StringField, SelectField, RadioField, PasswordField, TextAreaField, IntegerField, DecimalField, DateField, ValidationError, validators
import datetime

#Daffa
class forgotForm(Form):
    Username = StringField('Username', [validators.DataRequired()])
    new_password = PasswordField('New Password', [validators.DataRequired()])
    confirmnew_password = PasswordField("Confirm Password", [validators.DataRequired()])
    def log_check(self):
        log_pass = self.new_password.data
        SpecialSym =['$', '@', '#', '%']
        val = True
        if len(log_pass) <8:
            print("Password must be 8 alphaneumeric and symbol long")
            val = False
        if not any(char.isdigit() for char in log_pass):
            print("Password should have at least one numeral")
        if not any(char.isupper() for char in log_pass):
            print("Password should have at least one Uppercase Letter")
            val = False
        if not any(char.islower() for char in log_pass):
            print("Password should have at least one lowercase letter")
            val = False
        if not any(char in SpecialSym for char in log_pass):
                print("Password should have at least one special symbol")
                val = False
        if val:
            return val

    def confirm_newpass(self):
        pword = self.new_password.data
        cpass = self.confirmnew_password.data
        val = True
        if pword == cpass:
            return val
        else:
            print("Your password  does not match")

class registerForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    mobileNo = StringField('Phone Number', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    Confirm_Password = PasswordField('Confirm Password', [validators.DataRequired()])
    gender = RadioField("Gender", [validators.DataRequired()], choices=[("Male", "Male"), ("Female", "Female")])

    def register_check(self):
        pass_word = self.password.data
        c_pass = self.Confirm_Password.data
        mobnum = self.mobileNo.data
        usercheck = self.username.data
        c_email = self.email.data
        SpecialSym =['$', '@', '#', '%']
        error_msg = []
        valid = ["8", "9"]
        not_allowed = [" "]
        e_list = ["@gmail.com", "@yahoo.com", "@mymail.edu.sg", "@hotmail.com"]

        pass_word = self.password.data
        SpecialSym =['$', '@', '#', '%']
        error_msg = []
        if len(pass_word) <8:
            print("Password must be 8 alphaneumeric and symbol long")
            error_msg.append(1)
        if not any(char.isdigit() for char in pass_word):
            print("Password should have at least one numeral")
            error_msg.append(1)
        if not any(char.isupper() for char in pass_word):
            print("Password should have at least one Uppercase Letter")
            error_msg.append(1)
        if not any(char.islower() for char in pass_word):
            print("Password should have at least one lowercase letter")
            error_msg.append(1)
        if not any(char in SpecialSym for char in pass_word):
                print("Password should have at least one special symbol")
                error_msg.append(1)
        if c_pass != pass_word:
            print("You have not entered the correct password")
            error_msg.append(6)
        if len(mobnum) != 8:
            print("Invalid mobile number 1")
            error_msg.append(7)
        if mobnum[0] not in valid:
            print("Invalid mobile number 2")
            error_msg.append(7)

        if any(char in not_allowed for char in usercheck) and usercheck.isalnum()== False and usercheck.isdigit()==False and usercheck.isalpha()==False:
           error_msg.append(8)
        if c_email[-10::] != "@gmail.com" and  c_email[-10::] != "@yahoo.com":
            error_msg.append(9)

        return error_msg

    def check_acct(self, acc):
        email = self.email.data
        mobnum = self.mobileNo.data
        usercheck = self.username.data
        error_msg2 = []
        for i in acc:
            if i.get_email() == email:
                error_msg2.append(1)
            if i.get_mobileNo() == mobnum:
                error_msg2.append(2)
            if i.get_username() == usercheck:
                error_msg2.append(3)
        return error_msg2

class loginForm(Form):
 Username = StringField('Username', [validators.DataRequired()])
 Password = PasswordField('Password', [validators.DataRequired()])


#Darren
class CreateProductForm(Form):
    ID =  SelectField('', [validators.DataRequired()], choices=[])
    Name = StringField('Model Name', [validators.DataRequired()])
    Price = StringField('Selling Price', [validators.DataRequired()])
    Quantity = StringField('Quantity', [validators.DataRequired()])
    Cpu = StringField('CPU', [validators.DataRequired()])
    Graphic = StringField('Graphics Card', [validators.DataRequired()])
    Weight = StringField('Weight(kg)', [validators.DataRequired()])
    Image = StringField('Image', [validators.DataRequired()])

    def pricenum(self):
        price = self.Price.data
        errormsg = 0
        price = price.replace(".", "")
        print(price)
        if price.isdigit() == False or float(price) <= 0:
            errormsg = 1
        return errormsg

    def quantitynum(self):
        quantity = self.Quantity.data
        errormsg = 0
        if quantity.isdigit() == False or int(quantity) <= 0:
            errormsg = 2
        return errormsg

    def weightnum(self):
        weight = self.Weight.data
        errormsg = 0
        weight = weight.replace(".", "")
        print(weight)
        if weight.isdigit() == False or float(weight) <= 0:
            errormsg = 3
        return errormsg


#Valencia
class PaymentForm(Form):
    paymentMethod = RadioField('', [validators.Optional()], choices=[('Credit/Debit Card', 'Credit/Debit Cards'), ('PayPal', 'PayPal'), ('Cash-on Delivery', 'Cash-on Delivery')])

    cardType = SelectField('Card Type: ', [validators.Optional()], choices=[('MasterCard', 'MasterCard'), ('Visa', 'Visa'), ('American Express', 'American Express')])
    cardNo = StringField('Card Number: ', [validators.Optional()])
    expiryMonth = SelectField('', [validators.Optional()], choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                                    ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')])
    expiryYear = SelectField('', [validators.Optional()], choices=[])
    cvv = StringField('Cvv: ', [validators.Optional()])

    username = StringField('Username: ', [validators.Optional()])
    password = PasswordField('Password: ', [validators.Optional()])

    addresseeName = StringField('Addressee Name: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    fullAddress = StringField('Full Address: ', [validators.Optional()])
    postalCode = StringField('Postal Code: ', [validators.Optional()])

    def  check_address(self):
        error_msg = -1

        full_address = self.fullAddress.data
        postal_code = self.postalCode.data
        if full_address != "":
            if len(postal_code) != 6:
                error_msg = 3

        return error_msg

    def check_credit_debit(self):
        error_msg = []

        card_type = self.cardType.data
        card_no = self.cardNo.data
        if card_type == "MasterCard":
            card_start = ["51", "52", "53", "54", "55"]
            if len(card_no) != 16 or card_no[0:2] not in card_start:
                error_msg.append(1)
        elif card_type == "Visa":
            card_length = [13, 16, 19]
            if len(card_no) not in card_length or card_no[0] != "4":
                error_msg.append(1)
        else:
            card_start = ["34", "37"]
            if len(card_no) != 15 or card_no[0:2] not in card_start:
                error_msg.append(1)

        if card_no.isdigit() == False:
            error_msg.append(1)

        c_v_v = self.cvv.data
        if len(c_v_v) == 3:
            if c_v_v != card_no[-3:]:
                error_msg.append(2)
        else:
            error_msg.append(2)

        return error_msg

    def check_expiry(self):
        error_msg = -1
        month = self.expiryMonth.data
        year = self.expiryYear.data

        now_year = datetime.datetime.now().strftime("%Y")
        now_month = datetime.datetime.now().strftime("%m")
        if year == now_year:
            if int(month) < int(now_month):
                error_msg = 4
        return error_msg


#Jun rong
class CreateUserForm(Form):
 suppliername = StringField('', [
        validators.Length(min=1,max=150),
        validators.DataRequired()])

 companyname = StringField('', [
        validators.optional(),
        validators.length(max=200),
        validators.DataRequired()])

 address = StringField('', [
        validators.optional(),
        validators.length(max=200),
        validators.DataRequired()])

 contactno = StringField('', [
        validators.DataRequired()])

 email = StringField('', [
        validators.Length(min=6, message=(u'Little short for an email address ?')),
        validators.Email(message=(u'That\'s not a valid email address.')),
        validators.DataRequired()])

 remarks = TextAreaField('', [validators.DataRequired()])

 def validate_contactNo(self):

     error = 0

     contactno = self.contactno.data
     if contactno.isdigit() == False:
         error = 1
     if len(contactno) != 8:
         error = 1
     contact_start = ["8", "9", "6"]
     if contactno[0] not in contact_start:
         error = 1

     return error

class CreateStockForm(Form):
    date = DateField('', format='%m/%d/%Y')

    suppliername = SelectField('', [
        validators.DataRequired()], choices=[])

    companyname = StringField('', [
        validators.DataRequired(),
        validators.length(max=200)])

    productname = StringField('', [
        validators.Length(min=3,max=80),
        validators.DataRequired()])

    costprice = StringField('', [
        validators.DataRequired()])

    quantity = StringField('', [
        validators.DataRequired()])

    description = TextAreaField('', [
        validators.DataRequired()])

    def validate_stock(self):

        error = []

        costprice = self.costprice.data
        if costprice.isdigit() == False:
            error.append(1)
        if "-" in costprice:
            error.append(1)
        if int(costprice) == 0:
            error.append(1)

        quantity =  self.quantity.data
        if quantity.isdigit() == False:
            error.append(2)
        if "-" in quantity:
            error.append(2)
        if int(quantity) == 0:
            error.append(2)

        return error
