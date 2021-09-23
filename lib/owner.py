from sqlalchemy import create_engine  
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from lib.models import Account, Owner, Transaction
import datetime
import pandas as pd

class objOwner():
    def __init__(self, session):

        self.session = session
   
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


    def annual_cont(self):
        ''

    def total_cont(self):
        ''


    def get_accounts(self, owner):
        while True:
            try:
                owner = owner #str(input('Enter account owner to query accounts for: '))
                #d = input('Enter start date of transaction [YYYY-MM-DD]: ')
                #trans_date = datetime.datetime.strptime(d, "%Y-%m-%d")
                break
            except ValueError:
                return print('Invalid entry.')
        
        owner_exists = self.session.query(Owner.owner_name).filter_by(owner_name=owner).first() is not None
        o = self.session.query(Owner).filter(Owner.owner_name == owner).one()
        
        if owner_exists:         
            query = self.session.query(Account).filter(Account.owner_id == o.id)
            accounts = pd.read_sql(query.statement, self.session.bind)
            
            print(f'\"{owner}\" has the following accounts:')
            return accounts.to_dict(orient="records")
        else:
            return print('\nThat Account does not exist.')

    def get_owners(self):             
        query = self.session.query(Owner)
        owners = pd.read_sql(query.statement, self.session.bind)
               
        print('The following Owners exist:')
        print(owners)

        return owners.to_dict(orient="records")

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
    
