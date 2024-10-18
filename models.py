from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
import json

def probe_model_5l_profit(data: dict):
    financial_index = latest_financial_index(data)
    
    total_revenue_5cr_flag_value = total_revenue_5cr_flag(data, financial_index)
    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(data, financial_index)
    iscr_flag_value = iscr_flag(data, financial_index)
    
    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }

if __name__ == "__main__":
    with open("data.json", "r") as file:
        content = file.read()
        data = json.loads(content)
        print(probe_model_5l_profit(data["data"]))
