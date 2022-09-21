import pandas as pd
import requests
import math
import pickle

from sympy import re

mainCompanyList = []
tax = 0.1
class Dividend:

    def __init__(self, uid, declaredDate:str = '00000000', dividend:float = 0):
        self.uid = uid
        self.declaredDate = declaredDate
        self.recievedDate:str = ''
        self.dividend = dividend
        self.recievedAmount = 0
    
    def update(self, date:str, amount:float):
        self.recievedDate = date
        self.recievedAmount = amount

class Company:

    def __init__(self, companyName:str, bseCode:str, nseCode:str, isinCode:str) -> None:
        self.companyName = companyName
        self.bseCode = bseCode
        self.nseCode = nseCode
        self.isinCode = isinCode
        self.marketPrice:float = 0
        self.dividendsDeclared:list = []
    
    def addDividend(self, newDividend:Dividend):
        flag = 0
        for div in self.dividendsDeclared:
            if(div.uid == newDividend.uid):
                flag = 1
                break
        if flag == 0:
            self.dividendsDeclared.append(newDividend)

class Transaction:

    def __init__(self, date:str, amount:float, quantity:int, transType:str, company:Company):
        self.date = date
        self.amount = amount
        self.quantity = quantity
        self.transType = transType
        self.company = company


class Account:    

    def __init__(self, name:str):
        self.accountHoldersName = name
        self.transactions:list = []
        self.companiesInHolding:list = []

    def addTransaction(self, newTransaction:Transaction):
        self.transactions.append(newTransaction)
        self.companiesInHolding.append(newTransaction.company)
        self.transactions.sort(key=lambda x:int(x.date))

    def getCompanyisin(self, isin:str):
        with open('companyData.pkl', 'rb') as f:
            mainCompanyList = pickle.load(f)

        for c in mainCompanyList:
            if c.isinCode == isin:
                return c

    def clearTransactions(self):
        self.transactions.clear()
        self.companiesInHolding.clear()

    def importTransactions(self, fileName:str):
        self.clearTransactions()
        csv = pd.read_csv(fileName).to_numpy()
        failed = []
        for trans in csv:
            company = self.getCompanyisin(trans[2])
            if(company != None):
                self.addTransaction(Transaction(trans[0], trans[4], trans[3], trans[1], company))
            else:
                failed.append(trans[2])
        return failed


def importCompanies():
    mainCompanyList = []
    queryParamsBSE = {'Group':'',
    'Scripcode':'',
    'industry': '',
    'segment': 'Equity',
    'status': ''
    }
    link = 'https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w'

    header = {
        'Host': 'api.bseindia.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.bseindia.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.bseindia.com/'
    }

    x = requests.get(url=link, params=queryParamsBSE, headers=header)
    df = pd.read_json(x.content)
    # print(df.columns)
    df.drop(['Status', 'GROUP', 'FACE_VALUE', 'INDUSTRY', 'scrip_id', 'Segment','NSURL', 'Issuer_Name', 'Mktcap'], axis=1, inplace=True)
    # print(df.head())
    for company in df.to_numpy():
        if(len(company[2])>5):
            mainCompanyList.append(Company(company[1],company[0],'', company[2]))

    # print(len(mainCompanyList))

    df = pd.read_csv('https://archives.nseindia.com/content/equities/EQUITY_L.csv')
    # print(df.columns)
    df.drop([' SERIES', ' DATE OF LISTING', ' PAID UP VALUE', ' MARKET LOT', ' FACE VALUE'], axis=1, inplace=True)
    
    for NSEcompany in df.to_numpy():
        br_flag = 0
        for BSEcompany in mainCompanyList:
            if(BSEcompany.isinCode == NSEcompany[2]):
                BSEcompany.nseCode = NSEcompany[0]
                br_flag = 1
                break
        if(br_flag == 0):
            mainCompanyList.append(Company(NSEcompany[1], '', NSEcompany[0], NSEcompany[2]))

    # print(len(mainCompanyList))
    return mainCompanyList
    # print(df.head())

def importDividends(acc:Account, year):
    queryParams = {'Fdate': str(year-1) + '0401',
    'Purposecode': 'P9',
    'TDate': str(year) + '0331',
    'ddlcategorys': 'E',
    'ddlindustrys':'',
    'scripcode':'',
    'segment': '0',
    'strSearch': 'S'}
    link = 'https://api.bseindia.com/BseIndiaAPI/api/DefaultData/w'

    header = {
        'Host': 'api.bseindia.com',
        'User-Agent': 'whatever you want',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.bseindia.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.bseindia.com/'
    }

    x = requests.get(url=link, params=queryParams, headers=header)
    df = pd.read_json(x.content)
    
    df.drop(['short_name', 'Ex_date', 'long_name', 'RD_Date', 'BCRD_FROM', 'BCRD_TO', 'ND_START_DATE', 'ND_END_DATE', 'payment_date'], axis=1, inplace=True)
    
    for indx, dividend in enumerate(df.to_numpy()):
        for company in acc.companiesInHolding:
            if(company.bseCode == dividend[0]):
                if(dividend[1].find('Rs. - ')!=-1):
                    div = float(dividend[1].split('Rs. - ')[1])
                    company.addDividend(Dividend(str(year) + str(indx), dividend[2], div))
                    break

    return acc

def genAccTransReport(account:Account, finYear:int):
    report = []
    totalPrevQuantityPerCompanyDict = {}
    totalPrevAmountPerCompanyDict = {}

    totalQuantityPerCompanyDict = {}

    for trans in account.transactions:
        print(trans.company.companyName, trans.company, trans.transType, trans.date)
        if(int(trans.date) < int(str(finYear-1) + '0401')):
            try:
                if(trans.transType == 'Opening Balance'):
                    totalPrevQuantityPerCompanyDict[trans.company.isinCode] = trans.quantity
                    totalPrevAmountPerCompanyDict[trans.company.isinCode] = trans.amount
                elif(trans.transType == 'Purchase'):
                    totalPrevQuantityPerCompanyDict[trans.company.isinCode] += trans.quantity
                    totalPrevAmountPerCompanyDict[trans.company.isinCode] += trans.amount
                elif(trans.transType == 'Sale'):
                    print("hi, I want to sell")
                    totalPrevQuantityPerCompanyDict[trans.company.isinCode] -= trans.quantity
                    totalPrevAmountPerCompanyDict[trans.company.isinCode] -= trans.amount
            except:
                totalPrevQuantityPerCompanyDict[trans.company.isinCode] = trans.quantity
                totalPrevAmountPerCompanyDict[trans.company.isinCode] = trans.amount
        elif(int(str(finYear-1) + '0401') <= int(trans.date) <=  int(str(finYear) + '0331')):
            if(len(report) == 0):
                totalQuantityPerCompanyDict = totalPrevQuantityPerCompanyDict.copy()
                for company in list(totalPrevQuantityPerCompanyDict.keys()):
                    for c in account.companiesInHolding:
                        if c.isinCode == company:
                            company = c
                    # company = account.getCompanyisin(company)
                    if(totalPrevQuantityPerCompanyDict[company.isinCode]!=0):
                        report.append({'Date': '00000000', 'ISIN Code': company.isinCode, 'BSE Code':company.bseCode, 'NSE Code':company.nseCode, 'Company Name':company.companyName, 'Quantity':totalPrevQuantityPerCompanyDict[company.isinCode], 'Unit Price': totalPrevAmountPerCompanyDict[company.isinCode]/totalPrevQuantityPerCompanyDict[company.isinCode], 'Amount':totalPrevAmountPerCompanyDict[company.isinCode], 'Total Quantity':totalPrevQuantityPerCompanyDict[company.isinCode]})
            try:
                if(trans.transType == 'Opening Balance'):
                    totalQuantityPerCompanyDict[trans.company.isinCode] = trans.quantity
                elif(trans.transType == 'Purchase'):
                    totalQuantityPerCompanyDict[trans.company.isinCode] += trans.quantity
                elif(trans.transType == 'Sale'):
                    print("hi Im selling here though", totalQuantityPerCompanyDict)
                    totalQuantityPerCompanyDict[trans.company.isinCode] -= trans.quantity
            except:
                print("hi, im stupid if I ended up here", totalQuantityPerCompanyDict)
                totalQuantityPerCompanyDict[trans.company.isinCode] = trans.quantity
            
            report.append({'Date': trans.date, 'ISIN Code': trans.company.isinCode, 'BSE Code': trans.company.bseCode, 'NSE Code': trans.company.nseCode, 'Company Name': trans.company.companyName, 'Quantity': trans.quantity, 'Unit Price': trans.amount/trans.quantity, 'Amount':trans.amount, 'Total Quantity':totalQuantityPerCompanyDict[trans.company.isinCode]})
    # print(report)
    if(len(report) == 0):
                totalQuantityPerCompanyDict = totalPrevQuantityPerCompanyDict.copy()
                for company in list(totalPrevQuantityPerCompanyDict.keys()):
                    report.append({'Date': '00000000', 'ISIN Code': company.isinCode, 'BSE Code':company.bseCode, 'NSE Code':company.nseCode, 'Company Name':company.companyName, 'Quantity':totalPrevQuantityPerCompanyDict[company], 'Unit Price': totalPrevAmountPerCompanyDict[company]/totalPrevQuantityPerCompanyDict[company], 'Amount':totalPrevAmountPerCompanyDict[company], 'Total Quantity':totalPrevQuantityPerCompanyDict[company]})
    report.sort(key=lambda x: int(x['Date']))
    # for i in report:
    #     print(i)
    return report


def genAccDividendReport(account:Account, finYear:int):
    report = []
    accTransReport = genAccTransReport(account, finYear)
    # print(accTransReport)
    # account = importDividends(account, finYear)
    taxedYet = {}
    totalQuantity = 0
    row = {}
    totalAmountPerCompanyDict = {}
    for company in account.companiesInHolding:
        taxedYet[company] = False
    
    for company in account.companiesInHolding:
        # print(company.companyName)
        for dividend in company.dividendsDeclared:
            # print(dividend.declaredDate)
            dateToConsider = ''
            if(dividend.recievedDate == ''):
                dateToConsider = dividend.declaredDate
            else:
                dateToConsider =  dividend.recievedDate
            # print(dateToConsider)
            if(int(str(finYear-1) + '0401') <= int(dateToConsider) <= int(str(finYear) + '0331')):
                # print(len(accTransReport))
                for trans in accTransReport:
                    # print(trans['date'], dividend.declaredDate)
                    if(int(trans['Date']) < int(dividend.declaredDate) and trans['ISIN Code'] == company.isinCode):
                        # print(trans['date'])
                        totalQuantity = trans['Total Quantity']
                row = {'Date': dividend.declaredDate, 'ISIN Code': company.isinCode, 'BSE Code': company.bseCode, 'NSE Code': company.nseCode, 'Company Name': company.companyName, 'Dividend Declared': dividend.dividend, 'Quantity': totalQuantity, 'Dividend Amount': dividend.dividend*totalQuantity, 'Recieved Date':dividend.recievedDate, 'Recieved Amount': dividend.recievedAmount}
                try:
                    totalAmountPerCompanyDict[company] += row['Dividend Amount']
                except:
                    totalAmountPerCompanyDict[company] = row['Dividend Amount']
                
                if(totalAmountPerCompanyDict[company] >= 5000):
                    if(taxedYet[company]):
                        row['Tax Amount'] = math.ceil(row['Dividend Amount']*tax)
                        row['Final Amount'] = row['Dividend Amount'] - row['Tax Amount']
                    else:
                        row['Tax Amount'] = math.ceil(totalAmountPerCompanyDict[company]*tax)
                        row['Final Amount'] = row['Dividend Amount'] - row['Tax Amount']
                        taxedYet[company] = True
                else:
                    row['Tax Amount'] = 0
                    row['Final Amount'] = row['Dividend Amount'] - row['Tax Amount']
                row['Id'] = dividend.uid
                report.append(row)
    # print(len(report))
    report.sort(key=lambda x: int(x['Date']))
    return report
    

