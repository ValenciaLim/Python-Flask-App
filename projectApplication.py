from flask import Flask, render_template ,request, redirect, url_for, session
from Forms import PaymentForm, loginForm, registerForm, forgotForm, CreateProductForm, CreateUserForm, CreateStockForm
import Cart, Sales, Account, Laptop, Stock, User
import shelve, datetime, random, calendar

app = Flask(__name__)
app.secret_key = "app-project"

ccc = Cart.Cart()
a1 = Account.Admin("vvv", "12345678%Tt", "v@email.com", 82345678, "Female")

@app.route('/')
def default():
 session['account'] = {}
 session['user_status'] = "logout"
 AcctsDict = {}
 db = shelve.open('storage.db', 'c')
 try:
     AcctsDict = db['Accounts']
 except:
     print("Error in retrieving Accounts from storage.db")
 AcctsDict[a1.get_i_d()] = a1
 db['Accounts'] = AcctsDict
 db.close()
 return render_template('home.html')

@app.route('/home')
def home():
 AcctsDict = {}
 db = shelve.open("storage.db", "r")
 try:
     AcctsDict = db['Accounts']
 except:
     print("Error in retrieving Accounts from storage.db")

 db.close()

 user = session['user_status']
 return render_template('home.html', user=user)


#Daffa
@app.route('/forgotpass', methods=['GET', 'POST'])
def forgotpass():
 ForgotForm = forgotForm(request.form)
 if request.method == 'POST' and ForgotForm.validate() and ForgotForm.log_check():
  AcctsDict = {}
  db = shelve.open("storage.db", "w")
  AcctsDict = db['Accounts']

  for key in AcctsDict:
   print(AcctsDict[key].get_password())
   if AcctsDict[key].get_username() == ForgotForm.Username.data:
    AcctsDict[key].set_password(ForgotForm.new_password.data)
    db['Accounts'] = AcctsDict
    print(AcctsDict[key].get_password())
    return redirect(url_for('login'))
  db.close()
 return render_template('forgotpass.html', form=ForgotForm)

@app.route('/login', methods=['GET', 'POST'])
def login():
 LoginForm = loginForm(request.form)
 error_msg = []

 if request.method == 'POST' and LoginForm.validate():
  AcctsDict = {}
  db = shelve.open("storage.db", "r")
  try:
     AcctsDict = db['Accounts']
  except:
     print("Error in retrieving Accounts from storage.db")

  db.close()

  valid_acct = False
  for key in AcctsDict:
   if AcctsDict[key].get_username() == LoginForm.Username.data and AcctsDict[key].get_password() == LoginForm.Password.data:
       valid_acct = True
       if isinstance(AcctsDict[key], Account.Customer):
           accountDict = {"ID": AcctsDict[key].get_i_d(), "Username": AcctsDict[key].get_username(), "MobileNo": AcctsDict[key].get_mobileNo(), "EmailAddress": AcctsDict[key].get_email(), "Address": []}
           address = {"FullAddress": "Sembawang Avenue 10 blk 500 #03-50", "PostalCode": "766500"}
           accountDict["Address"].append(address)
           session["account"] = accountDict
           session['user_status'] = "login"
           return redirect(url_for('shop'))

       if isinstance(AcctsDict[key], Account.Admin):
           return redirect(url_for('dashboard'))
  if valid_acct == False:
      error_msg.append(1)

 return render_template('login.html', form=LoginForm)

@app.route('/register', methods=['GET', 'POST'])
def register():
 RegisterForm = registerForm(request.form)
 error_msg = []
 error_msg2 = []

 if request.method == 'POST' and RegisterForm.validate():
  AcctsDict = {}
  db = shelve.open('storage.db', 'c')
  try:
   AcctsDict = db['Accounts']
  except:
   print("Error in retrieving Accounts from storage.db")

  accountList = []
  for key in AcctsDict:
   account = AcctsDict.get(key)
   accountList.append(account)

  error_msg = RegisterForm.register_check()
  error_msg2 = RegisterForm.check_acct(accountList)
  if len(error_msg) == 0:
   if len(error_msg2) == 0:
    accountID = random.randint(1000, 9999)
    while accountID in AcctsDict:
        accountID = random.randint(1000, 9999)
    account = Account.Customer(RegisterForm.username.data, RegisterForm.password.data, RegisterForm.email.data, RegisterForm.mobileNo.data,RegisterForm.gender.data)
    account.set_i_d(accountID)
    AcctsDict[account.get_i_d()] = account
    db['Accounts'] = AcctsDict
    db.close()

    accountDict = {"ID": account.get_i_d(), "Username": account.get_username(), "MobileNo": account.get_mobileNo(), "EmailAddress": account.get_email(), "Address": []}
    address = {"FullAddress": "Sembawang Avenue 10 blk 500 #03-50", "PostalCode": "766500"}
    accountDict["Address"].append(address)
    session["account"] = accountDict
    session['user_status'] = "login"
    return redirect(url_for('home'))
 return render_template('register.html', form=RegisterForm, error_msg=error_msg, error_msg2=error_msg2)

@app.route("/viewacct")
def viewacct():
 AcctsDict = {}
 db = shelve.open("storage.db", "r")
 try:
     AcctsDict=db['Accounts']
 except:
     print("Error in retrieving Accounts from storage.db")
 db.close()

 accountList = []
 for key in AcctsDict:
  account = AcctsDict.get(key)
  accountList.append(account)
 return render_template("viewacct.html", accountList = accountList)

@app.route('/deleteAcctUser/<id>', methods = ["POST"])
def deleteAcctUser(id):
 AcctsDict = {}
 db = shelve.open("storage.db", "w")
 AcctsDict = db["Accounts"]

 AcctsDict.pop(id)
 db["Accounts"] = AcctsDict
 db.close()
 return redirect(url_for("viewacct"))

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route("/wishlist")
def wishlist():
    account = session['account']
    user = session['user_status']

    AcctsDict = {}
    db = shelve.open("storage.db", "r")
    try:
        AcctsDict=db['Accounts']
    except:
        print("Error in retrieving Accounts from storage.db")
    db.close()

    if user=="login":
        acct_obj = AcctsDict.get(account["ID"])
        wishlist = acct_obj.get_wishlist()
        return render_template('wishlist.html', wishlist = wishlist, user=user)
    else:
        return redirect(url_for('login'))

@app.route('/deletewish/<int:id>', methods=["POST"])
def deletewish(id):
 account = session['account']
 AcctsDict = {}
 db = shelve.open("storage.db", "w")
 AcctsDict = db["Accounts"]

 acct_obj = AcctsDict[account["ID"]]
 del acct_obj.get_wishlist()[id]
 db["Accounts"] = AcctsDict

 db.close()
 return redirect(url_for("wishlist"))

@app.route('/addwish/<int:id>', methods = ["POST"])
def addwish(id):
 account = session['account']
 user = session['user_status']

 AcctsDict = {}
 laptopDict = {}
 db = shelve.open("storage.db", "w")
 AcctsDict = db["Accounts"]
 laptopDict = db['Laptops']

 if user == "login":
     acct_obj = AcctsDict[account["ID"]]
     wishlist = acct_obj.get_wishlist()

     in_wishlist = False
     for i in wishlist:
         if i.get_laptopID() == id:
             in_wishlist = True

     if in_wishlist == False:
         wishlist.append(laptopDict[id])
         acct_obj.set_wishlist(wishlist)
         db['Accounts'] = AcctsDict

     db.close()
     return redirect(url_for("wishlist"))
 else:
     return redirect(url_for('login'))


#Darren
@app.route("/shop")
def shop():
    laptopsDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        laptopsDict = db['Laptops']
    except:
        print("Error in retrieving Accounts from storage.db")
    db.close()

    def bylaptopID_key(laptop):
        return laptop.get_laptopID()

    laptopsList = []
    for key in laptopsDict:
        laptop = laptopsDict.get(key)
        laptopsList.append(laptop)
    laptopsList=sorted(laptopsList,key=bylaptopID_key)

    user = session['user_status']

    return render_template('shop.html', laptopsList=laptopsList, count=len(laptopsList), user=user)

@app.route('/toIndividualProduct', methods=['POST'])
def toIndividualProduct():
    product_id = request.form.get('laptopID')
    return redirect(url_for('shopIndividual', id=product_id))

@app.route('/shopIndividual/<int:id>')
def shopIndividual(id):
    laptopsDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        laptopsDict = db['Laptops']
    except:
        print("Error in retrieving Accounts from storage.db")
    db.close()

    user = session['user_status']

    return render_template('shopIndividual.html', laptop=laptopsDict[id], user=user)

@app.route('/Addproduct', methods=['GET', 'POST'])
def Addproduct():
    createProductForm = CreateProductForm(request.form)
    errormsg = []

    stocksDict = {}
    db = shelve.open('storage.db', 'r')
    stocksDict = db['Stocks']
    db.close()

    stockID_list = []
    for key in stocksDict:
        options = str(stocksDict[key].get_stockID()) + "-" + stocksDict[key].get_productname()
        stockID_list.append(options)

    createProductForm.ID.choices = [(i,i) for i in stockID_list]

    if request.method == 'POST' and createProductForm.validate():
        laptopsDict = {}
        db = shelve.open('storage.db', 'c')

        try:
            laptopsDict = db['Laptops']
        except:
            print("Error in retrieving Users from storage.db.")

        errormsg1 = createProductForm.pricenum()
        errormsg2 = createProductForm.quantitynum()
        errormsg3 = createProductForm.weightnum()

        if errormsg1 != 0:
            errormsg.append(errormsg1)
        if errormsg2 != 0:
            errormsg.append(errormsg2)
        if errormsg3 != 0:
            errormsg.append(errormsg3)

        if len(errormsg) == 0:
            laptop = Laptop.Laptop(createProductForm.Name.data, createProductForm.Price.data, createProductForm.Quantity.data,
                                   createProductForm.Cpu.data, createProductForm.Graphic.data, createProductForm.Weight.data, createProductForm.Image.data)
            laptopsDict[laptop.get_laptopID()] = laptop
            db['Laptops'] = laptopsDict

            db.close()

            return redirect(url_for('Manageproduct'))

    return render_template('Addproduct.html', form=createProductForm, errormsg=errormsg)

@app.route('/Manageproduct') #Admin
def Manageproduct():
    laptopsDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        laptopsDict = db['Laptops']
    except:
        print("Error in retrieving Users from storage.db.")
    db.close()

    laptopsList = []
    for key in laptopsDict:
        laptop = laptopsDict.get(key)
        laptopsList.append(laptop)

    return render_template('Manageproduct.html', laptopsList=laptopsList, count=len(laptopsList))

@app.route('/Updateproduct/<int:id>/<errormsg>', methods=['GET', 'POST'])
def updateProduct(id, errormsg):
    updateProductForm = CreateProductForm(request.form)
    if request.method == 'POST':
        errormsg = ""
        laptopDict = {}
        db = shelve.open('storage.db', 'w')
        laptopDict = db['Laptops']

        errormsg1 = updateProductForm.pricenum()
        errormsg2 = updateProductForm.quantitynum()
        errormsg3 = updateProductForm.weightnum()

        if errormsg1 != 0:
            errormsg+= str(errormsg1)
        if errormsg2 != 0:
            errormsg+= str(errormsg1)
        if errormsg3 != 0:
            errormsg+= str(errormsg1)

        if len(errormsg) == 0:
            laptop = laptopDict.get(id)
            laptop.set_Image(updateProductForm.Image.data)
            laptop.set_Name(updateProductForm.Name.data)
            laptop.set_Price(updateProductForm.Price.data)
            laptop.set_Quantity(updateProductForm.Quantity.data)
            laptop.set_Cpu(updateProductForm.Cpu.data)
            laptop.set_Graphic(updateProductForm.Graphic.data)
            laptop.set_Weight(updateProductForm.Weight.data)
            db['Laptops'] = laptopDict
            db.close()
            return redirect(url_for('Manageproduct'))
        else:
            return redirect(url_for('updateProduct', id=id, form=updateProductForm, errormsg=errormsg))
    else:
        laptopDict = {}
        db = shelve.open('storage.db', 'r')
        try:
            laptopDict = db['Laptops']
        except:
            print("Error in retrieving Users from storage.db.")
        db.close()

        laptop = laptopDict.get(id)
        updateProductForm.Image.data = laptop.get_Image()
        updateProductForm.Name.data = laptop.get_Name()
        updateProductForm.Price.data = laptop.get_Price()
        updateProductForm.Quantity.data = laptop.get_Quantity()
        updateProductForm.Cpu.data = laptop.get_Cpu()
        updateProductForm.Graphic.data = laptop.get_Graphic()
        updateProductForm.Weight.data = laptop.get_Weight()

        return render_template('Updateproduct.html', form=updateProductForm, errormsg=errormsg)

@app.route('/Deleteproduct/<int:id>', methods=['POST']) #Admin
def Deleteproduct(id):
    laptopsDict = {}
    db = shelve.open('storage.db', 'w')
    laptopsDict = db['Laptops']

    laptopsDict.pop(id)
    db['Laptops'] = laptopsDict
    db.close()

    return redirect(url_for('Manageproduct'))

@app.route('/addToCart/<id>', methods=['POST'])
def addToCart(id):
    laptopsDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        laptopsDict = db['Laptops']
    except:
        print("Error in retrieving Users from storage.db.")
    db.close()

    cart_item = {'Product':laptopsDict[int(id)], 'Quantity': 1}
    ccc.add_items(cart_item)
    return redirect(url_for('retrieveCart'))


# Valencia
@app.route('/retrieveCart')
def retrieveCart():
    user = session['user_status']
    return render_template('retrieveCart.html', cart=ccc.get_items(), count=len(ccc.get_items()), totalamt=ccc.get_total_amt(), user=user)

@app.route('/deleteCart_all', methods=['POST'])
def deleteCart_all():
 delete_item_id = request.form.getlist('check')
 delete_item = []
 for i in ccc.get_items():
     if str(i['Product'].get_laptopID()) in delete_item_id:
         delete_item.append(i)
 for i in delete_item:
  ccc.get_items().remove(i)
 return redirect(url_for('retrieveCart'))

@app.route('/deleteCart/<int:id>', methods=['POST'])
def deleteCart(id):
 ccc.get_items().pop(id)
 return redirect(url_for('retrieveCart'))

@app.route('/editQuantity', methods=['POST'])
def editQuantity():
 product_quantity = request.form.getlist('quantities')
 for i in ccc.get_items():
     i['Quantity'] = product_quantity[ccc.get_items().index(i)]
 return redirect(url_for('paymentDetails'))

@app.route('/paymentDetails', methods=['GET', 'POST'])
def paymentDetails():
 account = session["account"]
 user = session['user_status']

 if user == "login":
     contact = {"MobileNo": account["MobileNo"], "EmailAddress": account["EmailAddress"]}

     method_index = -1
     error_msg = []

     paymentForm = PaymentForm(request.form)
     year_now = datetime.datetime.now().strftime("%Y")
     paymentForm.expiryYear.choices = [(str(i),str(i)) for i in range(int(year_now), int(year_now)+4)]

     if request.method == 'POST' and paymentForm.validate():
      e = paymentForm.check_address()
      e_date = paymentForm.check_expiry()
      if e != -1:
       error_msg.append(e)

      if e_date != -1:
       error_msg.append(e_date)

      if paymentForm.fullAddress.data != "":
       new = {"FullAddress": paymentForm.fullAddress.data, "PostalCode": paymentForm.postalCode.data}
       account["Address"].append(new)
       session["account"] = account
       address_index = -1
      else:
       address_index = 0
       select = request.form.get('select')
       account = session["account"]
       for a in account["Address"]:
        if select[-7:] == a["PostalCode"]:
         address_index = account["Address"].index(a)

      if paymentForm.paymentMethod.data == "Credit/Debit Card":
       method_index = 0
       e = paymentForm.check_credit_debit()
       if len(e) != 0:
        for i in e:
         error_msg.append(i)

       if len(error_msg) == 0:
        expiry = request.form.get('expiryMonth') + "/" + request.form.get('expiryYear')
        payment_info = {"CardType": request.form.get('cardType'), "CardNo": request.form.get('cardNo'), "ExpiryDate": expiry, "CVV": request.form.get('cvv'), "AddresseeName": paymentForm.addresseeName.data}
        session["payment"] = payment_info
        return redirect(url_for('checkout', x=address_index, y=method_index))

      elif paymentForm.paymentMethod.data == "PayPal":
       payment_info = {"CardType": "", "CardNo": "", "ExpiryDate": "", "CVV": "", "AddresseeName": ""}
       session["payment"] = payment_info
       method_index = 1
       return redirect(url_for('checkout', x=address_index, y=method_index))

      else:
       payment_info = {"CardType": "", "CardNo": "", "ExpiryDate": "", "CVV": "", "AddresseeName": ""}
       session["payment"] = payment_info
       method_index = 2
       return redirect(url_for('checkout', x=address_index, y=method_index))

     return render_template('paymentDetails.html', form=paymentForm, contact=contact, address=account["Address"], error_msg=error_msg, method_index=method_index, user=user)
 else:
     return redirect(url_for('login'))

@app.route('/checkout/<x>/<int:y>/', methods=['GET', 'POST'])
def checkout(x, y):
 payment = session["payment"]
 account = session["account"]
 user = session['user_status']
 contact = {"MobileNo": account["MobileNo"], "EmailAddress": account["EmailAddress"]}

 return render_template('checkout.html', payment=payment, address=account["Address"][int(x)], contact=contact, cart=ccc.get_items(), totalamt=ccc.get_total_amt(), method=y, user=user)

@app.route('/addSales', methods=['POST'])
def addSales():
 account = session["account"]

 salesDict = {}
 db = shelve.open('storage.db', 'c')
 try:
  salesDict = db['Sales']
 except:
  print("Error in retrieving Users from storage.db.")
 sales_Id = random.randint(1000, 9999)
 sales = Sales.Sales(account["ID"], ccc.get_items(), sales_Id)
 salesDict[sales.get_sales_id()] = sales
 print(salesDict)
 db['Sales'] = salesDict
 db.close()

 ccc.set_items()

 return ('', 204)

@app.route('/retrieveOrders', methods=["GET", "POST"])
def retrieveOrders():
    salesDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        salesDict = db['Sales']
    except:
        print("Error in retrieving Users from storage.db.")
    db.close()

    if request.method == "POST":
        sorted_sales = {}
        sort_option = request.form.get('order_sort')
        if sort_option == "Transaction Date":
            for key in salesDict:
                if salesDict[key].get_transaction_date() not in sorted_sales:
                    sorted_sales[salesDict[key].get_transaction_date()] = []
                sorted_sales[salesDict[key].get_transaction_date()].append(salesDict[key])
        elif sort_option == "Customer ID":
            for key in salesDict:
                if salesDict[key].get_customer_id() not in sorted_sales:
                    sorted_sales[salesDict[key].get_customer_id()] = []
                sorted_sales[salesDict[key].get_customer_id()].append(salesDict[key])
        else:
            for key in salesDict:
                if salesDict[key].get_status() not in sorted_sales:
                    sorted_sales[salesDict[key].get_status()] = []
                sorted_sales[salesDict[key].get_status()].append(salesDict[key])
        return render_template('retrieveOrders.html', salesDict=sorted_sales, sort=sort_option)
    else:
        sales_by_date = {}
        for key in salesDict:
            if salesDict[key].get_transaction_date() not in sales_by_date:
                sales_by_date[salesDict[key].get_transaction_date()] = []
            sales_by_date[salesDict[key].get_transaction_date()].append(salesDict[key])
        return render_template('retrieveOrders.html', salesDict=sales_by_date, sort="Transaction Date")

@app.route('/updateOrderStatus/<id>', methods=['POST'])
def updateOrderStatus(id):
    salesDict = {}
    db = shelve.open('storage.db', 'w')
    salesDict = db['Sales']

    for key in salesDict:
        if salesDict[key].get_sales_id() == int(id):
            salesDict[key].set_status()

    db['Sales'] = salesDict
    db.close()
    return redirect(url_for('retrieveOrders'))

@app.route('/UserOrders')
def UserOrders():
    account = session["account"]
    user = session['user_status']

    salesDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        salesDict = db['Sales']
    except:
        print("No sales storage")
    db.close()

    if user=="login":
        OrderList = []
        for key in salesDict:
            if salesDict[key].get_customer_id() == account["ID"]:
                OrderList.append(salesDict[key])

        return render_template('UserOrders.html', OrderList=OrderList, user=user)
    else:
        return redirect(url_for('login'))

@app.route('/cancelOrder/<int:id>/<int:index>', methods=['POST'])
def cancelOrder(id, index):
    salesDict = {}
    db = shelve.open('storage.db', 'w')
    salesDict = db['Sales']

    del salesDict[id].get_bought_products()[index]
    delete_key = []

    for key in salesDict:
        if len(salesDict[key].get_bought_products()) == 0:
            delete_key.append(key)

    for i in delete_key:
        salesDict.pop(i)

    db['Sales'] = salesDict
    db.close()

    return redirect(url_for('UserOrders'))

@app.route('/dashboard')
def dashboard():
    now = datetime.datetime.now()

    salesDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        salesDict = db['Sales']
    except:
        print("Error retrieving from storage.db")
    db.close()

    months = {}
    for key in salesDict:
        year = salesDict[key].get_transaction_date().split('-')
        if year[0] == now.strftime("%Y"): #default is year 2020
            if year[1] not in months:
                months[year[1]] = salesDict[key].get_sales_amt()
            else:
                months[year[1]] = months[year[1]] + salesDict[key].get_sales_amt()

    days = {}
    for key in salesDict:
        year = salesDict[key].get_transaction_date().split('-')
        if year[1] == now.strftime("%m"):
            if year[2] not in days:
                days[year[2]] = salesDict[key].get_sales_amt()
            else:
                days[year[2]] = days[year[2]] + salesDict[key].get_sales_amt()

    months_y = []
    months_x = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    this_month = now.strftime("%m")
    months_x = months_x[0:months_x.index(this_month)+1]
    for i in months_x:
        if i in months:
            months_y.append(float(months[i]))
        else:
            months_y.append(0.0)

    days_y = []
    days_x = []

    days_in_the_month = calendar.monthrange(now.year, now.month)[-1]
    for i in range(1, days_in_the_month+1):
        days_x.append(i)
    this_day = datetime.datetime.now().strftime("%d")
    days_x = days_x[0:days_x.index(int(this_day))+1]
    for i in days_x:
        if i in days:
            days_y.append(float(days[i]))
        else:
            days_y.append(0.0)

    return render_template('dashboard.html', values_month=months_y, labels_month=months_x, revenue_month=sum(months_y),
                           values_day=days_y, labels_day=days_x, revenue_day=sum(days_y))


#Jun Rong
@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    error_msg = 0
    createUserForm = CreateUserForm(request.form)

    if request.method == 'POST' and createUserForm.validate():
        usersDict = {}
        db = shelve.open('storage.db', 'c')
        try:
            usersDict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        error_msg = createUserForm.validate_contactNo()
        if error_msg == 0:
            duplicate = False
            for key in usersDict:
                if usersDict[key].get_suppliername().upper() == createUserForm.suppliername.data.upper() and\
                    usersDict[key].get_companyname().upper() == createUserForm.companyname.data.upper()and\
                    usersDict[key].get_address().upper() == createUserForm.address.data.upper() and \
                    usersDict[key].get_contactno() == createUserForm.contactno.data:
                    print("duplicate data")
                    duplicate = True

            if duplicate == False:
                print(duplicate)
                user = User.User(createUserForm.suppliername.data,createUserForm.companyname.data,createUserForm.address.data,createUserForm.contactno.data, createUserForm.email.data, createUserForm.remarks.data)
                usersDict[user.get_supplierID()] = user
                db['Users'] = usersDict
                # Test codes
                db.close()
                return redirect(url_for('retrieveUsers'))
            else:
                print(duplicate)
                return render_template('createUser.html', form=createUserForm, duplicate=duplicate)
    return render_template('createUser.html', form=createUserForm, error_msg=error_msg)

@app.route('/retrieveUsers')
def retrieveUsers():
 usersDict = {}
 db = shelve.open('storage.db', 'r')
 try:
     usersDict = db['Users']
 except:
     print("Error in retrieving Users from storage.db.")
 db.close()

 usersList = []
 for key in usersDict:
     user = usersDict.get(key)
     usersList.append(user)

 return render_template('retrieveUsers.html',usersList=usersList, count=len(usersList))

@app.route('/updateUser/<int:id>/<int:error>', methods=['GET', 'POST'])
def updateUser(id, error):
    updateUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        userDict = {}
        db = shelve.open('storage.db', 'w')
        userDict = db['Users']
        error = updateUserForm.validate_contactNo()
        if error == 0:
            user = userDict.get(id)
            user.set_suppliername(updateUserForm.suppliername.data)
            user.set_companyname(updateUserForm.companyname.data)
            user.set_address(updateUserForm.address.data)
            user.set_contactno(updateUserForm.contactno.data)
            user.set_email(updateUserForm.email.data)
            user.set_remarks(updateUserForm.remarks.data)
            db['Users'] = userDict
            db.close()
            return redirect(url_for('retrieveUsers'))
        else:
            return redirect(url_for('updateUser',id = id, form=updateUserForm, error = error))
    else:
        userDict = {}
        db = shelve.open('storage.db', 'r')
        try:
            userDict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        db.close()
        user = userDict.get(id)
        updateUserForm.suppliername.data = user.get_suppliername()
        updateUserForm.companyname.data = user.get_companyname()
        updateUserForm.address.data = user.get_address()
        updateUserForm.contactno.data = user.get_contactno()
        updateUserForm.email.data = user.get_email()
        updateUserForm.remarks.data = user.get_remarks()
        return render_template('updateUser.html', form=updateUserForm,  error = error )

@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
 usersDict = {}
 db = shelve.open('storage.db', 'w')
 usersDict = db['Users']
 usersDict.pop(id)
 db['Users'] = usersDict
 db.close()
 return redirect(url_for('retrieveUsers'))

@app.route('/createStock', methods=['GET', 'POST'])
def createStock():
 error = []
 createStockForm = CreateStockForm(request.form)

 usersDict = {}
 db = shelve.open('storage.db', 'r')
 usersDict = db['Users']
 db.close()

 #Dict containing the the supplier name (key) then the company name in the list
 supplierDict = {}
 for key in usersDict:
     suppliername = usersDict[key].get_suppliername()
     companyname = usersDict[key].get_companyname()
     supplierid = usersDict[key].get_supplierID()
     supplierkey = str(supplierid) + suppliername
     if supplierkey not in supplierDict:
         supplierkey = str(supplierid) + suppliername
         supplierDict[supplierkey] = []
     supplierDict[supplierkey].append(companyname)

 createStockForm.suppliername.choices = [(i,i) for i in supplierDict]
 print(supplierDict)

 if request.method == 'POST' and createStockForm.validate():
    stocksDict = {}
    db = shelve.open('storage.db', 'c')
    try:
        stocksDict = db['Stocks']
    except:
        print("Error in retrieving Stocks from storage.db.")

    error = createStockForm.validate_stock()
    if len(error) == 0:
        exist = False
        for key in stocksDict:
            if stocksDict[key].get_date() == createStockForm.date.data and \
            stocksDict[key].get_productname().upper() == createStockForm.productname.data.upper() and \
            stocksDict[key].get_costprice() == createStockForm.costprice.data and \
            stocksDict[key].get_suppliername().upper() == createStockForm.suppliername.data.upper():
                    exist = True
                    old_quantity = stocksDict[key].get_quantity()
                    new_quantity = createStockForm.quantity.data
                    print("Duplicate data")
                    print(old_quantity)
                    print(new_quantity)
                    quantity = int(new_quantity) + int(old_quantity)
                    print(quantity)
                    stocksDict[key].set_quantity(quantity)
        if exist == False:
            stock = Stock.Stock(createStockForm.date.data,createStockForm.suppliername.data,createStockForm.companyname.data, createStockForm.productname.data,createStockForm.costprice.data, createStockForm.quantity.data, createStockForm.description.data)
            stocksDict[stock.get_stockID()] = stock
        db['Stocks'] = stocksDict

        return redirect(url_for('retrieveStocks'))
 return render_template('createStock.html', form=createStockForm, error = error, supplierDict=supplierDict)

@app.route('/retrieveStocks')
def retrieveStocks():

    stocksDict = {}
    salesDict = {}
    db = shelve.open('storage.db', 'w')
    try:
        stocksDict = db['Stocks']
        salesDict = db["Sales"]
    except:
        print("Error retrieving from storage.db")

    stockID_List = []
    for key in stocksDict:
        ID = stocksDict[key].get_stockID()
        stockname = stocksDict[key].get_productname()
        stockID = str(ID) +"-"+ stockname
        stock_quantity = stocksDict[key].get_quantity()
        print(stock_quantity)
        if int(stock_quantity) >= 1000:
            stocksDict[key].set_status("High Stock")
        elif int(stock_quantity) <= 100:
            stocksDict[key].set_status("Low Stock")
        elif int(stock_quantity) >100 and int(stock_quantity) <1000:
            stocksDict[key].set_status("Sufficient Stock")

        stockID_List.append(stockID)
        print(stockID_List)

    productID_list = []
    for key in stocksDict:
        options = str(stocksDict[key].get_stockID()) + "-" + stocksDict[key].get_productname()
        productID_list.append(options)
        print(productID_list)

    for key in salesDict:
          products = salesDict[key].get_bought_products()
          for i in range(len(products)):
              if products[i]['Product'].get_laptopID() in stocksDict:
                  product_stock = stocksDict[products[i]['Product'].get_laptopID()]
                  orders_quantity = int(products[i]['Quantity'])
                  new_stock = int(product_stock.get_quantity()) - orders_quantity
                  product_stock.set_quantity(new_stock)
                  print(new_stock)
    db['Stock'] = stocksDict

    stocksList = []
    for item in stocksDict:
         stock =stocksDict.get(item)
         stocksList.append(stock)
    return render_template('retrieveStocks.html', stocksList=stocksList, count=len(stocksList))

@app.route('/updateStock/<int:id>/', methods=['GET', 'POST'])
def updateStock(id):
    updateStockForm = CreateStockForm(request.form)

    usersDict = {}
    db = shelve.open('storage.db', 'r')
    try:
        usersDict = db['Users']
    except:
        print("Error in retrieving Stocks from storage.db.")
    db.close()

    supplierDict = {}
    for key in usersDict:
         suppliername = usersDict[key].get_suppliername()
         companyname = usersDict[key].get_companyname()
         supplierid = usersDict[key].get_supplierID()
         supplierkey = str(supplierid) + suppliername
         if supplierkey not in supplierDict:
             supplierkey =  suppliername + str(supplierid)
             supplierDict[supplierkey] = []
             supplierDict[supplierkey].append(companyname)
    updateStockForm.suppliername.choices = [(i,i) for i in supplierDict]

    if request.method == 'POST' and updateStockForm.validate():
        stockDict = {}
        db = shelve.open('stock.db', 'w')
        stockDict = db['Stock']
        stock = stockDict.get(id)
        stock.set_stockID(updateStockForm.stockID.data)
        stock.set_suppleirname(updateStockForm.suppliername.data)
        stock.set_companyname(updateStockForm.companyname.data)
        stock.set_productname(updateStockForm.productname.data)
        stock.set_costprice(updateStockForm.costprice.data)
        stock.set_quantity(updateStockForm.quantity.data)
        stock.set_description(updateStockForm.description.data)

        db['Stocks'] = stockDict
        db.close()
        return redirect(url_for('retrieveUsers'))
    else:
        stockDict = {}
        db = shelve.open('storage.db', 'r')
        try:
            stockDict = db['Stocks']
        except:
            print("Error in retrieving Stocks from storage.db.")
        db.close()
        stock = stockDict.get(id)
        updateStockForm.date.data = stock.get_date()
        updateStockForm.suppliername.data = stock.get_suppliername()
        updateStockForm.companyname.data = stock.get_companyname()
        updateStockForm.productname.data = stock.get_productname()
        updateStockForm.costprice.data = stock.get_costprice()
        updateStockForm.quantity.data = stock.get_quantity()
        updateStockForm.description.data = stock.get_description()
        return render_template('updateStock.html', form=updateStockForm, supplierDict=supplierDict)

@app.route('/deleteStock/<int:id>', methods=['POST'])
def deleteStock(id):
 stocksDict = {}
 db = shelve.open('storage.db', 'w')
 stocksDict = db['Stocks']
 stocksDict.pop(id)
 db['Stocks'] = stocksDict
 db.close()
 return redirect(url_for('retrieveStocks'))

@app.route("/color")
def color():
    return render_template("color.html")

if __name__ == '__main__':
 app.run()
