import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

random.seed(42)


# -----------------------------
# 1. PRODUCTS TABLE
# -----------------------------

products = pd.DataFrame({
    "product_id": [
        "PR01","PR02","PR03","PR04",
        "PR05","PR06","PR07","PR08"
    ],
    "product_name": [
        "BNPL",
        "Credit Card",
        "Personal Loan",
        "Health Insurance",
        "Digital Wallet",
        "EMI Financing",
        "Rewards Plus",
        "Investment Lite"
    ],
    "category": [
        "Lending",
        "Credit",
        "Lending",
        "Protection",
        "Payments",
        "Lending",
        "Loyalty",
        "Wealth"
    ]
})


products.to_csv(
    "products.csv",
    index=False
)


# -----------------------------
# 2. PARTNERS TABLE
# -----------------------------

partner_names = [
    "Flipkart",
    "Myntra",
    "Amazon India",
    "Swiggy",
    "Zomato",
    "MakeMyTrip",
    "OYO",
    "BigBasket",
    "Zepto",
    "Croma",
    "Reliance Digital",
    "Nykaa",
    "Urban Company",
    "BookMyShow",
    "Cult Fit",
    "PolicyBazaar",
    "PharmEasy",
    "Apollo 24/7",
    "Tata Neu",
    "Pine Labs"
]


industries = [
    "Ecommerce",
    "Fashion",
    "Food Delivery",
    "Travel",
    "Healthcare",
    "Retail",
    "Payments"
]


partners = pd.DataFrame({
    "partner_id":[f"P{i:02}" for i in range(1,21)],
    "partner_name":partner_names,
    "industry":[random.choice(industries) for _ in range(20)]
})


partners.to_csv(
    "partners.csv",
    index=False
)



# -----------------------------
# 3. CUSTOMERS TABLE
# -----------------------------

cities=[
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Gurgaon"
]


customers=[]


for i in range(1,501):

    signup_date = (
        datetime(2025,1,1)
        +
        timedelta(days=random.randint(0,300))
    )


    customers.append([
        f"C{i:03}",
        signup_date.date(),
        random.choice(cities),
        random.choices(
            ["18-24","25-34","35-44","45-54"],
            weights=[20,40,30,10]
        )[0],

        random.choices(
            ["Low","Medium","High"],
            weights=[25,55,20]
        )[0],

        random.choice(
            [
                "Organic",
                "Referral",
                "Partner",
                "Social Media",
                "Paid Ads"
            ]
        )
    ])


customers=pd.DataFrame(
    customers,
    columns=[
        "customer_id",
        "signup_date",
        "city",
        "age_group",
        "income_segment",
        "acquisition_channel"
    ]
)


customers.to_csv(
    "customers.csv",
    index=False
)



# -----------------------------
# 4. TRANSACTIONS TABLE
# -----------------------------


product_weights=[
    20, # BNPL
    15, # Card
    7,  # Loan
    8,  # Insurance
    30, # Wallet
    12, # EMI
    5,  # Rewards
    3   # Investment
]


margin={
"PR01":0.03,
"PR02":0.025,
"PR03":0.05,
"PR04":0.04,
"PR05":0.02,
"PR06":0.035,
"PR07":0.015,
"PR08":0.02
}


transactions=[]


for i in range(1,2501):

    product=random.choices(
        products.product_id,
        weights=product_weights
    )[0]


    amount=random.randint(
        500,
        50000
    )


    revenue=round(
        amount*margin[product],
        2
    )


    transactions.append([

        f"T{i:05}",

        random.choice(
            customers.customer_id.tolist()
        ),

        random.choice(
            partners.partner_id.tolist()
        ),

        product,


        (
        datetime(2025,1,1)
        +
        timedelta(days=random.randint(0,365))
        ).date(),


        amount,

        revenue,


        random.choices(
            ["Yes","No"],
            weights=[60,40]
        )[0],


        random.choices(
            ["Yes","No"],
            weights=[25,75]
        )[0],


        random.choices(
            ["Success","Failed","Pending"],
            weights=[85,10,5]
        )[0]

    ])



transactions=pd.DataFrame(
    transactions,
    columns=[
        "transaction_id",
        "customer_id",
        "partner_id",
        "product_id",
        "transaction_date",
        "amount",
        "revenue",
        "is_repeat",
        "cross_sell",
        "status"
    ]
)



transactions.to_csv(
    "transactions.csv",
    index=False
)



# -----------------------------
# 5. FUNNEL EVENTS TABLE
# -----------------------------


stages = [
    "Viewed",
    "Application Started",
    "KYC Completed",
    "Approved",
    "Activated",
    "First Transaction"
]

events = []

for i in range(1, 2001):

    # Select a real customer-product combination
    txn = transactions.sample(1).iloc[0]

    customer = txn["customer_id"]
    product = txn["product_id"]

    stage = random.choice(stages)

    event_date = (
        pd.to_datetime(txn["transaction_date"])
        - timedelta(days=random.randint(0, 5))
    ).date()

    events.append([
        f"E{i:05}",
        customer,
        product,
        stage,
        event_date
    ])

funnel = pd.DataFrame(
    events,
    columns=[
        "event_id",
        "customer_id",
        "product_id",
        "stage",
        "event_date"
    ]
)

funnel.to_csv(
    "funnel_events.csv",
    index=False
)

print("Dataset generation completed successfully!")