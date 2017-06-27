import cx_Oracle                #Imports all the classes and functions necessary for establishing a connection from Oracle Database.
class customer:
    def __init__(self):
        self.conn = cx_Oracle.connect('TEST/root@xe')
        print("connected")
        self.cur = self.conn.cursor()   #creating an object of a cursor class

    def new_coustomer(self, fname, lname, mobno, add1, add2, city, state, pin, gen, email, password): #function to create new customer.
        self.cur.execute("insert into  customer values (C_ID_VAL.NEXTVAL,:pram1,:pram2,:pram3,:pram4,:pram5,:pram6,:pram7,:pram8,:pram9,:pram10,:pram11)",(fname, lname, mobno, add1, add2, city, state, pin, gen, email, password))
        query = "select C_ID_VAL.currval from dual"
        self.cur.execute(query)
        ren = self.cur.fetchall()
        ren = list(sum(ren, ()))
        print("Welcome "+fname+"!")
        print("Your coustomer ID= ", ren[0])
        print("Your password= ", password)
        self.conn.commit()


class CurrentAccount:
    def __init__(self):
        self.conn = cx_Oracle.connect('TEST/root@xe')
        print("connected")
        self.cur = self.conn.cursor()

    def open_account(self, c_id):   #open new current account 
        bal = int(input("enter balance you want to enter in your new account: "))
        if bal<=0:  #checking for a valid amount
            print("Please enter a valid amount.\n")
        else:
            self.cur.execute("insert into current_acc values(ACCOUNT_NO_VAL2.NEXTVAL,:pram1,'ACTIVE',to_date(sysdate,'DD/MM/YY'),NUll,:pram2)",(c_id, bal))
            self.conn.commit()
            print("Current Account Open Successful\n")

    def deposit(self, c_id):    #function for deposit
        amount = int(input("Enter amount to deposit: "))
        if amount<=0:
            print("Please enter a valid amount.\n")
        else:
            self.cur.execute("select c_id from current_acc")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            if (int(c_id) in ret):  #to check whether customer ID exists or not
                pass
            else:
                print(c_id + " does not have a Current Account\n")
                return
            self.cur.execute("select balance from current_acc where c_id=" + c_id + "")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            ret = ret[0]
            new_amount = ret + amount
            self.cur.execute("UPDATE current_acc SET balance=:1 where c_id=:2", (new_amount, c_id))     #UPDATE BALANCE IN CURRENT ACCOUNT FOR RESPECTIVE C_ID
            # self.conn.commit()
            self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'deposit',:2,:3,'Current Account')",(c_id, amount, new_amount)) #UPDATE HISTORY TABLE
            self.conn.commit()      #COMMIT ALL THE VALUES
            print("Amount Deposited Successfully\n")

    def withdraw(self, c_id):       #FUNCTION TO WITHDRAW FROM CURRENT_ACCOUNT
        amount = int(input("enter amount to withdraw: "))
        if amount<=0:
            print("Please enter a valid amount.\n")
        else:
            self.cur.execute("select c_id from current_acc")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            if (int(c_id) in ret):
                pass
            else:
                print(c_id + " does not have a Current Account.\n")
                return
            self.cur.execute("select balance from current_acc where c_id=" + c_id + "")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            ret = ret[0]
            if ret < amount:
                print("your account has " + str(ret) + " amount")
                return
            else:
                ret = ret - amount
                self.cur.execute("UPDATE current_acc SET balance=:1 where c_id=:2", (str(ret), c_id))
                self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'withdrawl',:2,:3,'Current Account')",(c_id, amount, ret))
                self.conn.commit()
                print("Amount Withdrawn Successfully\n")

    def transfer(self, c_id):       #FUNCTION TO TRANFER FROM CURRENT ACCOUNT
        print("enter amount to transfer")
        amount = int(input())
        if amount<=0:
            print("Please enter a valid amount.\n")
            return
        else:
            self.cur.execute("select c_id from current_acc")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            if (int(c_id) in ret):
                pass
            else:
                print(c_id + " does not have a current account\n")
                return
            self.cur.execute("select balance from current_acc where c_id=" + c_id + "")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            ret = ret[0]
            if ret < amount:        #CHECKING WHETHER AMOUNT ENTERED IS GREATER THAN THE BALANCE
                print("your account has " + str(ret) + " amount")
                return
            print("enter customer ID in which you want to transfer the amount: ")
            c_id1 = input()
            print("1. transfer into saving account\n2. transfer into current account")
            ch = int(input())
            if ch == 1:
                try:
                    self.cur.execute("select c_id from saving_acc")
                    ret = self.cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id1) in ret):
                        pass
                    else:
                        print(c_id1 + " does not have a saving account.\n")
                        return
                    self.cur.execute("select status from SAVING_ACC where c_id=" + c_id1 + "")
                    stu = self.cur.fetchall()
                    stu = list(sum(stu, ()))
                    stu = stu[0]
                    if str(stu) == "LOCK" or str(stu) == "CLOSE":
                        print(c_id1 + " is locked or closed.\n")
                        return
                    else:
                        self.cur.execute("select balance from current_acc where c_id=" + c_id + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret - amount
                        self.cur.execute("UPDATE current_acc SET balance=:1 where c_id=:2", (str(ret), c_id))
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'transfer',:2,:3,'Current Account')",(c_id, amount, ret))
                        self.conn.commit()
                        self.cur.execute("select balance from saving_acc where c_id=" + c_id1 + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret + amount
                        self.cur.execute("UPDATE saving_acc SET balance=:1 where c_id=:2", (str(ret), c_id1))
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'deposit',:2,:3,'Saving Account')",(c_id1, amount, ret))
                        self.conn.commit()
                        print("Transaction successful.\n")
                except Exception as e:
                    print(e)
            elif ch == 2:
                try:
                    self.cur.execute("select c_id from current_acc")
                    ret = self.cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id1) in ret):
                        pass
                    else:
                        print(c_id1 + " does not have a current account.\n")
                        return
                    self.cur.execute("select status from current_acc where c_id=" + c_id1 + "")
                    stu = self.cur.fetchall()
                    stu = list(sum(stu, ()))
                    stu = stu[0]
                    if str(stu) == "CLOSE" or str(stu) == "LOCK":
                        print(c_id1 + " is locked or closed.\n")
                        return
                    if str(c_id)==str(c_id1):
                        print("\nyou can not transfer the amount to same account")
                        return
                    else:
                        self.cur.execute("select balance from current_acc where c_id=" + c_id + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret - amount
                        self.cur.execute("UPDATE current_acc SET balance=:1 where c_id=:2", (str(ret), c_id))
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'transfer',:2,:3,'Current Account')",(c_id, amount, ret))
                        self.conn.commit()
                        self.cur.execute("select balance from current_acc where c_id=" + c_id1 + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret + amount
                        self.cur.execute("UPDATE current_acc SET balance=:1 where c_id=:2", (str(ret), c_id1))
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'deposit',:2,:3,'Current Account')",(c_id1, amount, ret))
                        self.conn.commit()
                        print("Transaction successful.\n")
                except Exception as e:
                    print(e)


class SavingAccount:        #CLASS FOR SAVING ACCOUNT
    def __init__(self):
        self.conn = cx_Oracle.connect('TEST/root@xe')
        print("connected")
        self.cur = self.conn.cursor()

    def open_account(self, c_id):   #FUNCTION TO OPEN NEW SAVING ACCOUNT
        bal = int(input("enter balance you want to enter in your new account: "))
        if bal<0:
            print("Please enter a valid amount.\n")
            return
        else:
            self.cur.execute("insert into SAVING_ACC values(ACCOUNT_NO_VAL1.NEXTVAL,:pram1,'ACTIVE',to_date(sysdate,'DD/MM/YY'),NUll,:pram2,0)",(c_id, bal))
            self.conn.commit()
            print("Saving Account Open Successful.\n")

    def deposit(self, c_id):        #FUNCTION TO DEPOSITE INTO SAVING ACCOUNT
        amount = int(input("enter amount to deposit: "))
        if amount<=0:       #CHECKING FOR VALID AMOUNT TO DEPOSIT
            print("Please enter a valid amount.\n")
            return
        else:
            self.cur.execute("select c_id from saving_acc")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            if (int(c_id) in ret):
                pass
            else:
                print(c_id + " does not have a saving account.\n")
                return
            self.cur.execute("select balance from saving_acc where c_id=" + c_id + "")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            ret = ret[0]
            new_amount = ret + amount
            self.cur.execute("UPDATE saving_acc SET balance=:1 where c_id=:2", (new_amount, c_id))
            # self.conn.commit()
            self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'deposit',:2,:3,'Saving Account')",(c_id, amount, new_amount))
            self.conn.commit()
            print("Amount Deposited Successfully\n")

    def withdraw(self, c_id):       #FUNCTION TO WITHDRAW FROM SAVING ACCOUNT
        self.cur.execute("select c_id from saving_acc")     #CHECKING FOR C_ID WHETHER IT EXISTS OR NOT
        ret = self.cur.fetchall()
        ret = list(sum(ret, ()))
        if (int(c_id) in ret):
            pass
        else:
            print(c_id + " does not have a saving account\n")
            return
        self.cur.execute("select WITHDRAWL from saving_acc where c_id=" + c_id + "")
        ret = self.cur.fetchall()
        ret = list(sum(ret, ()))
        ret = ret[0]
        if ret >= 9:
            print("you have exceeded the per month withdrawl limit.\n")
            return
        amount = int(input("enter amount to withdraw: "))
        if amount<=0:       #CHECKING FOR VALID AMOUNT
            print("Please enter a valid amount.\n")
            return
        else:
            self.cur.execute("select balance from saving_acc where c_id=" + c_id + "")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            ret = ret[0]
            if ret < amount:
                print("your account has " + str(ret) + " amount")
                return
            else:
                ret = ret - amount
                self.cur.execute("UPDATE saving_acc SET balance=:1 where c_id=:2", (str(ret), c_id))
                self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'withdrawl',:2,:3,'Saving Account')",(c_id, amount, ret))
                self.conn.commit()
                self.cur.execute("select WITHDRAWL from saving_acc where c_id=" + c_id + "")
                ret = self.cur.fetchall()
                ret = list(sum(ret, ()))
                ret = ret[0]
                ret = ret + 1
                self.cur.execute("UPDATE saving_acc SET WITHDRAWL=:1 where c_id=:2", (str(ret), c_id))
                self.conn.commit()
                print("Amount Withdrawn Successfully\n")

    def transfer(self, c_id):
        print("enter amount to transfer: ")
        amount = int(input())
        if amount<=0:
            print("Please enter a valid amount.\n")
            return
        else:
            self.cur.execute("select c_id from saving_acc")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            if (int(c_id) in ret):
                pass
            else:
                print(c_id + " does not have a saving account.\n")
                return
            self.cur.execute("select balance from saving_acc where c_id=" + c_id + "")
            ret = self.cur.fetchall()
            ret = list(sum(ret, ()))
            ret = ret[0]
            if ret < amount:
                print("your account has " + str(ret) + " amount")
                return
            print("enter customer ID in which you want to transfer the amount: ")
            c_id1 = input()
            print("1. transfer into saving account\n2. transfer into current account")
            ch = int(input())
            if ch == 1:
                try:
                    self.cur.execute("select c_id from saving_acc")
                    ret = self.cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id1) in ret):
                        pass
                    else:
                        print(c_id1 + " does not have a saving account.\n")
                        return
                    self.cur.execute("select status from saving_acc where c_id=" + c_id1 + "")
                    spr = self.cur.fetchall()
                    spr = list(sum(spr, ()))
                    spr = spr[0]
                    if str(spr) == "LOCK" or str(spr) == "CLOSE":
                        print(c_id1 + " is locked or closed.\n")
                        return
                    if str(c_id)==str(c_id1):
                        print("\n you can not transfer the amount to same account")
                        return
                    else:
                        self.cur.execute("select balance from saving_acc where c_id=" + c_id + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret - amount
                        self.cur.execute("UPDATE saving_acc SET balance=:1 where c_id=:2", (str(ret), c_id))
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'transfer',:2,:3,'Saving Account')",(c_id, amount, ret))
                        self.conn.commit()
                        self.cur.execute("select balance from saving_acc where c_id=" + c_id1 + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret + amount
                        self.cur.execute("UPDATE saving_acc SET balance=:1 where c_id=:2", (str(ret), c_id1))   #UPDATE BALANCE FOR SAVING ACCOUNT
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'deposit',:2,:3,'Saving Account')",(c_id1, amount, ret)) #UPDATE HISTORY TABLE
                        self.conn.commit()
                        print("Transaction successful.\n")
                except Exception as e:
                    print(e)
            elif ch == 2:
                try:
                    self.cur.execute("select c_id from current_acc")
                    ret = self.cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id1) in ret):
                        pass
                    else:
                        print(c_id1 + " does not have a current account\n")
                        return
                    self.cur.execute("select status from current_acc where c_id=" + c_id1 + "")
                    spr = self.cur.fetchall()
                    spr = list(sum(spr, ()))
                    spr = spr[0]
                    if str(spr) == "LOCK" or str(spr) == "CLOSE":
                        print(c_id1 + " is locked or closed.")
                        return
                    else:
                        self.cur.execute("select balance from saving_acc where c_id=" + c_id + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret - amount
                        self.cur.execute("UPDATE saving_acc SET balance=:1 where c_id=:2", (str(ret), c_id))
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'transfer',:2,:3,'Saving Account')",(c_id, amount, ret))
                        self.conn.commit()
                        self.cur.execute("select balance from current_acc where c_id=" + c_id1 + "")
                        ret = self.cur.fetchall()
                        ret = list(sum(ret, ()))
                        ret = ret[0]
                        ret = ret + amount
                        self.cur.execute("UPDATE current_acc SET balance=:1 where c_id=:2", (str(ret), c_id1))
                        self.cur.execute("insert into history values(:1,to_date(sysdate,'DD/MM/YY'),'deposit',:2,:3,'Current Account')",(c_id1, amount, ret))
                        self.conn.commit()
                        print("Transaction successful.\n")
                except Exception as e:
                    print(e)

    def history(self, date1, date2, c_id):      #FUNCTION TO STORE TRANSFER, WITHDROW AND DEPOSIT HISTORY
        self.cur.execute("select * from history where DATE_OF_TRANSACTION between to_date(:1,'DD/MM/YY') and to_date(:2,'DD/MM/YY') and c_id=:3",(date1, date2, c_id))
        ret = self.cur.fetchall()
        ret = list(sum(ret, ()))
        if len(ret) == 0:
            print("No history for this account\n")
            return
        print("Customer ID     date of transaction          action       amount      balance       type of account")
        for i in range(0, len(ret), 6):
            print(str(ret[0 + i]) + "           " + str(ret[1 + i]) + "           " + str(ret[2 + i]) + "       " + str(ret[3 + i]) + "        " + str(ret[4 + i]) + "          " + str(ret[5 + i]))


class FixedDeposit:     #CLASS TO STORE FIXED  DEPOSITE INFORMATION
    def __init__(self):
        self.conn = cx_Oracle.connect('TEST/root@xe')
        print("connected")
        self.cur = self.conn.cursor()

    def open_account(self, c_id):
        while True:
            bal = int(input("Enter balance you want to enter in your new FD account: "))
            if bal < 1000:      #CHECKING WHETHER THE AMOUNT IS CORRECT ACCORDING TO THE CONSTRAINT PROVIDED
                print("Balance of FD can not less than 1000, please retry\n")
                continue
            term = int(input("Enter the term for your fixed deposit in months: "))
            if term < 12:       #CHECKING WHETHER THE TERM IS CORRECT ACCORDING TO THE CONSTRAINT PROVIDED
                print("Term can not be less than 12 months, please retry\n")
                continue
            else:
                break
        self.cur.execute("insert into FIXED_DEPOSITE values(FD_ACCOUNT_NO_VAL.NEXTVAL,:1,to_date(sysdate,'DD/MM/YY'),:2,:3)",(c_id, bal, term))
        self.conn.commit()
        print("FIXED DEPOSITE account created.\n")


class Loan:
    def __init__(self):
        self.conn = cx_Oracle.connect('TEST/root@xe')
        print("connected")
        self.cur = self.conn.cursor()

    def open_account(self, c_id):
        self.cur.execute("select c_id from saving_acc")
        ret = self.cur.fetchall()
        ret = list(sum(ret, ()))
        if (int(c_id) in ret):
            pass
        else:
            print(c_id + " does not have a saving account\n")
            return
        while True:
            amount = int(input("enter loan amount: "))
            if amount<=0:
                print("Please enter a valid amount.\n")
            else:
                if (amount % 1000) != 0:
                    print("please enter the valid amount in multiple of 1000\n")
                    continue
                else:
                    self.cur.execute("select balance from saving_acc where c_id=" + c_id + "")
                    ret = self.cur.fetchall()
                    ret = list(sum(ret, ()))
                    ret = ret[0]
                    if amount > int(2 * int(ret)):
                        print("You can not avail loan greater than twice the amount in your saving account\n")
                        continue
                    else:
                        break
            while True:
                term = int(input("enter term of loan: "))
                if term <= 0:
                    print("term can not be", term)
                    continue
                else:
                    break
            self.cur.execute("insert into LOAN values(LOAN_VAL.NEXTVAL,:1,to_date(sysdate,'DD/MM/YY'),:2,:3)",(c_id, amount, term))
            self.conn.commit()
            print("Loan availed.\n")


conn = cx_Oracle.connect('TEST/root@xe')        #ESTABLISHING CONNECTION WITH DATABASE( DATABASE NAME- TEST, PASSWORD- ROOT )
cur = conn.cursor()     #CREATING AN OBJECT OF CURSOR CLASS TO EXECUTE QUERIES
lock = 0
admin_name = ""
admin_pass = ""
sa1 = ""
sa2 = ""
admin_status = "ACTIVE"
cur.execute("select to_date(sysdate,'DD/MM/YY') from dual")     #CHECKING FOR 1ST DATE OF MONTH TO UPDATE THE WITHDRAWL LIMIT FOR ALL CUSTOMERS
ret = cur.fetchall()
ret = list(sum(ret, ()))
ret = ret[0]
ret = str(ret)
ret = ret.split('-')
day = str(ret[2])
day = int(day[0:2])
if int(day) == 1:       #UPDATING WITHDRWAL LIMIT
    cur.execute("update saving_acc SET WITHDRAWL='0'")
    conn.commit()
while (True):
    print("1. Sign Up\n2. Sign In\n3. Admin Sign In\n4. Quit")      #MAIN MENU
    choice = int(input())
    if choice == 1:
        fname = str(input("enter first name: "))
        if len(fname) == 0:
            print("FName cannot be empty, try again\n")
            continue
        lname = str(input("enter last name: "))
        if len(lname) == 0:
            print("LName cannot be empty, try again\n")
            continue
        mobno = int(input("enter mobile no: (+91)"))
        add1 = input("enter address Line 1: ")
        if len(add1) == 0:
            print("Line 1 address cannot be empty, try again\n")
            continue
        add2 = input("enter address Line 2: ")
        if len(add2) == 0:
            print("Line 2 address cannot be empty, try again\n")
            continue
        city = input("enter city: ")
        if len(city) == 0:
            print("City cannot be empty, try again\n")
            continue
        state = input("enter state: ")
        if len(state) == 0:
            print("State cannot be empty, try again\n")
            continue
        pin = input("enter pin: ")
        gen = input("enter gender: ")
        if len(gen) == 0:
            print("Gender cannot be empty, try again\n")
            continue
        email = input("enter email: ")
        if len(email) == 0:
            print("Email field cannot be empty, try again\n")
            continue
        while True:
            passw = input("enter password: ")
            import re

            pro = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
            if pro.match(passw):
                break
            else:
                print("password must be ALPHA-NUMERIC and 8 CHARACTERS LONG, please  retry")
                continue
        obj = customer()
        obj.new_coustomer(fname, lname, mobno, add1, add2, city, state, pin, gen, email, passw)
    elif choice == 2:

        print("enter your coustomer ID")
        cus_id = str(input())
        if len(cus_id) == 0:
            print("Enter the Customer ID, it cannot be blank.\n")
            continue
        cur.execute("select c_id from customer")
        ret = cur.fetchall()
        ret = list(sum(ret, ()))
        if (int(cus_id) in ret):
            pass
        else:
            print(cus_id + " does not exist\n")
            continue
        try:
            cur.execute("select status from saving_acc where c_id=" + cus_id + "")
            sa1 = cur.fetchall()
            sa1 = list(sum(sa1, ()))
            sa1 = sa1[0]
        except Exception as e:
            pass
        try:
            cur.execute("select status from CURRENT_ACC where c_id=" + cus_id + "")
            sa2 = cur.fetchall()
            sa2 = list(sum(sa1, ()))
            sa2 = sa2[0]
        except Exception as e:
            pass
        if sa1 == "LOCK" or sa2 == "LOCK":      #CHECKING WHETHER THE ACCOUNT IS LOCKED OR NOT
            print("your account has been locked, contact the bank.\n")
            continue
        print("enter your password: ")
        cus_pass = input()
        try:
            cur.execute("select password from customer where C_ID=" + cus_id + "")
            ret = cur.fetchall()
            ret = list(sum(ret, ()))
            lock = 0
            while (True):
                if ret[0] == cus_pass:
                    print("Sign in successful\n")
                    break
                else:
                    if lock == 2:       #CHECK FOR ACCOUNT LOCK CONITION
                        try:
                            cur.execute("UPDATE SAVING_ACC SET status='LOCK' where c_id=" + cus_id + "")        #LOCKING THE ACCOUNT
                            conn.commit()
                            print("Saving Account has been locked.\n")
                        except Exception as e:
                            pass
                        try:
                            cur.execute("UPDATE CURRENT_ACC SET status='LOCK' where c_id=" + cus_id + "")
                            conn.commit()
                            print("Current Account has been locked.\n")
                        except Exception as e:
                            pass
                        finally:
                            exit()
                    print("Wrong password. Please enter passowrd again\n")
                    cus_pass = input()
                    lock += 1
            while True:
                print("1. Address change\n2. Open New Account\n3. Money Deposit\n4. Money Withdrawl\n5. Transfer Money\n6. Print statement\n7. Account closure\n8. Avail Loan\n0. customer logout")
                ins = int(input())
                if ins == 1:
                    add1 = input("enter address Line 1 ")
                    add2 = input("enter address Line 2 ")
                    city = input("enter city ")
                    state = input("enter state ")
                    pin = input("enter pin ")
                    cur.execute("UPDATE customer SET C_ADD_LINE1=:1,C_ADD_LINE2=:2,C_ADD_CITY=:3,C_ADD_STATE=:4,C_ADD_PIN=:5 WHERE C_ID=:6",(add1, add2, city, state, pin, cus_id))
                    conn.commit()
                elif ins == 2:
                    print("1. open Saving Account\n2. open Current Account\n3. open Fixed Deposit Account")
                    ci = int(input())
                    if ci == 1:
                        cur.execute("select c_id from saving_acc")
                        ret = cur.fetchall()
                        ret = list(sum(ret, ()))
                        if (int(cus_id) in ret):
                            print(cus_id + " already have a Saving Account\n")
                            continue
                        else:
                            obj = SavingAccount()
                            obj.open_account(cus_id)
                    elif ci == 2:
                        cur.execute("select c_id from current_acc")
                        ret = cur.fetchall()
                        ret = list(sum(ret, ()))
                        if (int(cus_id) in ret):
                            print(cus_id + " already have a Current Account\n")
                            continue
                        else:
                            obj = CurrentAccount()
                            obj.open_account(cus_id)
                    elif ci == 3:
                        obj = FixedDeposit()
                        obj.open_account(cus_id)
                elif ins == 3:
                    print("1. Saving Account\n2. Current Account")
                    ac = int(input())
                    if ac == 1:
                        if sa1 == "CLOSE":
                            print("your SAVING ACCOUNT has been closed\n")
                            continue
                        obj = SavingAccount()
                        obj.deposit(cus_id)
                    elif ac == 2:
                        if sa2 == "CLOSE":
                            print("your CURRENT ACCOUNT has been closed\n")
                            continue
                        obj = CurrentAccount()
                        obj.deposit(cus_id)
                elif ins == 4:
                    print("1. Saving Account\n2. Current Account")
                    ac = int(input())
                    if ac == 1:
                        if sa1 == "CLOSE":
                            print("your SAVING ACCOUNT has been closed\n")
                            continue
                        obj = SavingAccount()
                        obj.withdraw(cus_id)
                    elif ac == 2:
                        if sa2 == "CLOSE":
                            print("your CURRENT ACCOUNT has been closed\n")
                            continue
                        obj = CurrentAccount()
                        obj.withdraw(cus_id)
                elif ins == 6:
                    date1 = input("first date in dd/mm/yyyy format")
                    date2 = input("second date in dd/mm/yyyy format")
                    obj = SavingAccount()
                    obj.history(date1, date2, cus_id)
                elif ins == 5:
                    print("1. to transfer from Saving Account\n2. to transfer from Current Account") #MENU ASKING WHICH TYPE OF ACCOUNT WE WANT TO TRANSFER FROM
                    ac = int(input())
                    if ac == 1:
                        obj = SavingAccount()
                        obj.transfer(cus_id)
                    elif ac == 2:
                        obj = CurrentAccount()
                        obj.transfer(cus_id)
                elif ins == 7:
                    print("Do you want to close account y/n: ")
                    inp = input()
                    if inp == 'y':
                        print("1. close Saving Account\n2. close Current Account") #menu to close which user account
                        ac = int(input())
                        if ac == 1:
                            cur.execute("select c_id from saving_acc")
                            ret = cur.fetchall()
                            ret = list(sum(ret, ()))
                            if (int(cus_id) in ret):
                                pass
                            else:
                                print(cus_id + " does not have a saving account.\n")
                                continue
                            cur.execute("UPDATE saving_acc SET status='CLOSE' where c_id=" + str(cus_id) + "")
                            conn.commit()
                            cur.execute("UPDATE saving_acc SET END_DATE=to_date(sysdate,'DD/MM/YY') where c_id=" + str(cus_id) + "")
                            conn.commit()
                            cur.execute("select BALANCE from saving_acc where c_id=" + str(cus_id) + "")
                            qw = cur.fetchall()
                            qw = list(sum(qw, ()))
                            qw = qw[0]
                            print("The amount of " + str(qw) + " has been sent to your address. Thanks for banking with us :)\n")
                            print("Account has been closed\n")
                        elif ac == 2:
                            cur.execute("select c_id from current_acc")
                            ret = cur.fetchall()
                            ret = list(sum(ret, ()))
                            if (int(cus_id) in ret):
                                pass
                            else:
                                print(cus_id + " does not have a current account.\n")
                                continue
                            cur.execute("UPDATE CURRENT_ACC SET status='CLOSE' where c_id=" + str(cus_id) + "")
                            conn.commit()
                            cur.execute("UPDATE CURRENT_ACC SET END_DATE=to_date(sysdate,'DD/MM/YY') where c_id=" + str(
                                cus_id) + "")
                            conn.commit()
                            cur.execute("select BALANCE from current_acc where c_id=" + str(cus_id) + "")
                            qw = cur.fetchall()
                            qw = list(sum(qw, ()))
                            qw = qw[0]
                            print("The amount of " + str(qw) + " has been sent to your address. Thanks for banking with us :)")
                            print("Account has closed\n")
                elif ins == 0:
                    print("logout successful.")
                    break
                elif ins == 8:
                    obj = Loan()
                    obj.open_account(cus_id)
        except Exception as e:
            print(e)
    elif choice == 3:
        lock = 0
        cur.execute("select status from admin")
        admin_status = cur.fetchall()
        admin_status = list(sum(admin_status, ()))
        admin_status = admin_status[0]
        if admin_status == "LOCKED":
            print("admin has been locked\n")
            continue
        adm_nam = input("enter name: ")
        adm_pass = input("enter password: ")
        cur.execute("select name from admin")
        admin_name = cur.fetchall()
        admin_name = list(sum(admin_name, ()))
        admin_name = admin_name[0]
        cur.execute("select password from admin")
        admin_pass = cur.fetchall()
        admin_pass = list(sum(admin_pass, ()))
        admin_pass = admin_pass[0]
        while True:
            if adm_nam == str(admin_name) and adm_pass == str(admin_pass):
                print("1. Print closed account history\n2. FD Report of a customer\n3. FD Report of Customer vis-a-vis another customer\n4. FD Report w.r.t a particular FD amount\n5. Loan Report of a Customer\n6. Loan Report of customer vis-a-vis another customer\n7. Loan report w.r.t a particular loan amount\n8. Loan-FD report of customer\n9. Report of customer who are yet to avail a loan\n10. Report of customer who are yet to open an FD account\n11. Report of customer who neither have a loan nor an FD account with the bank\n0. Admin logout ")
                cho = int(input())
                if cho == 1:
                    cur.execute("select c_id from saving_acc where status='CLOSE'")
                    ret1 = ret = cur.fetchall()
                    ret1 = list(sum(ret, ()))
                    print("Customer ID       End Date")
                    for i in ret1:
                        cur.execute("select END_DATE from saving_acc where c_id=" + str(i) + "")
                        ret = cur.fetchall()
                        ret = list(sum(ret, ()))
                        print(str(i) + "              " + str(ret[0]))

                    cur.execute("select c_id from current_acc where status='CLOSE'")
                    ret1 = ret = cur.fetchall()
                    ret1 = list(sum(ret, ()))
                    for i in ret1:
                        cur.execute("select END_DATE from current_acc where c_id=" + str(i) + "")
                        ret = cur.fetchall()
                        ret = list(sum(ret, ()))
                        print(str(i) + "              " + str(ret[0]))      #printing customer id and End date
                elif cho == 2:
                    c_id = input("enter a customer ID ")
                    cur.execute("select c_id from customer")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print(c_id + " does not exist\n")
                        continue
                    cur.execute("select c_id from FIXED_DEPOSITE")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print("N.A")
                        continue
                    cur.execute("select * from FIXED_DEPOSITE where c_id=" + c_id + "")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    print("Account no                customer ID           Start date          balance     term")
                    for i in range(0, len(ret), 5):
                        print(str(ret[0 + i]) + "           " + str(ret[1 + i]) + "           " + str(ret[2 + i]) + "      " + str(ret[3 + i]) + "          " + str(ret[4 + i]))
                elif cho == 3:
                    c_id = input("enter a customer ID: ")
                    cur.execute("select c_id from customer")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print(c_id + " does not exist")
                        continue
                    cur.execute("select c_id from FIXED_DEPOSITE")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print("N.A")
                        continue
                    cur.execute("select balance from FIXED_DEPOSITE where c_id=" + c_id + "")
                    ret1 = cur.fetchall()
                    ret1 = list(sum(ret1, ()))
                    ret1 = sum(ret1)
                    cur.execute("select c_id from FIXED_DEPOSITE where balance>=" + str(ret1) + "")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if len(ret) == 0:
                        print("N.A no account has balance greater than: ", ret1)
                        continue
                    print("Account No          customer ID        balance         term")
                    a = list()
                    for i in ret:
                        if i not in a:
                            a.append(i)
                            cur.execute("select FD_ACCOUNT_NO,C_ID,BALANCE,TERM from FIXED_DEPOSITE where c_id=" + str(i) + "")
                            ret2 = cur.fetchall()
                            ret2 = list(sum(ret2, ()))
                            for j in range(0, len(ret2), 4):
                                print(str(ret2[0]) + "        " + str(ret2[1]) + "            " + str(ret2[2]) + "        " + str(ret2[3]))
                elif cho == 4:
                    while True:
                        amount = int(input("enter a amount: "))
                        if amount < 0:
                            print("invalid amount retry.\n")
                            continue
                        elif int(amount % 1000) != 0:
                            print("enter amount in multiple of 1000, retry\n")
                            continue
                        else:
                            break

                    cur.execute("select c_id from FIXED_DEPOSITE where balance>=" + str(amount) + "")
                    ret2 = cur.fetchall()
                    ret2 = list(sum(ret2, ()))
                    if len(ret2) == 0:
                        print("N.A.\n")
                        continue
                    print("customer ID       first name         last name        FD Amount")
                    a = list()
                    for i in ret2:
                        if i not in a:
                            a.append(i)
                            cur.execute("select C.c_id, C.C_FNAME, C.C_LNAME, B.BALANCE from customer C,FIXED_DEPOSITE B where C.c_id=B.c_id and C.c_id=" + str(i) + "")
                            ret1 = cur.fetchall()
                            ret1 = list(sum(ret1, ()))
                            for j in range(0, len(ret1), 4):
                                if int(ret1[3 + j])>int(amount):
                                    print(str(ret1[0 + j]) + "              " + str(ret1[1 + j]) + "             " + str(ret1[2 + j]) + "           " + str(ret1[3 + j]))
                elif cho == 5:
                    c_id = input("enter a customer ID: ")
                    cur.execute("select c_id from customer")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print(c_id + " does not exist")
                        continue
                    cur.execute("select c_id from loan")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print("Not Availed\n")
                        continue
                    cur.execute("select * from loan where c_id=" + c_id + "")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    print("Account no                Customer ID           Start date          Loan Amount     Term")
                    for i in range(0, len(ret), 5):
                        print(str(ret[0 + i]) + "           " + str(ret[1 + i]) + "           " + str(ret[2 + i]) + "      " + str(ret[3 + i]) + "             " + str(ret[4 + i]))
                elif cho == 6:
                    c_id = input("enter a customer ID: ")
                    cur.execute("select c_id from customer")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print(c_id + " does not exist.\n")
                        continue
                    cur.execute("select c_id from loan")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if (int(c_id) in ret):
                        pass
                    else:
                        print("N.A, account doesn't have loan\n")
                        continue
                    cur.execute("select LOAN_AMOUNT from loan where c_id=" + c_id + "")
                    ret1 = cur.fetchall()
                    ret1 = list(sum(ret1, ()))
                    ret1 = sum(ret1)
                    cur.execute("select c_id from loan where LOAN_AMOUNT>=" + str(ret1) + "")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    if len(ret) == 0:
                        print("N.A no account has balance greater than", ret1)
                        continue
                    print("Account No          customer ID        balance         term")
                    a = list()
                    for i in ret:
                        if i not in a:
                            a.append(i)
                            cur.execute("select L_ACCOUNT_NO,C_ID,LOAN_AMOUNT,TERM from loan where c_id=" + str(i) + "")
                            ret2 = cur.fetchall()
                            ret2 = list(sum(ret2, ()))
                            for j in range(0, len(ret2), 4):
                                print(str(ret2[0 + j]) + "        " + str(ret2[1 + j]) + "            " + str(
                                    ret2[2 + j]) + "        " + str(ret2[3 + j]))
                elif cho == 7:
                    while True:
                        amount = int(input("enter an amount: "))
                        if amount < 0:      #CHECKING FOR VALID AMOUNT
                            print("invalid amount retry\n")
                            continue
                        elif int(amount % 1000) != 0:
                            print("enter amount in multiple of 1000, retry\n")
                            continue
                        else:
                            break

                    cur.execute("select c_id from loan where LOAN_AMOUNT>=" + str(amount) + "")
                    ret2 = cur.fetchall()
                    ret2 = list(sum(ret2, ()))
                    if len(ret2) == 0:
                        print("N.A, so such accounts.\n")
                        continue
                    print("customer ID       first name         last name        Loan Amount")
                    a = list()
                    for i in ret2:
                        if i not in a:
                            a.append(i)
                            cur.execute("select C.c_id, C.C_FNAME, C.C_LNAME, B.LOAN_AMOUNT from customer C,loan B where C.c_id=B.c_id and B.c_id=" + str(i) + "")
                            ret1 = cur.fetchall()
                            ret1 = list(sum(ret1, ()))
                            for j in range(0, len(ret1), 4):
                                if int(ret1[3 + j])>int(amount):
                                    print(str(ret1[0 + j]) + "              " + str(ret1[1 + j]) + "             " + str(ret1[2 + j]) + "           " + str(ret1[3 + j]))
                elif cho == 8:
                    cur.execute("select c_id from loan")
                    retl = cur.fetchall()
                    retl = list(sum(retl, ()))
                    if len(retl) == 0:
                        print("no accounts in loan.\n")
                        continue
                    cur.execute("select c_id from FIXED_DEPOSITE")
                    retf = cur.fetchall()
                    retf = list(sum(retf, ()))
                    if len(retf) == 0:
                        print("no accounts in FIXED_DEPOSITE.\n")
                        continue
                    cl = list()
                    if len(retl) < len(retf):
                        l = retl
                        s = retf
                    else:
                        l = retf
                        s = retl
                    for i in l:
                        if i in s and i not in cl:
                            cl.append(i)
                    if len(cl) == 0:
                        print("no customer has both loan and FD account.\n")
                        continue
                    print("customer ID        first name      last name      sum of loan amount       sum of FD account")
                    ft=0
                    for i in cl:
                        cur.execute("select LOAN_AMOUNT from loan where c_id=" + str(i) + "")
                        ret1 = cur.fetchall()
                        ret1 = list(sum(ret1, ()))
                        ret1 = sum(ret1)
                        cur.execute("select balance from FIXED_DEPOSITE where c_id=" + str(i) + "")
                        ret2 = cur.fetchall()
                        ret2 = list(sum(ret2, ()))
                        ret2 = sum(ret2)
                        if ret1 > ret2:
                            ft=1
                            cur.execute("select c_id,C_FNAME,C_LNAME from customer where c_id=" + str(i) + "")
                            ret3 = cur.fetchall()
                            ret3 = list(sum(ret3, ()))
                            print(str(ret3[0]) + "                 " + str(ret3[1]) + "        " + str(ret3[2]) + "              " + str(ret1) + "                  " + str(ret2))
                    if ft==0:       #CHECKING IF THERE IS NO SUM OF LOAN GREATER THAN SUM OF FIXED DEPOSIT
                        print("\n")
                        print("No person has sum of loan greater than sum of fixed deposit amount\n")
                elif cho == 9:
                    cur.execute("select c_id from customer")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    cur.execute("select c_id from loan")
                    retl = cur.fetchall()
                    retl = list(sum(retl, ()))
                    ul = list()
                    for i in retl:
                        if i not in ul:
                            ul.append(i)
                    LA = list()
                    ret = set(ret)
                    ul = set(ul)
                    LA = ret - ul
                    if len(LA) == 0:
                        print("all customers have availed loan\n")
                        continue
                    print("customer ID         First name         Last name")
                    for i in LA:
                        cur.execute("select c_id,C_FNAME,C_LNAME from customer where c_id=" + str(i) + "")
                        ret3 = cur.fetchall()
                        ret3 = list(sum(ret3, ()))
                        print(str(ret3[0]) + "               " + str(ret3[1]) + "             " + str(ret3[2]))
                elif cho == 10:
                    cur.execute("select c_id from customer")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    cur.execute("select c_id from FIXED_DEPOSITE")
                    retl = cur.fetchall()
                    retl = list(sum(retl, ()))
                    ul = list()
                    for i in retl:
                        if i not in ul:
                            ul.append(i)
                    LA = list()
                    ret = set(ret)
                    ul = set(ul)
                    LA = ret - ul
                    if len(LA) == 0:
                        print("all customers have FIXED DEPOSITE Account\n")
                        continue
                    print("customer ID         First name         Last name")
                    for i in LA:
                        cur.execute("select c_id,C_FNAME,C_LNAME from customer where c_id=" + str(i) + "")
                        ret3 = cur.fetchall()
                        ret3 = list(sum(ret3, ()))
                        print(str(ret3[0]) + "               " + str(ret3[1]) + "             " + str(ret3[2]))
                elif cho == 11:
                    cur.execute("select c_id from customer")
                    ret = cur.fetchall()
                    ret = list(sum(ret, ()))
                    cur.execute("select c_id from FIXED_DEPOSITE")
                    ret1 = cur.fetchall()
                    ret1 = list(sum(ret1, ()))
                    cur.execute("select c_id from loan")
                    ret2 = cur.fetchall()
                    ret2 = list(sum(ret2, ()))
                    for i in ret1:
                        if i not in ret2:
                            ret2.append(i)
                    ul = list()
                    for i in ret2:
                        if i not in ul:
                            ul.append(i)
                    na = list()
                    ul = set(ul)
                    ret = set(ret)
                    na = ret - ul
                    if len(na) == 0:
                        print("all customers have FIXED DEPOSITE or loan Account\n")
                        continue
                    print("customer ID         First name         Last name")
                    for i in na:
                        cur.execute("select c_id,C_FNAME,C_LNAME from customer where c_id=" + str(i) + "")
                        ret3 = cur.fetchall()
                        ret3 = list(sum(ret3, ()))
                        print(str(ret3[0]) + "               " + str(ret3[1]) + "             " + str(ret3[2]))

                elif cho == 0:
                    print("Logout successful\n")
                    break
            else:
                if lock == 2:
                    cur.execute("update admin set status='LOCKED'")
                    print("Admin has been locked\n")
                    break
                print("wrong password or user name retry\n")
                adm_nam = input("enter name: ")
                adm_pass = input("enter password: ")
                lock += 1
    elif choice == 4:
        try:
            conn.close()        #CLOSE THE CONNECTION TO THE DATABASE
        except Exception as e:
            pass
        finally:
            print("Have a nice day... Hope to see you soon :)")     #ENDING QUOTE :)
            exit()      #EXITING FROM THE APPLICATION
