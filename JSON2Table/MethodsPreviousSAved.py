import psycopg2
import pandas as pd
from pulldata import *


pd.options.mode.chained_assignment = None

def establish_database_connection():
    conn = psycopg2.connect(
        dbname='MyDatabase',
        user='postgres',
        password='bobwashere',
        host='localhost',
        port=5432
    )
    return conn

def create_general_table_if_not_exists(cur):
    create_general_table_query = """
    CREATE TABLE IF NOT EXISTS General (
        "Ticker.Exchange" VARCHAR(50) PRIMARY KEY,
        "Ticker.Date" TEXT,
        Ticker VARCHAR(10),
        StockExchange VARCHAR(50),
        Name VARCHAR(100),
        Industry VARCHAR(50),
        Sector VARCHAR(50),
        LongDescription TEXT,
        Website VARCHAR(255),
        "52WeekHigh" NUMERIC(10, 2),
        "52WeekLow" NUMERIC(10, 2),
        Volume TEXT
    );
    """
    cur.execute(create_general_table_query)

def create_balancesheet_table_if_not_exists(cur):
    create_balancesheet_table_query = """
CREATE TABLE IF NOT EXISTS BalanceSheet (
    "Ticker.Exchange" VARCHAR(50) PRIMARY KEY,
    "Ticker.Date" TEXT,
    Ticker VARCHAR(10),
    StockExchange VARCHAR(50),
    Name VARCHAR(100),
    "TotalAssets" NUMERIC(10, 2),
    "CurrentAssets" NUMERIC(10, 2),
    "CashCashEquivalentsShortTermInvestments" NUMERIC(10, 2),
    "CashAndCashEquivalents" NUMERIC(10, 2),
    "OtherShortTermInvestments" NUMERIC(10, 2),
    "Receivables" NUMERIC(10, 2),
    "AccountsReceivable" NUMERIC(10, 2),
    "Inventory" NUMERIC(10, 2),
    "RawMaterials" NUMERIC(10, 2),
    "WorkInProcess" NUMERIC(10, 2),
    "FinishedGoods" NUMERIC(10, 2),
    "OtherInventories" NUMERIC(10, 2),
    "PrepaidAssets" NUMERIC(10, 2),
    "RestrictedCash" NUMERIC(10, 2),
    "OtherCurrentAssets" NUMERIC(10, 2),
    "TotalNonCurrentAssets" NUMERIC(10, 2),
    "NetPPE" NUMERIC(10, 2),
    "GrossPPE" NUMERIC(10, 2),
    "Properties" NUMERIC(10, 2),
    "LandAndImprovements" NUMERIC(10, 2),
    "MachineryFurnitureEquipment" NUMERIC(10, 2),
    "OtherProperties" NUMERIC(10, 2),
    "ConstructionInProgress" NUMERIC(10, 2),
    "Leases" NUMERIC(10, 2),
    "AccumulatedDepreciation" NUMERIC(10, 2),
    "GoodwillAndOtherIntangibleAssets" NUMERIC(10, 2),
    "Goodwill" NUMERIC(10, 2),
    "OtherIntangibleAssets" NUMERIC(10, 2),
    "NonCurrentNoteReceivables" NUMERIC(10, 2),
    "OtherNonCurrentAssets" NUMERIC(10, 2),
    "TotalLiabilitiesNetMinorityInterest" NUMERIC(10, 2),
    "CurrentLiabilities" NUMERIC(10, 2),
    "PayablesAndAccruedExpenses" NUMERIC(10, 2),
    "Payables" NUMERIC(10, 2),
    "AccountsPayable" NUMERIC(10, 2),
    "TotalTaxPayable" NUMERIC(10, 2),
    "CurrentAccruedExpenses" NUMERIC(10, 2),
    "InterestPayable" NUMERIC(10, 2),
    
    "CurrentProvisions" NUMERIC(10, 2),
    "CurrentDebtAndCapitalLeaseObligation" NUMERIC(10, 2),
    "CurrentDebt" NUMERIC(10, 2),
    "OtherCurrentBorrowings" NUMERIC(10, 2),
    "CurrentCapitalLeaseObligation" NUMERIC(10, 2),
    "CurrentDeferredLiabilities" NUMERIC(10, 2),
    "CurrentDeferredRevenue" NUMERIC(10, 2),
    "OtherCurrentLiabilities" NUMERIC(10, 2),
    "TotalNonCurrentLiabilitiesNetMinorityInterest" NUMERIC(10, 2),
    "LongTermProvisions" NUMERIC(10, 2),
    "LongTermDebtAndCapitalLeaseObligation" NUMERIC(10, 2),
    "LongTermDebt" NUMERIC(10, 2),
    "LongTermCapitalLeaseObligation" NUMERIC(10, 2),
    "NonCurrentDeferredLiabilities" NUMERIC(10, 2),
    "NonCurrentDeferredTaxesLiabilities" NUMERIC(10, 2),
    "NonCurrentDeferredRevenue" NUMERIC(10, 2),
    "NonCurrentAccruedExpenses" NUMERIC(10, 2),
    "PreferredSecuritiesOutsideStockEquity" NUMERIC(10, 2),
    "OtherNonCurrentLiabilities" NUMERIC(10, 2),
    "TotalEquityGrossMinorityInterest" NUMERIC(10, 2),
    "StockholdersEquity" NUMERIC(10, 2),
    "CapitalStock" NUMERIC(10, 2),
    "PreferredStock" NUMERIC(10, 2),
    "CommonStock" NUMERIC(10, 2),
    
    "AdditionalPaidInCapital" NUMERIC(10, 2),
    "RetainedEarnings" NUMERIC(10, 2),
    "GainsLossesNotAffectingRetainedEarnings" NUMERIC(10, 2),
    
    "OtherEquityAdjustments" NUMERIC(10, 2),
    "MinorityInterest" NUMERIC(10, 2),
    "TotalCapitalization" NUMERIC(10, 2),
    
    "CommonStockEquity" NUMERIC(10, 2),
    "CapitalLeaseObligations" NUMERIC(10, 2),
    "NetTangibleAssets" NUMERIC(10, 2),
    
    "WorkingCapital" NUMERIC(10, 2),
    "InvestedCapital" NUMERIC(10, 2),
    "TangibleBookValue" NUMERIC(10, 2),
    
    "TotalDebt" NUMERIC(10, 2),
    "NetDebt" NUMERIC(10, 2),
    "ShareIssued" NUMERIC(10, 2),
    
    "OrdinarySharesNumber" NUMERIC(10, 2)
);

"""
    cur.execute(create_balancesheet_table_query)
    
def update_or_insert_general_data(cur, ticker, row):
    check_query = "SELECT COUNT(*) FROM General WHERE Ticker = %s;"
    cur.execute(check_query, (ticker,))
    count = cur.fetchone()[0]

    if count > 0:
        update_query = """
        UPDATE General
        SET "Ticker.Date" = %s, "Ticker.Exchange" = %s, StockExchange = %s, Name = %s, Industry = %s, Sector = %s, 
            LongDescription = %s, Website = %s, "52WeekHigh" = %s, "52WeekLow" = %s, 
            Volume = %s
        WHERE Ticker = %s;
        """
        cur.execute(update_query, (
            row['Ticker.Date'],
            row['Ticker.Exchange'],
            row['StockExchange'],
            row['Name'],
            row['Industry'],
            row['Sector'],
            row['LongDescription'],
            row['Website'],
            row['52WeekHigh'],
            row['52WeekLow'],
            str(row['Volume']),
            ticker
        ))
    else:
        insert_query = """
        INSERT INTO General ("Ticker.Date", "Ticker.Exchange", Ticker, StockExchange, Name, Industry, Sector, LongDescription, Website, "52WeekHigh", "52WeekLow", Volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, ( 
            row['Ticker.Date'],
            row['Ticker.Exchange'],
            ticker,
            row['StockExchange'],
            row['Name'],
            row['Industry'],
            row['Sector'],
            row['LongDescription'],
            row['Website'],
            row['52WeekHigh'],
            row['52WeekLow'],
            str(row['Volume']),  
        ))
 
def update_or_insert_Balance_Sheet_data(cur, ticker, row):
    check_query = "SELECT COUNT(*) FROM BalanceSheet WHERE Ticker = %s;"
    cur.execute(check_query, (ticker,))
    count = cur.fetchone()[0]


    if count > 0:
        update_query = """
        UPDATE BalanceSheet
        SET "Ticker.Date" = %s, "Ticker.Exchange" = %s, "StockExchange" = %s, Name = %s, "TotalAssets" = %s, "CurrentAssets" = %s, "CashCashEquivalentsShortTermInvestments" = %s, "CashAndCashEquivalents" = %s, "OtherShortTermInvestments" = %s, "Receivables" = %s, "AccountsReceivable" = %s, "Inventory" = %s, "RawMaterials" = %s, "WorkInProcess" = %s, "FinishedGoods" = %s, "OtherInventories" = %s, "PrepaidAssets" = %s, "RestrictedCash" = %s, "OtherCurrentAssets" = %s, "TotalNonCurrentAssets" = %s, "NetPPE" = %s, "GrossPPE" = %s, "Properties" = %s, "LandAndImprovements" = %s, "MachineryFurnitureEquipment" = %s, "OtherProperties" = %s, "ConstructionInProgress" = %s, "Leases" = %s, "AccumulatedDepreciation" = %s, "GoodwillAndOtherIntangibleAssets" = %s, "Goodwill" = %s, "OtherIntangibleAssets" = %s, "NonCurrentNoteReceivables" = %s, "OtherNonCurrentAssets" = %s, "TotalLiabilitiesNetMinorityInterest" = %s, "CurrentLiabilities" = %s, "PayablesAndAccruedExpenses" = %s, "Payables" = %s, "AccountsPayable" = %s, "TotalTaxPayable" = %s, "CurrentAccruedExpenses" = %s, "InterestPayable" = %s, "CurrentProvisions" = %s, "CurrentDebtAndCapitalLeaseObligation" = %s, "CurrentDebt" = %s, "OtherCurrentBorrowings" = %s, "CurrentCapitalLeaseObligation" = %s, "CurrentDeferredLiabilities" = %s, "CurrentDeferredRevenue" = %s, "OtherCurrentLiabilities" = %s, "TotalNonCurrentLiabilitiesNetMinorityInterest" = %s, "LongTermProvisions" = %s, "LongTermDebtAndCapitalLeaseObligation" = %s, "LongTermDebt" = %s, "LongTermCapitalLeaseObligation" = %s, "NonCurrentDeferredLiabilities" = %s, "NonCurrentDeferredTaxesLiabilities" = %s, "NonCurrentDeferredRevenue" = %s, "NonCurrentAccruedExpenses" = %s, "PreferredSecuritiesOutsideStockEquity" = %s, "OtherNonCurrentLiabilities" = %s, "TotalEquityGrossMinorityInterest" = %s, "StockholdersEquity" = %s, "CapitalStock" = %s, "PreferredStock" = %s, "CommonStock" = %s, "AdditionalPaidInCapital" = %s, "RetainedEarnings" = %s, "GainsLossesNotAffectingRetainedEarnings" = %s, "OtherEquityAdjustments" = %s, "MinorityInterest" = %s, "TotalCapitalization" = %s, "CommonStockEquity" = %s, "CapitalLeaseObligations" = %s, "NetTangibleAssets" = %s, "WorkingCapital" = %s, "InvestedCapital" = %s, "TangibleBookValue" = %s, "TotalDebt" = %s, "NetDebt" = %s, "ShareIssued" = %s, "OrdinarySharesNumber" = %s
        WHERE Ticker = %s;
        """
        cur.execute(update_query, (
            row['Ticker.Date'],
            row['Ticker.Exchange'],
            row['StockExchange'],
            row['Name'],
            row['TotalAssets'],
            row['CurrentAssets'],
            row['CashCashEquivalentsShortTermInvestments'],
            row['CashAndCashEquivalents'],
            row['OtherShortTermInvestments'],
            row['Receivables'],
            
            row['AccountsReceivable'],
            row['Inventory'],
            row['RawMaterials'],
            row['WorkInProcess'],
            row['FinishedGoods'],
            row['OtherInventories'],
            row['PrepaidAssets'],
            row['RestrictedCash'],
            row['OtherCurrentAssets'],
            row['TotalNonCurrentAssets'],
            row['NetPPE'],
            row['GrossPPE'],
            row['Properties'],
            row['LandAndImprovements'],
            row['MachineryFurnitureEquipment'],
            row['OtherProperties'],
            row['ConstructionInProgress'],
            row['Leases'],
            row['AccumulatedDepreciation'],
            row['GoodwillAndOtherIntangibleAssets'],
            row['Goodwill'],
            row['OtherIntangibleAssets'],
            row['NonCurrentNoteReceivables'],
            row['OtherNonCurrentAssets'],
            row['TotalLiabilitiesNetMinorityInterest'],
            row['CurrentLiabilities'],
            row['PayablesAndAccruedExpenses'],
            row['Payables'],
            
            row['AccountsPayable'],
            row['TotalTaxPayable'],
            row['CurrentAccruedExpenses'],
            row['InterestPayable'],
            row['CurrentProvisions'],
            row['CurrentDebtAndCapitalLeaseObligation'],
            row['CurrentDebt'],
            row['OtherCurrentBorrowings'],
            row['CurrentCapitalLeaseObligation'],
            row['CurrentDeferredLiabilities'],
            row['CurrentDeferredRevenue'],
            row['OtherCurrentLiabilities'],
            row['TotalNonCurrentLiabilitiesNetMinorityInterest'],
            row['LongTermProvisions'],
            row['LongTermDebtAndCapitalLeaseObligation'],
            row['LongTermDebt'],
            row['LongTermCapitalLeaseObligation'],
            row['NonCurrentDeferredLiabilities'],
            row['NonCurrentDeferredTaxesLiabilities'],
            row['NonCurrentDeferredRevenue'],
            row['NonCurrentAccruedExpenses'],
            row['PreferredSecuritiesOutsideStockEquity'],
            row['OtherNonCurrentLiabilities'],
            row['TotalEquityGrossMinorityInterest'],
            row['StockholdersEquity'],
            row['CapitalStock'],
            row['PreferredStock'],
            row['CommonStock'],
            
            row['AdditionalPaidInCapital'],
            row['RetainedEarnings'],
            
            row['GainsLossesNotAffectingRetainedEarnings'],
            row['OtherEquityAdjustments'],
            row['MinorityInterest'],
            row['TotalCapitalization'],
            row['CommonStockEquity'],
            row['CapitalLeaseObligations'],
            row['NetTangibleAssets'],
            row['WorkingCapital'],
            row['InvestedCapital'],
            row['TangibleBookValue'],
            row['TotalDebt'],
            row['NetDebt'],
            row['ShareIssued'],
            row['OrdinarySharesNumber'],
            ticker
        ))
    else:
        insert_query = """
        INSERT INTO BalanceSheet (Ticker, "Ticker.Date", "Ticker.Exchange", StockExchange, Name, "TotalAssets", "CurrentAssets",
        "CashCashEquivalentsShortTermInvestments", "CashAndCashEquivalents", "OtherShortTermInvestments", "Receivables",
        "AccountsReceivable", "Inventory", "RawMaterials", "WorkInProcess", "FinishedGoods", "OtherInventories",
        "PrepaidAssets", "RestrictedCash", "OtherCurrentAssets", "TotalNonCurrentAssets", "NetPPE", "GrossPPE",
        "Properties", "LandAndImprovements", "MachineryFurnitureEquipment", "OtherProperties", "ConstructionInProgress",
        "Leases", "AccumulatedDepreciation", "GoodwillAndOtherIntangibleAssets", "Goodwill", "OtherIntangibleAssets",
        "NonCurrentNoteReceivables", "OtherNonCurrentAssets", "TotalLiabilitiesNetMinorityInterest", "CurrentLiabilities",
        "PayablesAndAccruedExpenses", "Payables", "AccountsPayable", "TotalTaxPayable", "CurrentAccruedExpenses",
        "InterestPayable", "CurrentProvisions", "CurrentDebtAndCapitalLeaseObligation", "CurrentDebt", "OtherCurrentBorrowings",
        "CurrentCapitalLeaseObligation", "CurrentDeferredLiabilities", "CurrentDeferredRevenue", "OtherCurrentLiabilities",
        "TotalNonCurrentLiabilitiesNetMinorityInterest", "LongTermProvisions", "LongTermDebtAndCapitalLeaseObligation",
        "LongTermDebt", "LongTermCapitalLeaseObligation", "NonCurrentDeferredLiabilities", "NonCurrentDeferredTaxesLiabilities",
        "NonCurrentDeferredRevenue", "NonCurrentAccruedExpenses", "PreferredSecuritiesOutsideStockEquity", "OtherNonCurrentLiabilities",
        "TotalEquityGrossMinorityInterest", "StockholdersEquity", "CapitalStock", "PreferredStock", "CommonStock",
        "AdditionalPaidInCapital", "RetainedEarnings", "GainsLossesNotAffectingRetainedEarnings", "OtherEquityAdjustments",
        "MinorityInterest", "TotalCapitalization", "CommonStockEquity", "CapitalLeaseObligations", "NetTangibleAssets",
        "WorkingCapital", "InvestedCapital", "TangibleBookValue", "TotalDebt", "NetDebt", "ShareIssued", "OrdinarySharesNumber")
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """
        values = [
            ticker,
            row['Ticker.Date'],
            row['Ticker.Exchange'],
            row['StockExchange'],
            row['Name'],
            int(row['TotalAssets']) if row['TotalAssets'] is not None else None,
            int(row['CurrentAssets']) if row['CurrentAssets'] is not None else None,
            int(row['CashCashEquivalentsShortTermInvestments']) if row['CashCashEquivalentsShortTermInvestments'] is not None else None,
            int(row['CashAndCashEquivalents']) if row['CashAndCashEquivalents'] is not None else None,
            int(row['OtherShortTermInvestments']) if row['OtherShortTermInvestments'] is not None else None,
            int(row['Receivables']) if row['Receivables'] is not None else None,
            int(row['AccountsReceivable']) if row['AccountsReceivable'] is not None else None,
            int(row['Inventory']) if row['Inventory'] is not None else None,
            int(row['RawMaterials']) if row['RawMaterials'] is not None else None,
            int(row['WorkInProcess']) if row['WorkInProcess'] is not None else None,
            int(row['FinishedGoods']) if row['FinishedGoods'] is not None else None,
            
            int(row['OtherInventories']) if row['OtherInventories'] is not None else None,
            int(row['PrepaidAssets']) if row['PrepaidAssets'] is not None else None,
            int(row['RestrictedCash']) if row['RestrictedCash'] is not None else None,
            int(row['OtherCurrentAssets']) if row['OtherCurrentAssets'] is not None else None,
            int(row['TotalNonCurrentAssets']) if row['TotalNonCurrentAssets'] is not None else None,
            int(row['NetPPE']) if row['NetPPE'] is not None else None,
            int(row['GrossPPE']) if row['GrossPPE'] is not None else None,
            int(row['Properties']) if row['Properties'] is not None else None,
            int(row['LandAndImprovements']) if row['LandAndImprovements'] is not None else None,
            
            int(row['MachineryFurnitureEquipment']) if row['MachineryFurnitureEquipment'] is not None else None,
            int(row['OtherProperties']) if row['OtherProperties'] is not None else None,
            int(row['ConstructionInProgress']) if row['ConstructionInProgress'] is not None else None,
            int(row['Leases']) if row['Leases'] is not None else None ,
            int(row['AccumulatedDepreciation']) if row['AccumulatedDepreciation'] is not None else None ,
            int(row['GoodwillAndOtherIntangibleAssets']) if row['GoodwillAndOtherIntangibleAssets'] is not None else None ,
            int(row['Goodwill']) if row['Goodwill'] is not None else None ,
            int(row['OtherIntangibleAssets']) if row['OtherIntangibleAssets'] is not None else None ,
            int(row['NonCurrentNoteReceivables']) if row['NonCurrentNoteReceivables'] is not None else None ,
            int(row['OtherNonCurrentAssets']) if row['OtherNonCurrentAssets'] is not None else None ,
            int(row['TotalLiabilitiesNetMinorityInterest']) if row['TotalLiabilitiesNetMinorityInterest'] is not None else None ,
            int(row['CurrentLiabilities']) if row['CurrentLiabilities'] is not None else None ,
            int(row['PayablesAndAccruedExpenses']) if row['PayablesAndAccruedExpenses'] is not None else None ,
            int(row['Payables']) if row['Payables'] is not None else None ,
            
            int(row['AccountsPayable']) if row['AccountsPayable'] is not None else None ,
            int(row['TotalTaxPayable']) if row['TotalTaxPayable'] is not None else None ,
            int(row['CurrentAccruedExpenses']) if row['CurrentAccruedExpenses'] is not None else None ,
            int(row['InterestPayable']) if row['InterestPayable'] is not None else None ,
            
            int(row['CurrentProvisions']) if row['CurrentProvisions'] is not None else None ,
            int(row['CurrentDebtAndCapitalLeaseObligation']) if row['CurrentDebtAndCapitalLeaseObligation'] is not None else None ,
            int(row['CurrentDebt']) if row['CurrentDebt'] is not None else None ,
            int(row['OtherCurrentBorrowings']) if row['OtherCurrentBorrowings'] is not None else None ,
            int(row['CurrentCapitalLeaseObligation']) if row['CurrentCapitalLeaseObligation'] is not None else None ,
            int(row['CurrentDeferredLiabilities']) if row['FinishedGoods'] is not None else None ,
            int(row['CurrentDeferredRevenue']) if row['CurrentDeferredLiabilities'] is not None else None ,
            int(row['OtherCurrentLiabilities']) if row['OtherCurrentLiabilities'] is not None else None ,
            int(row['TotalNonCurrentLiabilitiesNetMinorityInterest']) if row['TotalNonCurrentLiabilitiesNetMinorityInterest'] is not None else None ,
            int(row['LongTermProvisions']) if row['LongTermProvisions'] is not None else None ,
            int(row['LongTermDebtAndCapitalLeaseObligation']) if row['LongTermDebtAndCapitalLeaseObligation'] is not None else None ,
            int(row['LongTermDebt']) if row['LongTermDebt'] is not None else None ,
            int(row['LongTermCapitalLeaseObligation']) if row['LongTermCapitalLeaseObligation'] is not None else None ,
            int(row['NonCurrentDeferredLiabilities']) if row['NonCurrentDeferredLiabilities'] is not None else None ,
            int(row['NonCurrentDeferredTaxesLiabilities']) if row['NonCurrentDeferredTaxesLiabilities'] is not None else None ,
            int(row['NonCurrentDeferredRevenue']) if row['NonCurrentDeferredRevenue'] is not None else None ,
            int(row['NonCurrentAccruedExpenses']) if row['NonCurrentAccruedExpenses'] is not None else None ,
            int(row['PreferredSecuritiesOutsideStockEquity']) if row['PreferredSecuritiesOutsideStockEquity'] is not None else None ,
            int(row['OtherNonCurrentLiabilities']) if row['OtherNonCurrentLiabilities'] is not None else None ,
            int(row['TotalEquityGrossMinorityInterest']) if row['TotalEquityGrossMinorityInterest'] is not None else None ,
            int(row['StockholdersEquity']) if row['StockholdersEquity'] is not None else None ,
            int(row['CapitalStock']) if row['CapitalStock'] is not None else None ,
            int(row['PreferredStock']) if row['PreferredStock'] is not None else None ,
            int(row['CommonStock']) if row['CommonStock'] is not None else None ,
            
            int(row['AdditionalPaidInCapital']) if row['AdditionalPaidInCapital'] is not None else None ,
            int(row['RetainedEarnings']) if row['RetainedEarnings'] is not None else None ,
            int(row['GainsLossesNotAffectingRetainedEarnings']) if row['GainsLossesNotAffectingRetainedEarnings'] is not None else None ,
            int(row['OtherEquityAdjustments']) if row['OtherEquityAdjustments'] is not None else None ,
            int(row['MinorityInterest']) if row['MinorityInterest'] is not None else None ,
            int(row['TotalCapitalization']) if row['TotalCapitalization'] is not None else None ,
            int(row['CommonStockEquity']) if row['CommonStockEquity'] is not None else None ,
            int(row['CapitalLeaseObligations']) if row['CapitalLeaseObligations'] is not None else None ,
            int(row['NetTangibleAssets']) if row['NetTangibleAssets'] is not None else None ,
            int(row['WorkingCapital']) if row['WorkingCapital'] is not None else None ,
            int(row['InvestedCapital']) if row['InvestedCapital'] is not None else None ,
            int(row['TangibleBookValue']) if row['TangibleBookValue'] is not None else None ,
            int(row['TotalDebt']) if row['TotalDebt'] is not None else None ,
            int(row['NetDebt']) if row['NetDebt'] is not None else None ,
            int(row['ShareIssued']) if row['ShareIssued'] is not None else None ,
            int(row['OrdinarySharesNumber']) if row['OrdinarySharesNumber'] is not None else None 
        ]

# Execute the query with the adapted values
        cur.execute(insert_query, values)