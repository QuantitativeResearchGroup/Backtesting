import yfinance as yf
import pandas as pd
from datetime import datetime
# Suppress pandas warnings
pd.options.mode.chained_assignment = None

all_stock_data = None

def getallstock(tickers):
    global all_stock_data
    if all_stock_data is not None:
        return all_stock_data  # Return the cached data if available

    # Get the list of S&P 500 tickers

    data_frames = []
    data_framesIS = []
    data_framesBS = []
    data_framesCF = []
    # Iterate through the tickers
    for ticker in tickers:
        try:
            # Download the ticker's data
            ticker_data = yf.Ticker(ticker)
            info = ticker_data.info

            # Create a DataFrame for the ticker's information
            ticker_info = pd.DataFrame({
                'Ticker.Date': [ticker],
                'Ticker.Exchange':[ticker],
                'Ticker': [ticker],
                'StockExchange': [info.get('exchange', None)],
                'Name': [info.get('longName', None)],
                'Industry': [info.get('industry', None)],
                'Sector': [info.get('sector', None)],
                'LongDescription': [info.get('longBusinessSummary', None)],
                'Website': [info.get('website', None)],
                # 'CIK' : [info.get('address1', None)],# cik
                'HeadQuarter' : [info.get('address1', None)],# hq
                'Founded': [info.get('startDate', None)], # foundation
                '52WeekHigh': ticker_data.history(period="1y")['High'].min(),
                '52WeekLow': ticker_data.history(period="1y")['Low'].min(),
                'Volume': [info.get('averageVolume10days', None)],
                'Range': [info.get('dayRange', None)],
                'Open': [info.get('open', None)],
                'Close': [info.get('regularMarketPreviousClose', None)],
                'Change': [info.get('regularMarketChange', None)],
                'MarketCap': [info.get('marketCap', None)],
                'SharesOutstanding': [info.get('sharesOutstanding', None)],
                'PublicFloat': [info.get('floatShares', None)],
                'PE': [info.get('trailingPE', None)],
                'EPS': [info.get('trailingEps', None)],
                'DividendPct': [info.get('dividendRate', None)],
                'Dividend': [info.get('dividendYield', None)],
                'ExDivDate': [info.get('exDividendDate', None)],
                'ShortFloatPct': [info.get('shortPercentOfFloat', None)],
                'AverageVolume': [info.get('averageVolume', None)],
                'Income': [info.get('trailingAnnualDividendRate', None)],
                'Sales': [info.get('trailingAnnualDividendYield', None)],
                'ShookPerShare': [info.get('sharesShort', None)],
                'CashPerShare': [info.get('regularMarketPrice', None)],
                'Optionable': [info.get('options', None)],
                'Shortable': [info.get('shortable', None)],
                'Employees': [info.get('fullTimeEmployees', None)],
                'Recom': [info.get('recommendationKey', None)],
                'ForwardPE': [info.get('forwardPE', None)],
                'PEG': [info.get('pegRatio', None)],
                'PS': [info.get('priceToSalesTrailing12Months', None)],
                'PB': [info.get('priceToBook', None)],
                'PC': [info.get('priceToCashPerShare', None)],
                'PFCF': [info.get('priceToFreeCashFlows', None)],
                'QuickRatio': [info.get('quickRatio', None)],
                'CurrentRatio': [info.get('currentRatio', None)],
                'DebtToEquity': [info.get('debtToEquity', None)],
                'LongTermDebtToEquity': [info.get('longTermDebtToEquity', None)],
                'SMA20': [info.get('fiftyDayAverage', None)],
                'SMA50': [info.get('twoHundredDayAverage', None)],
                'SMA200': [info.get('twoHundredDayAverage', None)],
                'EPS_TTM': [info.get('trailingEps', None)],
                'EPSNextYear': [info.get('forwardEps', None)],
                'EPSNextQuarter': [info.get('epsForward', None)],
                'EPSThisYear': [info.get('epsCurrentYear', None)],
                'EPSNext5Y': [info.get('fiveYearAvgGrowth', None)],
                'EPSPast5Y': [info.get('trailingPE', None)],
                'EPSGrowthThisYear': [info.get('earningsQuarterlyGrowth', None)],
                'SalesPast5Y': [info.get('revenuePerShare', None)],
                'SalesQQ': [info.get('revenueQuarterlyGrowth', None)],
                'EPSQQ': [info.get('earningsQuarterlyGrowth', None)],
                'EarningsDate': [info.get('earningsTimestamp', None)],
                'InsiderOwn': [info.get('sharesPercentSharesOut', None)],
                'InsiderTrans': [info.get('netInsiderSharesSold', None)],
                'InstOwn': [info.get('institutionPercentSharesOut', None)],
                'InstTrans': [info.get('netInstitutionalSharesSold', None)],
                'ROA': [info.get('returnOnAssets', None)],
                'ROE': [info.get('returnOnEquity', None)],
                'ROI': [info.get('returnOnInvestment', None)],
                'GrossMargin': [info.get('grossMargins', None)],
                'OperMargin': [info.get('operatingMargins', None)],
                'ProfitMargin': [info.get('profitMargins', None)],
                'Payout': [info.get('payoutRatio', None)],
                'ShsOutstand': ['"DoubleCheck"'],
                'ShsFloat': [info.get('sharesFloat', None)],
                'ShortFloatRatio': [info.get('shortRatio', None)],
                'ShortInterest': [info.get('sharesShortPriorMonth', None)],
                'TargetPrice': [info.get('targetMeanPrice', None)],
                'RSI_14': [info.get('trailingRelativeStrength', None)],
                'RelVolume': [info.get('regularMarketVolume', None)],
                'AvgVolume_3m': [info.get('averageDailyVolume3Month', None)],
                'Volume': [info.get('regularMarketVolume', None)],
                'PerfWeek': ['"DoubleCheck"'],
                'PerfMonth': ['"DoubleCheck"'],
                'PerfQuarter': ['"DoubleCheck"'],
                'PerfHalfY': ['"DoubleCheck"'],
                'PerfY': ['"DoubleCheck"'],
                'PerfYTD': ['"DoubleCheck"'],
                'Beta': [info.get('beta', None)],
                'ATR': [info.get('averageTrueRange', None)],
                'Volatility': [info.get('dayRange', None)],
                'PrevClose': [info.get('regularMarketPreviousClose', None)],
                'BookValue': [info.get('bookValue', None)]
            })
            IncomeStatement = pd.DataFrame({
                # check version file based on yfinance
                # versionID to datetime (primarykey)
                'Ticker': [ticker],
                'StockExchange': [info.get('exchange', None)],
                'Ticker.Date': [ticker],
                'Ticker.Exchange':[ticker],
                'Name': [info.get('longName', None)],
                'Industry': [info.get('industry', None)],
                'TotalRevenue': [info.get('totalRevenue', None)],
                'CostOfGoodsSoldInclDA': [info.get('costOfRevenue', None)],
                'GrossProfit': [info.get('grossProfit', None)],
                'SellingGeneralAdministrativeExclOther': [info.get('sellingGeneralAdministrative', None)],
                'OtherOperatingExpense': [info.get('otherOperatingExpenses', None)],
                'OperatingIncome': [info.get('operatingIncome', None)],
                'InterestExpense': [info.get('interestExpense', None)],
                'UnusualExpense': [info.get('unusualExpense', None)],
                'NetIncomeBeforeTaxes': [info.get('incomeBeforeTax', None)],
                'IncomeTaxes': [info.get('taxProvision', None)],
                'ConsolidatedNetIncome': [info.get('netIncome', None)],
                'EPSRecurring': [info.get('trailingEps', None)],
                'EPSBasicBeforeExtraordinaries': [info.get('earningsPerShare', None)],
                'EPSDiluted': [info.get('dilutedEps', None)],
                'EBITDA': [info.get('ebitda', None)],
                'PriceToEarningsRatio': [info.get('trailingPE', None)],
                'PriceToSalesRatio': [info.get('priceToSalesTrailing12Months', None)],
                'GrossMargin': [info.get('grossMargins', None)],
                'OperatingMargin': [info.get('operatingMargins', None)],
                'NetMargin': [info.get('profitMargins', None)],
                'SharesOutstanding': [info.get('sharesOutstanding', None)],
                'MarketCapitalization': [info.get('marketCap', None)]
            })
            BalanceSheet = pd.DataFrame({
                'Ticker': [ticker],
                'StockExchange': [info.get('exchange', None)],
                'Ticker.Date': [ticker],
                'Ticker.Exchange':[ticker],
                'Name': [info.get('longName', None)],
                'TotalAssets': [info.get('totalAssets', None)],
                'CurrentAssets': [info.get('totalCurrentAssets', None)],
                'CashCashEquivalentsShortTermInvestments': [info.get('cashShortTermInvestments', None)],
                'CashAndCashEquivalents': [info.get('cash', None)],
                'OtherShortTermInvestments': [info.get('shortTermInvestments', None)],
                'Receivables': [info.get('netReceivables', None)],
                'AccountsReceivable': [info.get('netReceivables', None)],
                'Inventory': [info.get('inventory', None)],
                'RawMaterials': [info.get('rawMaterials', None)],
                'WorkInProcess': [info.get('workInProcess', None)],
                'FinishedGoods': [info.get('finishedGoods', None)],
                'OtherInventories': [info.get('otherInventories', None)],
                'PrepaidAssets': [info.get('prepaidAssets', None)],
                'RestrictedCash': [info.get('restrictedCash', None)],
                'OtherCurrentAssets': [info.get('otherCurrentAssets', None)],
                'TotalNonCurrentAssets': [info.get('totalNonCurrentAssets', None)],
                'NetPPE': [info.get('propertyPlantEquipment', None)],
                'GrossPPE': [info.get('grossPropertyPlantEquipment', None)],
                'Properties': [info.get('landBuildings', None)],
                'LandAndImprovements': [info.get('landBuildings', None)],
                'MachineryFurnitureEquipment': [info.get('machineryFurnitureEquipment', None)],
                'OtherProperties': [info.get('landBuildings', None)],  # Replace with the correct attribute
                'ConstructionInProgress': [info.get('constructionInProgress', None)],
                'Leases': [info.get('leases', None)],
                'AccumulatedDepreciation': [info.get('accumulatedDepreciation', None)],
                'GoodwillAndOtherIntangibleAssets': [info.get('goodWill', None)],
                'Goodwill': [info.get('goodWill', None)],
                'OtherIntangibleAssets': [info.get('otherIntangibleAssets', None)],
                'NonCurrentNoteReceivables': [info.get('notesPayable', None)],
                'OtherNonCurrentAssets': [info.get('otherAssets', None)],
                'TotalLiabilitiesNetMinorityInterest': [info.get('totalLiab', None)],
                'CurrentLiabilities': [info.get('totalCurrentLiabilities', None)],
                'PayablesAndAccruedExpenses': [info.get('totalPayables', None)],
                'Payables': [info.get('accountsPayable', None)],
                'AccountsPayable': [info.get('accountsPayable', None)],
                'TotalTaxPayable': [info.get('totalTaxPayable', None)],
                'CurrentAccruedExpenses': [info.get('accruedExpenses', None)],
                'InterestPayable': [info.get('interestPayable', None)],
                'CurrentProvisions': [info.get('currentDebt', None)],
                'CurrentDebtAndCapitalLeaseObligation': [info.get('currentDebt', None)],
                'CurrentDebt': [info.get('currentDebt', None)],
                'OtherCurrentBorrowings': [info.get('currentDebt', None)],  # Replace with the correct attribute
                'CurrentCapitalLeaseObligation': [info.get('currentDebt', None)],  # Replace with the correct attribute
                'CurrentDeferredLiabilities': [info.get('currentDebt', None)],  # Replace with the correct attribute
                'CurrentDeferredRevenue': [info.get('currentDebt', None)],  # Replace with the correct attribute
                'OtherCurrentLiabilities': [info.get('currentDebt', None)],  # Replace with the correct attribute
                'TotalNonCurrentLiabilitiesNetMinorityInterest': [info.get('longTermDebt', None)],
                'LongTermProvisions': [info.get('longTermDebt', None)],
                'LongTermDebtAndCapitalLeaseObligation': [info.get('longTermDebt', None)],
                'LongTermDebt': [info.get('longTermDebt', None)],
                'LongTermCapitalLeaseObligation': [info.get('longTermDebt', None)],
                'NonCurrentDeferredLiabilities': [info.get('longTermDebt', None)],  # Replace with the correct attribute
                'NonCurrentDeferredTaxesLiabilities': [info.get('longTermDebt', None)],  # Replace with the correct attribute
                'NonCurrentDeferredRevenue': [info.get('longTermDebt', None)],  # Replace with the correct attribute
                'NonCurrentAccruedExpenses': [info.get('longTermDebt', None)],  # Replace with the correct attribute
                'PreferredSecuritiesOutsideStockEquity': [info.get('preferredStock', None)],
                'OtherNonCurrentLiabilities': [info.get('preferredStock', None)],  # Replace with the correct attribute
                'TotalEquityGrossMinorityInterest': [info.get('totalStockholderEquity', None)],
                'StockholdersEquity': [info.get('totalStockholderEquity', None)],
                'CapitalStock': [info.get('totalStockholderEquity', None)],  # Replace with the correct attribute
                'PreferredStock': [info.get('preferredStock', None)],
                'CommonStock': [info.get('commonStock', None)],
                'AdditionalPaidInCapital': [info.get('totalStockholderEquity', None)],  # Replace with the correct attribute
                'RetainedEarnings': [info.get('retainedEarnings', None)],
                'GainsLossesNotAffectingRetainedEarnings': [info.get('retainedEarnings', None)],  # Replace with the correct attribute
                'OtherEquityAdjustments': [info.get('retainedEarnings', None)],  # Replace with the correct attribute
                'MinorityInterest': [info.get('minorityInterest', None)],
                'TotalCapitalization': [info.get('totalStockholderEquity', None)],  # Replace with the correct attribute
                'CommonStockEquity': [info.get('commonStockEquity', None)],
                'CapitalLeaseObligations': [info.get('capitalLeaseObligations', None)],
                'NetTangibleAssets': [info.get('netTangibleAssets', None)],
                'WorkingCapital': [info.get('workingCapital', None)],
                'InvestedCapital': [info.get('investedCapital', None)],
                'TangibleBookValue': [info.get('tangibleBookValue', None)],
                'TotalDebt': [info.get('longTermDebt', None)],  # Replace with the correct attribute
                'NetDebt': [info.get('longTermDebt', None)],  # Replace with the correct attribute
                'ShareIssued': [info.get('sharesOutstanding', None)],
                'OrdinarySharesNumber': [info.get('sharesOutstanding', None)],  # Replace with the correct attribute
            })
            CashFlow = pd.DataFrame({
                'Ticker': [ticker],
                'StockExchange': [info.get('exchange', None)],
                'Ticker.Date': [ticker],
                'Ticker.Exchange':[ticker],
                'Name': [info.get('longName', None)],
                'OperatingCashFlow': [info.get('Operating Cash Flow', None)],
                'CashFlowFromContinuingOperatingActivities': [info.get('Total Cash From Operating Activities', None)],
                'NetIncomeFromContinuingOperations': [info.get('Total Income', None)],
                'OperatingGainsLosses': [info.get('Gains Losses', None)],
                'GainLossOnSaleOfPPE': [info.get('Sale Purchase of Stock', None)],
                'NetForeignCurrencyExchangeGainLoss': [info.get('Effect of Exchange Rate Changes', None)],
                'DepreciationAmortizationDepletion': [info.get('Depreciation', None)],
                'DepreciationAndAmortization': [info.get('Depreciation', None)],
                'Depreciation': [info.get('Depreciation', None)],
                'AssetImpairmentCharge': [info.get('Effect of Exchange Rate Changes', None)],
                'StockBasedCompensation': [info.get('Stock-based compensation', None)],
                'OtherNonCashItems': [info.get('Effect of Exchange Rate Changes', None)],
                'ChangeInWorkingCapital': [info.get('Effect of Exchange Rate Changes', None)],
                'ChangeInReceivables': [info.get('Change in Receivables', None)],
                'ChangesInAccountReceivables': [info.get('Change in Receivables', None)],
                'ChangeInInventory': [info.get('Change in Inventory', None)],
                'ChangeInPrepaidAssets': [info.get('Change in Prepaid Assets', None)],
                'ChangeInPayablesAndAccruedExpense': [info.get('Change in Payables and Accrued Expense', None)],
                'ChangeInOtherCurrentAssets': [info.get('Change in Other Current Assets', None)],
                'ChangeInOtherCurrentLiabilities': [info.get('Change in Other Current Liabilities', None)],
                'ChangeInOtherWorkingCapital': [info.get('Change in Other Working Capital', None)],
                'InvestingCashFlow': [info.get('Total Cash From Investing Activities', None)],
                'CashFlowFromContinuingInvestingActivities': [info.get('Total Cash From Investing Activities', None)],
                'CapitalExpenditureReported': [info.get('Purchase of Property, Plant & Equipment', None)],
                'NetPPEPurchaseAndSale': [info.get('Purchase of Property, Plant & Equipment', None)],
                'PurchaseOfPPE': [info.get('Purchase of Property, Plant & Equipment', None)],
                'NetIntangiblesPurchaseAndSale': [info.get('Purchase of Intangible Assets', None)],
                'PurchaseOfIntangibles': [info.get('Purchase of Intangible Assets', None)],
                'SaleOfIntangibles': [info.get('Purchase of Intangible Assets', None)],
                'NetBusinessPurchaseAndSale': [info.get('Purchase of Business', None)],
                'PurchaseOfBusiness': [info.get('Purchase of Business', None)],
                'SaleOfBusiness': [info.get('Sale of Business', None)],
                'NetInvestmentPurchaseAndSale': [info.get('Purchase/Sale of Investments', None)],
                'PurchaseOfInvestment': [info.get('Purchase/Sale of Investments', None)],
                'SaleOfInvestment': [info.get('Purchase/Sale of Investments', None)],
                'NetOtherInvestingChanges': [info.get('Investing Cash Flow', None)],
                'FinancingCashFlow': [info.get('Total Cash From Financing Activities', None)],
                'CashFlowFromContinuingFinancingActivities': [info.get('Total Cash From Financing Activities', None)],
                'NetIssuancePaymentsOfDebt': [info.get('Issuance of Debt', None)],
                'NetLongTermDebtIssuance': [info.get('Issuance of Debt', None)],
                'LongTermDebtIssuance': [info.get('Issuance of Debt', None)],
                'LongTermDebtPayments': [info.get('Repayment of Debt', None)],
                'NetCommonStockIssuance': [info.get('Issuance of Capital Stock', None)],
                'CommonStockIssuance': [info.get('Issuance of Capital Stock', None)],
                'ProceedsFromStockOptionExercised': [info.get('Issuance of Capital Stock', None)],
                'NetOtherFinancingCharges': [info.get('Other Financing Charges', None)],
                'EndCashPosition': [info.get('End Cash Position', None)],
                'ChangesInCash': [info.get('Change in Cash', None)],
                'EffectOfExchangeRateChanges': [info.get('Effect of Exchange Rate Changes', None)],
                'BeginningCashPosition': [info.get('Beginning Cash Position', None)],
                'IncomeTaxPaidSupplementalData': [info.get('Effect of Exchange Rate Changes', None)],
                'InterestPaidSupplementalData': [info.get('Effect of Exchange Rate Changes', None)],
                'CapitalExpenditure': [info.get('Purchase of Property, Plant & Equipment', None)],
                'IssuanceOfCapitalStock': [info.get('Issuance of Capital Stock', None)],
                'IssuanceOfDebt': [info.get('Issuance of Debt', None)],
                'RepaymentOfDebt': [info.get('Repayment of Debt', None)],
                'FreeCashFlow': [info.get('Free Cash Flow', None)],
            }   )  
            current_datetime = datetime.now()
            current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')  # alter for date contraint
            # List of DataFrames
            dataframes = [ticker_info, IncomeStatement, BalanceSheet, CashFlow]
            for df in dataframes:
                df['Ticker.Exchange'] = df['Ticker'] + '.' + df['StockExchange']
                df['Ticker.Date'] = df['Ticker.Exchange'] + '.' + current_datetime_str
                # most recent event date from current date. 
                # iterate twice to ensure that there is no missing inserts
                # for new daily data, the method will c
            # Append the DataFrame to the list
            data_frames.append(ticker_info)
            data_framesIS.append(IncomeStatement)
            data_framesBS.append(BalanceSheet)
            data_framesCF.append(CashFlow)
            # print(ticker)
        except Exception as e:
            print(f"Error retrieving data for {ticker}: {str(e)}")

    # Concatenate the list of DataFrames into one DataFrame
    data_frames = pd.concat(data_frames, ignore_index=True)
    data_framesIS = pd.concat(data_framesIS, ignore_index=True)
    data_framesBS = pd.concat(data_framesBS, ignore_index=True)
    data_framesCF = pd.concat(data_framesCF, ignore_index=True)
    return data_frames, data_framesIS, data_framesBS, data_framesCF


def pulldata(stocks):
    a,b,c,d  = getallstock(stocks)  # Fetch the stock data if not cached
    return a,b,c,d

def pulGeneral(stocks,df):
    filtered_data = df[df['Ticker'].isin(stocks)][['Ticker', 'Name', 'StockExchange','Website','52WeekHigh','52WeekLow']]
    return filtered_data

def pullIncomeStatement(stocks,df):
    filtered_data = df[df['Ticker'].isin(stocks)][['Ticker', 'Name', 'TotalRevenue', 'GrossProfit','OperatingIncome']]
    return filtered_data

def pullCashFlow(stocks,df):
    filtered_data = df[df['Ticker'].isin(stocks)][['Ticker', 'Name', 'OperatingCashFlow', 'OperatingGainsLosses','OtherNonCashItems']]
    return filtered_data

def pullBalanceSheet(stocks,df):
    filtered_data = df[df['Ticker'].isin(stocks)][['Ticker', 'Name', 'TotalAssets', 'CurrentAssets', 'CashCashEquivalentsShortTermInvestments']]
    return filtered_data

def pullNews(stocks,df):
    pass

# Call the pulldata method to retrieve the data
#url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' 
#table = pd.read_html(url)[0]
#print(table)
#tickers = table['Symbol'].str.replace('.', '-').to_list()
#tickers = tickers[0:2]
#one,two,three,four = pulldata(tickers)
#print(three)
