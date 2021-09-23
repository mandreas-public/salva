from sqlalchemy import create_engine  
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
import config as cnf
import secret as sct
from lib.models import Account, Owner, Transaction
import datetime

class objTransaction():
    def __init__(self, session):

        self.session = session

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
    
    def del_trans(self):
        while True:
            try:
                transaction = int(input('Enter transaction ID to delete: '))
                break
            except ValueError:
                print('Invalid entry.')
        
        transaction_exists = self.session.query(Transaction.id).filter_by(id=transaction).first() is not None
        
        if transaction_exists:         
            t = self.session.query(Transaction).filter(Transaction.id == transaction).one()
            self.session.delete(t)
            print(f'\"{transaction}\" has been deleted')
        else:
            print('\nThat transaction ID does not exist.')
    
