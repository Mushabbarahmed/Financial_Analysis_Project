import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # For display purposes
    WHITE = 4  # Data missing

# Latest financial index function
def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

# Total revenue calculation
def total_revenue(data: dict, financial_index):
    return data["financials"][financial_index]["pnl"]["lineItems"]["net_revenue"]

# Total borrowings calculation
def total_borrowing(data: dict, financial_index):
    borrowings = (data["financials"][financial_index]["bs"]["liabilities"]["long_term_borrowings"]
                 + data["financials"][financial_index]["bs"]["liabilities"]["short_term_borrowings"])
    revenue = total_revenue(data, financial_index)
    return borrowings / revenue if revenue else 0

# ISCR (Interest Service Coverage Ratio) calculation
def iscr(data: dict, financial_index):
    financial = data["financials"][financial_index]
    profit_before_tax = financial["pnl"]["lineItems"]["profit_before_interest_and_tax"]
    depreciation = financial["pnl"]["lineItems"]["depreciation"]
    interest = financial["pnl"]["lineItems"].get("interest", 1)
    return (profit_before_tax + depreciation + 1) / (interest + 1)

# Flag for ISCR
def iscr_flag(data: dict, financial_index):
    ratio = iscr(data, financial_index)
    return FLAGS.GREEN if ratio >= 2 else FLAGS.RED

# Flag for total revenue exceeding 50 million
def total_revenue_5cr_flag(data: dict, financial_index):
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED

# Borrowing to revenue ratio flag
def borrowing_to_revenue_flag(data: dict, financial_index):
    ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
