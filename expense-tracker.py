import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE_PATH = "expenses.csv"

# Initialing the CSV file if not exists
# This function creates a CSV file with the required columns if it doesn't exist.
def init_file():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["name", "amount", "category", "timestamp"])
        df.to_csv(FILE_PATH, index=False)

# Her e we Save expenses into the CSV file 
# (just for people who don't know meaning of csv it is "comma seperated values" it is the easiest and the best way to store values in key value pairs)

def save_expense(name, amount, category):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[name, amount, category, timestamp]],columns=["name", "amount", "category", "timestamp"])
    new_entry.to_csv(FILE_PATH, mode="a", header=not os.path.exists(FILE_PATH), index=False)

# Load all expenses
def load_expenses():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return pd.DataFrame(columns=["name", "amount", "category", "timestamp"])

# Summarize expenses
def summarize_expenses(df):
    total = df["amount"].sum()
    by_category = df.groupby("category")["amount"].sum()
    return total, by_category

# App UI
def main():
    st.set_page_config(page_title="💸 Expense Tracker", layout="centered")
    st.title("💸 Expense Tracker Web App")
    
    init_file()
    df = load_expenses()

    with st.form("expense_form"):
        st.subheader("Add a new expense")
        name = st.text_input("Expense Name")
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        category = st.selectbox("Category", ["Food", "Rent", "Travel", "Entertainment", "Utilities", "Other"])
        submitted = st.form_submit_button("Add Expense")

        if submitted and name and amount:
            save_expense(name, amount, category)
            st.success(f"Added: {name} – ₹{amount} [{category}]")
            df = load_expenses()

    st.divider()

    if not df.empty:
        st.subheader("📊 Summary")
        total, by_category = summarize_expenses(df)
        st.write(f"### Total Spent: ₹{total:.2f}")
        st.bar_chart(by_category)

        with st.expander("🧾 View All Expenses"):
            st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No expenses recorded yet.")

if __name__ == "__main__":
    main()
