from os import path
import secret as sct
import config as cnf
from lib.account import objAccount
from lib.owner import objOwner
from lib.transaction import objTransaction
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker
from lib.models import Account, Owner, Transaction

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "lib", "models.py"))
exec(open(filepath).read())

db_uri = 'postgresql+psycopg2://'+sct.username+':'+sct.password+'@'+cnf.db_server+'/'+cnf.db_name
db = create_engine(db_uri)
Session = sessionmaker()
Session.configure(bind=db)

session = Session()

a = objAccount(session)
o = objOwner(session)
t = objTransaction(session)

def mainLoop():
    while True:
        option = input("""
         Salva
                                                  
         1. Add an Owner                      
         2. Add an Account                   
         3. Add a Deposit
         4. Add a Withdrawl
         5. List Owners
         6. List Owner Accounts
         7. List Account Balance
         8. List Account Transactions
         9. Delete an Owner
         10. Delete an Account
         11. Delete a Transaction
         "end": Exit                                                                      
        
             Option: """)                             

        if option == '1':
            o.add_owner()

        elif option == '2':
            a.add_account()

        elif option == '3':
            t.deposit()

        elif option == '4':
            t.withdraw()

        elif option == '5':
            a.get_owners()

        elif option == '6':
            a.get_accounts()

        elif option == '7':
            a.get_balance()

        elif option == '8':
            t.get_transactions()

        elif option == '9':
            o.del_owner()

        elif option == '10':
            a.del_account()

        elif option == '11':
            t.del_trans()        

        elif option == 'end':
            session.commit()
            session.close()
            exit()        
        else:
            print('\nThis is not an option!')

if __name__ == '__main__':
    mainLoop()




