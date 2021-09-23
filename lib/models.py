from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData, Float, Date, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker, relationship, backref
import config as cnf
import secret as sct

base = declarative_base()

# account_trans = Table(
#     "account_trans",
#     base.metadata,
#     Column("account_id", Integer, ForeignKey("accounts.id")),
#     Column("transaction_id", Integer, ForeignKey("transactions.id")),
# )

class Owner(base):  
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    owner_name = Column(String)
    owner_salary = Column(Float)
    owner_otherincome = Column(Float)
    owner_tfsa_room = Column(Float)
    owner_rrsp_room = Column(Float)
    accounts = relationship('Account', cascade="all, delete", backref='par_owner')

class Account(base):  
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_name = Column(String)
    account_type = Column(String)
    account_inst = Column(String)
    account_sbal = Column(Float)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    transactions = relationship('Transaction', cascade="all, delete", backref='par_accounts')

class Transaction(base):  
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    trans_date = Column(Date)
    trans_amount = Column(Float)
    account_id = Column(Integer, ForeignKey('accounts.id'))

db_uri = 'postgresql+psycopg2://'+sct.username+':'+sct.password+'@'+cnf.db_server+'/'+cnf.db_name
db = create_engine(db_uri)
base.metadata.create_all(db)



