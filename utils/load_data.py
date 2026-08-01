import pandas as pd

def load_data():

    customers = pd.read_csv("customers.csv")
    products = pd.read_csv("products.csv")
    partners = pd.read_csv("partners.csv")
    transactions = pd.read_csv("transactions.csv")
    funnel = pd.read_csv("funnel_events.csv")

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"]
    )

    funnel["event_date"] = pd.to_datetime(
        funnel["event_date"]
    )

    return (
        customers,
        products,
        partners,
        transactions,
        funnel
    )