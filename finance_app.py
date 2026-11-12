import streamlit as st
import boto3
import pandas as pd
import plotly.express as px
import uuid
import os
from decimal import Decimal

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL", "http://host.minikube.internal:4566")

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)
table = dynamodb.Table("FinanceTransactions")

st.set_page_config(page_title="FinanceFlow Dashboard", layout="wide")
st.title("Personal Finance Dashboard (AWS DynamoDB)")

with st.sidebar:
    st.header("Add Transaction")
    t_type = st.selectbox("Type", ["Expense", "Income"])
    category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Salary", "Entertainment", "Other"])
    amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
    date = st.date_input("Date")
    if st.button("Save Transaction"):
        table.put_item(Item={
            "id": str(uuid.uuid4()),
            "type": t_type,
            "category": category,
            "amount": Decimal(str(amount)),
            "date": str(date)
        })
        st.success("Saved to AWS DynamoDB!")

response = table.scan()
data = response.get("Items", [])

if data:
    df = pd.DataFrame(data)
    df["amount"] = df["amount"].astype(float)
    
    c1, c2, c3 = st.columns(3)
    inc = df[df["type"] == "Income"]["amount"].sum()
    exp = df[df["type"] == "Expense"]["amount"].sum()
    c1.metric("Total Income", f"${inc:,.2f}")
    c2.metric("Total Expenses", f"${exp:,.2f}")
    c3.metric("Net Balance", f"${(inc - exp):,.2f}")

    exp_df = df[df["type"] == "Expense"]
    if not exp_df.empty:
        st.plotly_chart(px.pie(exp_df, values="amount", names="category", hole=0.4), use_container_width=True)
    st.dataframe(df[["date", "type", "category", "amount"]], use_container_width=True)
else:
    st.info("No transactions yet. Add one from the sidebar.")
