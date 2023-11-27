variables = [
    "TotalRevenue",
    "CostOfGoodsSoldInclDA",
    "GrossProfit",
    "SellingGeneralAdministrativeExclOther",
    "OtherOperatingExpense",
    "OperatingIncome",
    "InterestExpense",
    "UnusualExpense",
    "NetIncomeBeforeTaxes",
    "IncomeTaxes",
    "ConsolidatedNetIncome",
    "EPSRecurring",
    "EPSBasicBeforeExtraordinaries",
    "EPSDiluted",
    "EBITDA",
    "PriceToEarningsRatio",
    "PriceToSalesRatio",
    "GrossMargin",
    "OperatingMargin",
    "NetMargin",
    "SharesOutstanding",
    "MarketCapitalization"
]

formatted_variables = [f"row['{variable}']," for variable in variables]
print(formatted_variables)
# This will result in a list of variables in the desired format
