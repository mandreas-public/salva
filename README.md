# salva
Salva is a retirement savings app - a passion project for me to consolidate spreadsheets!

# About
Salva demonstrates Postgres SQL integration on a self hosted database.  It currently consists of a CLI application this is half finished at best.  My goal is to build a complete front end of the software.

# Files
account.py - allows user to build and manage an account (a retirement savings account - ex: wealthsimple, rbc, etc).
owner.py - allows user to manage account owners (self, other).
transaction.py - allows user to enter retirement account transactions such as deposits or withdrawls.
models.py - build the database models for the various tables required in Postgres.
main.py - the main application as a CLI.
app.py - a working file to get a GUI front end of the program incorporated.
