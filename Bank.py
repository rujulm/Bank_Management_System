import mysql.connector
import tabulate

def create_account():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        print("\nTo create an account, please enter the following details")
        c_name=input("Enter name: ")
        c_age=int(input("Enter age: "))
        if c_age<18:
            print("\n\033[1;31mSorry! you are not eligible to open an account")
        else:
            c_address=input("\033[0;30mEnter address: ")
            c_salary=int(input("Enter salary: "))
            c_amount=int(input("Enter initial amount: "))
            if c_amount<3000:
                print("\n\033[1;31mMinimum deposit required is 3000")
                c_amount=int(input("\033[0;30mEnter initial amount: "))
            c_passwd=input("Create account password: ")
            c_username=input("Create account username: ")
            mycur.execute(f"insert into customer (Name,Age,Address,Salary,Balance,Password,Username) values ('{c_name}',{c_age},'{c_address}',{c_salary},{c_amount},'{c_passwd}','{c_username}')")
            mycon.commit()
            print("\nAccount has been created !")
            mycur.execute(f"select AccountNumber from customer where Name='{c_name}' and Age={c_age} and Address='{c_address}' and Salary={c_salary}")
            for i in mycur.fetchone():
                print("\n\033[1;36mYour account number is",i)
                mycur.execute(f"insert into loan (AccountNumber) values ({i})")
                mycon.commit()
            print("\n\033[0;30mTo operate your account choose option 1")
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()


def close_account(accno):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\033[1;31mInvalid account number")
        else:
            mycur.execute(f"select LoanAmount from Loan where AccountNumber={accno}")
            for i in mycur.fetchone():
                if i==0:
                    mycur.execute(f"delete from customer where AccountNumber={accno}")
                    mycon.commit()
                    print("\n\033[1;32mAccount has been deleted successfully")
                else:
                    print("\n\033[1;31mLoan pending....Account cannot be closed")
    
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()          


def deposit(accno):
    try:
        import datetime
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\033[1;31mInvalid account number")
        else:
            c_credit=int(input("\033[0;30mEnter amount to be deposited: "))
            mycur.execute(f"update customer set Balance=balance+{c_credit} where AccountNumber={accno}")
            mycon.commit()
            mycur.execute(f"select balance from customer where AccountNumber={accno}")
     
            for i in mycur.fetchone():
                balance2=i
            print("\n\033[1;32mTransaction successful!")
            print("\033[0;30mYour current balance is",balance2)
            mycur.execute(f"insert into Transactions (AccountNumber, Activity,Amount,TransactionDate) values ({accno},'credit',{c_credit},'{datetime.date.today()}')")
            mycon.commit()
        
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()
  
    
def withdraw(accno):
    try:
        import datetime
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\n\033[1;31mInvalid account number")
        else:
            c_debit=int(input("\033[0;30mEnter amount to be withdrawn: "))
            mycur.execute(f"select balance from customer where AccountNumber={accno}")
        
            for i in mycur.fetchone():
                balance1=i
            if balance1>=c_debit:
                mycur.execute(f"update customer set Balance=balance-{c_debit} where AccountNumber={accno}")
                mycon.commit()
                mycur.execute(f"select balance from customer where AccountNumber={accno}")
        
                for i in mycur.fetchone():
                    balance2=i
                print("\n\033[1;32mTransaction successful!")
                print("\033[0;30mYour current balance is",balance2)
                mycur.execute(f"insert into Transactions (AccountNumber, Activity,Amount,TransactionDate) values ({accno},'debit',{c_debit},'{datetime.date.today()}')")
                mycon.commit()
            else:
                print("\033[1;31mTransaction failed! Account balance is not sufficient")
        
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()


def account_statement(accno):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\n\033[1;31mInvalid account number")
        else:
            c_month=input("\n\033[0;30mEnter month: ")
            mycur.execute(f"select Activity,Amount,TransactionDate from Transactions where monthname(TransactionDate)='{c_month}' and AccountNumber={accno}")
            rs=mycur.fetchall()
            print('\n\033[0;36m'+20*'*','ACCOUNT STATEMENT',20*'*')
            print(tabulate.tabulate(rs,headers=['Account Activity','Amount','Transaction Date'],showindex='always',tablefmt='fancy_grid'))
    
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()
                   

def loan(accno):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        rec=mycur.fetchone()
        if rec==None:
            print("\n\033[1;30mInvalid account number")
        else:
            mycur.execute(f"select Salary from customer where AccountNumber={accno}")
            rs=mycur.fetchone()
            for i in rs:
                if i<15000:
                    print("\n\033[1;31mSorry, you are not eligible to apply for a loan.")
                else:
                    rec=(['Student','05 years','4%'],['Student','10 years','6%'],['Auto','05 years','6%'],['Auto','08 years','9%'],['Mortgage','10 years','2%'],['Mortgage','25 years','5%'],['Personal','03 years','4%'],['Personal','05 years','7%'])
                    print(tabulate.tabulate(rec,headers=['Loan Type','Duration','Interest Rate'],tablefmt='fancy_grid'))
                    print("\n\033[0;30mChoose type of loan:")
                    print("1. Student Loan")
                    print("2. Auto Loan")
                    print("3. Mortgage Loan")
                    print("4. Personal Loan")
                    ch=int(input("\nEnter choice: "))
                    p=int(input("Enter loan amount: "))
                    if p<=6*i:
                        t=float(input("Enter duration of loan: "))
                        m=t*12
                
                        if ch==1 and t==5:
                            r=0.04/12
                            type='student'
                        elif ch==1 and t==10:
                            r=0.06/12
                            type='student'
                        elif ch==2 and t==5:
                            r=0.06/12
                            type='auto'
                        elif ch==2 and t==8:
                            r=0.09/12
                            type='auto'
                        elif ch==3 and t==10:
                            r=0.02/12
                            type='mortgage'
                        elif ch==3 and t==25:
                            r=0.05/12
                            type='mortgage'
                        elif ch==4 and t==3:
                            r=0.04/12
                            type='personal'
                        elif ch==4 and t==5:
                            r=0.07/12
                            type='personal'
                        else:
                            print("\n\033[1;31mInvalid value entered")
                        x=(1+r)**m
                        y=(1+r)**m-1
                        c_EMI=p*r*x//y
                        rate=r*1200
                        mycur.execute(f"update loan set LoanType='{type}',LoanAmount={p},Interest={rate},Duration={t},EMI={c_EMI},PendingEMIs={m} where AccountNumber={accno}")
                        mycon.commit()
                        print("\n\033[1;32mLoan has been granted")
                        print("\033[0;30mThe EMI to be paid is",c_EMI)
                    else:
                        print("\n\033[1;31mLoan request denied")
        
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()               


def pay_emi(accno):
    import datetime
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor(buffered=True)
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\n\033[1;31mInvalid account number")
        
        else:
            mycur.execute(f"select LoanAmount,EMI,PendingEMIs from loan where AccountNumber={accno}")
            r=mycur.fetchone()
            loan=r[0]
            EMI=r[1]
            num=r[2]
            if loan==0:
                print("\n\033[1;31mNo loan borrowed!")
            else:
                t=datetime.date.today()
                mycur.execute(f"select transactiondate from transactions where Accountnumber={accno} and activity='EMI' and month(transactiondate)={t.month} and year(transactiondate)={t.year}")
                d=mycur.fetchone()
                if d==None:
                    mycur.execute(f"select balance from customer where AccountNumber={accno}")
                    for j in mycur.fetchone():
                        balance=j
            
                    v1=balance-EMI
                    if v1>=0:
                        mycur.execute(f"update customer set balance={v1} where AccountNumber={accno}")
                        mycon.commit()
                
                        v2=num-1
                        mycur.execute(f"update loan set PendingEMIs={v2} where AccountNumber={accno}")
                        mycon.commit()
            
                        print("\n\033[1;32mTransaction succesful!")
                        print("\033[0;30mYour available balance is",v1)
                        mycur.execute(f"insert into Transactions (AccountNumber, Activity,Amount,TransactionDate) values ({accno},'EMI',{EMI},'{datetime.date.today()}')")
                        mycon.commit()
                        if v2==0:
                            print("\n\033[1;32mLoan has been cleared")
                    else:
                        print("\n\033[1;31mAccount balance is not sufficient to pay EMI")
                else:
                    print("\n\033[1;32mEMI for this month has been paid!")
            
    except Exception as e:
         print(e)
        
    mycur.close()
    mycon.close() 


def view_details(accno):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\n\033[1;31mInvalid account number")
        else:
            mycur.execute(f"select Name,Age,Address,Salary,Balance,LoanAmount,LoanType,Interest,Duration,EMI,PendingEMIs from customer c, loan l where c.AccountNumber={accno} and  c.AccountNumber=l.AccountNumber")
            r=mycur.fetchall()
            print(tabulate.tabulate(r,headers=['Name','Age','Address','Salary','Balance','Loan Amount','Loan Type','Interest','Duration','EMI','Pending EMIs'],tablefmt='fancy_grid'))

    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()
    
    
def edit_details(accno):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select * from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\n\033[1;31mInvalid account number")
        else:
            print("\n\033[0;30mPlease choose the information to be edited:")
            print("1. Address")
            print("2. Salary")
            print("3. Account password")
            print("4. Account username")
            ch=int(input("Enter option number: "))
            if ch==1:
                c_address=input("Address: ")
                mycur.execute(f"update customer set Address='{c_address}' where AccountNumber={accno}")
                mycon.commit()
                print("\n\033[1;32mDetails have been updated")
            elif ch==2:
                c_salary=int(input("Salary: "))
                mycur.execute(f"update customer set Salary={c_salary} where AccountNumber={accno}")
                mycon.commit()
                print("\n\033[1;32mDetails have been updated")
            elif ch==3:
                c_passwd=input("Account password: ")
                mycur.execute(f"update customer set password='{c_passwd}' where AccountNumber={accno}")
                mycon.commit()
                print("\n\033[1;32mDetails have been updated")
            elif ch==4:
                c_username=input("Account username: ")
                mycur.execute(f"update customer set username='{c_username}' where AccountNumber={accno}")
                mycon.commit()
                print("\n\033[1;32mDetails have been updated")
            else:
                print("Invalid option number")
    
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()
            
               
while True:
    txt="\033[1;96mWELCOME TO ABU DHABI CITY BANK!"
    s='_'
    print("\n\033[1;96m",s*15,txt,s*15)
    print("\n\033[1;90m1. Existing customer")
    print("2. New customer")
    print("3. Exit")
    op1=int(input("\n\033[0;30mEnter option number: "))
    if op1==1:
        accno=int(input("Enter account number: "))
        user=input("Enter username: ")
        pw=input("Enter password: ")
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='rujul8',database='bank')
        mycur=mycon.cursor()
        mycur.execute(f"select password,username from customer where AccountNumber={accno}")
        r=mycur.fetchone()
        if r==None:
            print("\n\033[1;31mAccount does not exist")
        elif user==r[1] and pw==r[0]:
            print("\n\033[1;32m Login successful!")
            while True:
                print("\n\033[1;30m 1. View details")
                print(" 2. Edit details")
                print(" 3. Deposit money")
                print(" 4. Withdraw money")
                print(" 5. Apply for a loan")
                print(" 6. Pay EMI")
                print(" 7. View account statement")
                print(" 8. Close account")
                print(" 9. Exit\n")
                op2=int(input("\n\033[0;30mEnter option number: "))
                if op2==1:
                    view_details(accno)
                elif op2==2:
                    edit_details(accno)
                elif op2==3:
                    deposit(accno)
                elif op2==4:
                    withdraw(accno)
                elif op2==5:
                    loan(accno)
                elif op2==6:
                    pay_emi(accno)
                elif op2==7:
                    account_statement(accno)
                elif op2==8:
                    close_account(accno)
                elif op2==9:
                    print("\n\033[1;36mThank you for choosing Abu Dhabi City Bank!")
                    break
                else:
                    print("Invalid option number")
        else:
            print("\n\033[1;31mIncorrect username or password")
            continue
    elif op1==2:
        create_account()
    elif op1==3:
        print("\n\033[1;36mThank you for choosing Abu Dhabi City Bank!")
        break
    else:
        print("Invalid option number")
        
    
