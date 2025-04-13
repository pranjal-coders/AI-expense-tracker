import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

FILE_PATH = "expenses.csv"
USERNAME = "admin"
PASSWORD = "admin123"  # You can later use env variables for safety

# ---------------------------- Initialising the csv fiel ----------------------------
def init_file():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["name", "amount", "category", "timestamp"])
        df.to_csv(FILE_PATH, index=False)

# ---------------------------- Function to save load and summarise the expenses  ----------------------------
def save_expense(name, amount, category):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[name, amount, category, timestamp]],
                             columns=["name", "amount", "category", "timestamp"])
    new_entry.to_csv(FILE_PATH, mode="a", header=not os.path.exists(FILE_PATH), index=False)

def load_expenses():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return pd.DataFrame(columns=["name", "amount", "category", "timestamp"])

def summarize_expenses(df):
    total = df["amount"].sum()
    by_category = df.groupby("category")["amount"].sum().reset_index()
    return total, by_category

# ----------------------------- Hardcoded Authorisation ----------------------------
def login():
    st.title("🔐 Login to Expense Tracker")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username == USERNAME and password == PASSWORD:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# ----------------------------- The main app ----------------------------
def main_app():
    st.title("💸 Expense Tracker Web App")
    init_file()
    df = load_expenses()

    with st.form("expense_form"):
        st.subheader("Add a new expense")
        name = st.text_input("Expense Name")
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        category = st.selectbox("Category", ["Food", "Rent", "Travel", "Entertainment", "Utilities", "Other"])
        submitted = st.form_submit_button("Add Expense")

        if submitted and name:
            save_expense(name, amount, category)
            st.success(f"Added: {name} – ₹{amount} [{category}]")
            df = load_expenses()

    st.divider()

    if not df.empty:
        st.subheader("📊 Summary")
        total, by_category = summarize_expenses(df)
        st.markdown(f"### Total Spent: ₹{total:.2f}")

        # Chart selection
        chart_type = st.selectbox("Choose chart type", ["Bar", "Pie", "Donut", "Line"])

        if chart_type == "Bar":
            fig = px.bar(by_category, x="category", y="amount", color="category", title="Expenses by Category")
        elif chart_type == "Pie":
            fig = px.pie(by_category, names="category", values="amount", title="Expenses Distribution")
        elif chart_type == "Donut":
            fig = px.pie(by_category, names="category", values="amount", hole=0.4, title="Expenses (Donut Chart)")
        elif chart_type == "Line":
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df_sorted = df.sort_values("timestamp")
            fig = px.line(df_sorted, x="timestamp", y="amount", color="category", title="Spending Over Time")

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🧾 View All Expenses"):
            st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No expenses recorded yet.")

# ----------------------------- Run app the main function ----------------------------
def main():
    st.set_page_config(page_title="💸 Expense Tracker", layout="centered")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login()
    else:
        main_app()

if __name__ == "__main__":
    main()
# This code is a simple expense tracker web app using Streamlit and Plotly for visualization.