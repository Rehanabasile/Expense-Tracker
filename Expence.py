import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read the existing expense data or create an empty DataFrame
try:
    data = pd.read_csv("Expense_Data.csv")
except FileNotFoundError:
    data = pd.DataFrame(columns=["Date", "Category", "Amount"])

st.title("Daily Expense Tracker")
nav = st.sidebar.radio("Navigation", ["Home", "Add Expense", "View Expenses"])

if nav == "Home":
    image_url = "your-new-salary-iStockphoto.jpg"
    st.image(image_url, width=500)
if nav == "Add Expense":
    st.header("Add Your Daily Expense")
    date = st.date_input("Date", pd.Timestamp.today())
    category = st.selectbox("Category", ["Food", "Transportation", "Entertainment", "Other"])
    amount = st.number_input("Amount", 0.00, 100000.00, step=10.00)
    
if st.button("Add Expense"):
        new_expense = {"Date": date, "Category": category, "Amount": amount}
        new_expense_df = pd.DataFrame([new_expense])  # Convert dictionary to DataFrame
        data = pd.concat([data, new_expense_df], ignore_index=True)  # Concatenate existing and new data
        data.to_csv("Expense_Data.csv", mode='a', header=False, index=False)
        st.success("Expense added successfully!")


if nav == "View Expenses":
    st.header("View Your Expenses")
    category_filter = st.selectbox("Filter by Category", ["All"] + data["Category"].unique().tolist())
    
    if category_filter == "All":
        filtered_data = data
    else:
        filtered_data = data[data["Category"] == category_filter]
    
    st.dataframe(filtered_data)
    
    # Bar chart to visualize expenses by category
    expenses_by_category = filtered_data.groupby("Category")["Amount"].sum()
    plt.figure(figsize=(10, 6))
    plt.bar(expenses_by_category.index, expenses_by_category.values)
    plt.xlabel("Category")
    plt.ylabel("Total Expense Amount")
    plt.title("Expenses by Category")
    st.pyplot(plt)

st.sidebar.text("Manage your daily expenses efficiently!")
