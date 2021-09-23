from sqlalchemy import create_engine  
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
import config as cnf
import secret as sct
from lib.models import Account, Owner, Transaction
import datetime

class objAccount():
    def __init__(self, session):
        
        self.session = session

    def add_account(self):
        while True:
            try:
                account_name = str(input('Account unique name: '))
                account_type = str(input('Account type [tfsa, rrsp, hisa or non-reg]: '))
                account_inst = str(input('Account institution name: '))
                account_sbal = float(input('Account starting balance: '))
                account_owner = str(input('Account owner name: '))
                break
            except ValueError:
                print('Invalid entry.')

        account_exists = self.session.query(Account.account_name).filter_by(account_name=account_name).first() is not None
        owner_exists = self.session.query(Owner.owner_name).filter_by(owner_name=account_owner).first() is not None

        if not account_exists and owner_exists:
            o = self.session.query(Owner).filter_by(owner_name=account_owner).first()

            account = Account(
                account_name = account_name, 
                account_type = account_type,
                account_inst = account_inst,
                account_sbal = account_sbal,
                owner_id = o.id
                )
            self.session.add(account)
            self.session.commit()
            print('New Account added.\n')
        elif account_exists and owner_exists:
            print('\nThat account already exists.')
            y_n = str(input('Would you like to update account data [y/n]? '))
            if y_n == 'y':
                a = self.session.query(Account).filter(Account.account_name == account_name).one()
                o = self.session.query(Owner).filter_by(owner_name=account_owner).first()

                a.account_name = account_name
                a.account_type = account_type
                a.account_inst = account_inst
                a.account_sbal = account_sbal
                a.owner_id = o.id
                
                self.session.commit()
                print('Account data updated.\n')
            else:
                print('\nOperation cancelled.')
        else:
            print('\nThat owner does not exist.  Add owner first.')
    
    def add_owner(self):
        while True:
            try:
                owner_name = str(input('Account owner name: '))
                owner_salary = float(input('Owner salary: '))
                owner_otherincome = float(input('Owner other income: '))
                owner_tfsa_room = float(input('Owner current TFSA room: '))
                owner_rrsp_room = float(input('Owner current RRSP room: '))       
                break
            except ValueError:
                print('Invalid entry.')

        owner_exists = self.session.query(Owner.owner_name).filter_by(owner_name=owner_name).first() is not None

        if not owner_exists:
            owner = Owner(
                owner_name = owner_name, 
                owner_salary = owner_salary,
                owner_otherincome = owner_otherincome,
                owner_tfsa_room = owner_tfsa_room,
                owner_rrsp_room = owner_rrsp_room,
                )
            self.session.add(owner)
            self.session.commit()
            print('New Account Owner added.\n')
        else:
            print('\nThat owner already exists.')
            y_n = str(input('Would you like to update owner data [y/n]? '))
            if y_n == 'y':
                o = self.session.query(Owner).filter(Owner.owner_name == owner_name).one()

                o.owner_name = owner_name
                o.owner_salary = owner_salary
                o.owner_otherincome = owner_otherincome
                o.owner_tfsa_room = owner_tfsa_room
                o.owner_rrsp_room = owner_rrsp_room
                
                self.session.commit()
                print('Account Owner data updated.')
            else:
                print('\nOperation cancelled.')

    def deposit(self):      
        while True:
            try:
                trans_amount = float(input('Enter amount deposited: '))
                d = input('Enter date of transaction [YYYY-MM-DD]: ')
                trans_date = datetime.datetime.strptime(d, "%Y-%m-%d")
                trans_account = str(input('Enter account name: '))
                break
            except ValueError:
                print('Invalid entry.')
        
        account_exists = self.session.query(Account.account_name).filter_by(account_name=trans_account).first() is not None
        a = self.session.query(Account).filter(Account.account_name == trans_account).one()
        
        if account_exists:         
            transaction = Transaction(
                trans_date = trans_date,
                trans_amount = trans_amount,
                account_id = a.id  
            )

            self.session.add(transaction)
            self.session.commit()
            print('New Transaction added.\n')
        else:
            print('\nThat Account does not exist.')
        
        sbal = a.account_sbal
        ts = self.session.query(func.sum(Transaction.trans_amount)).filter(Transaction.account_id == a.id).one()
        acc_bal = sbal + ts[0]
        
        print(f'Current account balance in \"{trans_account}\" is {acc_bal}')

    def withdraw(self):
        while True:
            try:
                trans_amount = float(input('Enter amount withdrawn: '))
                d = input('Enter date of transaction [YYYY-MM-DD]: ')
                trans_date = datetime.datetime.strptime(d, "%Y-%m-%d")
                trans_account = str(input('Enter account name: '))
                break
            except ValueError:
                print('Invalid entry.')
        
        account_exists = self.session.query(Account.account_name).filter_by(account_name=trans_account).first() is not None
        a = self.session.query(Account).filter(Account.account_name == trans_account).one()
        
        if account_exists:         
            transaction = Transaction(
                trans_date = trans_date,
                trans_amount = trans_amount * -1,
                account_id = a.id  
            )

            self.session.add(transaction)
            self.session.commit()
            print('New Transaction added.')
        else:
            print('\nThat Account does not exist.')
        
        sbal = a.account_sbal
        ts = self.session.query(func.sum(Transaction.trans_amount)).filter(Transaction.account_id == a.id).one()
        acc_bal = sbal + ts[0]
        
        print(f'Current account balance in \"{trans_account}\" is {acc_bal}')

    def annual_cont(self):
        ''

    def total_cont(self):
        ''

    def get_balance(self):
        while True:
            try:
                account = str(input('Enter account to query: '))
                #d = input('Enter start date of transaction [YYYY-MM-DD]: ')
                #trans_date = datetime.datetime.strptime(d, "%Y-%m-%d")
                break
            except ValueError:
                print('Invalid entry.')
        
        account_exists = self.session.query(Account.account_name).filter_by(account_name=account).first() is not None
        a = self.session.query(Account).filter(Account.account_name == account).one()
        
        if account_exists:         
            sbal = a.account_sbal
            ts = self.session.query(func.sum(Transaction.trans_amount)).filter(Transaction.account_id == a.id).one()
            acc_bal = sbal + ts[0]
            print(f'The account balance of \"{account}\" is {acc_bal}')
        else:
            print('\nThat Account does not exist.')

    def get_accounts(self):
        while True:
            try:
                owner = str(input('Enter account owner to query accounts for: '))
                #d = input('Enter start date of transaction [YYYY-MM-DD]: ')
                #trans_date = datetime.datetime.strptime(d, "%Y-%m-%d")
                break
            except ValueError:
                print('Invalid entry.')
        
        owner_exists = self.session.query(Owner.owner_name).filter_by(owner_name=owner).first() is not None
        o = self.session.query(Owner).filter(Owner.owner_name == owner).one()
        
        if owner_exists:         
            accounts = self.session.query(Account).filter(Account.owner_id == o.id).all()
            
            print(f'\"{owner}\" has the following accounts:')
            for account in accounts:
                print (f'Name: {account.account_name}; Type: {account.account_type}; Institution: {account.account_inst}.')
        else:
            print('\nThat Account does not exist.')

    def get_transactions(self):
        while True:
            try:
                account = str(input('Enter account to query transactions for: '))
                break
            except ValueError:
                print('Invalid entry.')
        
        account_exists = self.session.query(Account.account_name).filter_by(account_name=account).first() is not None
        o = self.session.query(Account).filter(Account.account_name == account).one()
        
        if account_exists:         
            transactions = self.session.query(Transaction).filter(Transaction.account_id == o.id).all()
            
            print(f'\"{account}\" has the following transactions:')
            for transaction in transactions:
                print (f'ID: {transaction.id}; Date: {transaction.trans_date}; Amount: {transaction.trans_amount}.')
        else:
            print('\nThat Account does not exist.')

    def get_owners(self):             
        owners = self.session.query(Owner).all()
        print('The following Owners exist:')
        for owner in owners:
            print (f'Name: {owner.owner_name}; Salary: {owner.owner_salary}; Other Income: {owner.owner_otherincome}; TFSA Room: {owner.owner_tfsa_room}; RRSP Room: {owner.owner_rrsp_room};')  
    
    def del_owner(self):
        while True:
            try:
                owner = str(input('Enter owner to delete: '))
                break
            except ValueError:
                print('Invalid entry.')
        
        owner_exists = self.session.query(Owner.owner_name).filter_by(owner_name=owner).first() is not None
        
        if owner_exists:         
            o = self.session.query(Owner).filter(Owner.owner_name == owner).one()
            self.session.delete(o)
            print(f'\"{owner}\" has been deleted')
        else:
            print('\nThat Owner does not exist.')
    
    def del_account(self):
        while True:
            try:
                account = str(input('Enter account to delete: '))
                break
            except ValueError:
                print('Invalid entry.')
        
        account_exists = self.session.query(Account.account_name).filter_by(account_name=account).first() is not None
        
        if account_exists:         
            a = self.session.query(Account).filter(Account.account_name == account).one()
            self.session.delete(a)
            print(f'\"{account}\" has been deleted')
        else:
            print('\nThat Owner does not exist.')
    
    def del_trans(self):
        while True:
            try:
                owner = str(input('Enter owner to delete: '))
                #d = input('Enter start date of transaction [YYYY-MM-DD]: ')
                #trans_date = datetime.datetime.strptime(d, "%Y-%m-%d")
                break
            except ValueError:
                print('Invalid entry.')
        
        owner_exists = self.session.query(Owner.owner_name).filter_by(owner_name=owner).first() is not None
        
        if owner_exists:         
            o = self.session.query(Owner).filter(Owner.owner_name == owner).one()
            self.session.delete(o)
            print(f'\"{owner}\" has been deleted')
        else:
            print('\nThat Owner does not exist.')
    
    def close_session(self):
        self.session.commit()
        self.session.close()
