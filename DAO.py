import pickle
from application import *
# from application import Account, Transaction, Company, importCompanies

def newAccount(name:str):
    
    with open('data.pkl', 'rb') as f:
        database = pickle.load(f)

    database[name] = Account(name)

    with open('data.pkl', 'wb') as f:
        pickle.dump(database, f)



def getAccountList():
    with open('data.pkl', 'rb') as f:
        database = pickle.load(f)

    accountNameList = list(database.keys())

    return accountNameList

def getAccount(accountName:str):
    with open('data.pkl', 'rb') as f:
        database = pickle.load(f)
    return database[accountName]

def importTransAcc(accountName:str, filename:str):
    with open('data.pkl', 'rb') as f:
        database = pickle.load(f)
    
    failed = database[accountName].importTransactions(filename)

    with open('data.pkl', 'wb') as f:
        pickle.dump(database, f)
    return failed


def updateCompanyList():
    mainCompanyList = importCompanies()    

    with open('companyData.pkl', 'wb') as f:
        pickle.dump(mainCompanyList, f)

def getCompanyList():
    with open('companyData.pkl', 'rb') as f:
        mainCompanyList = pickle.load(f)

    companyNameList = [c.isinCode + " - " + c.companyName for c in mainCompanyList]
    companyNameList.sort()

    return companyNameList

def getCompany(companyName:str):
    with open('companyData.pkl', 'rb') as f:
        mainCompanyList = pickle.load(f)

    for c in mainCompanyList:
        if c.companyName == companyName:
            return c

def getCompanyisin(isin:str):
    with open('companyData.pkl', 'rb') as f:
        mainCompanyList = pickle.load(f)

    for c in mainCompanyList:
        if c.isinCode == isin:
            return c

def newTransaction(accName:str, date:str, amount:float, quantity:int, transactionType:str, companyName:str):
    
    with open('data.pkl', 'rb') as f:
        database = pickle.load(f)
    
    
    print(Transaction("20201012", 100.0, 10, "Purchase", Company("hello kitty", "a", "b", "c")))

    company:Company = getCompanyisin(companyName[:12])
    print(company, date, amount, quantity, transactionType)
    transac = Transaction(date, amount, quantity, transactionType, company)
    database[accName].addTransaction(transac)

    with open('data.pkl', 'wb') as f:
        pickle.dump(database, f)

def reset():
    with open('data.pkl', 'rb') as f:
        database = pickle.load(f)

    database = {}

    with open('data.pkl', 'wb') as f:
        pickle.dump(database, f)
