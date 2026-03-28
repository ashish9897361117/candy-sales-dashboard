import streamlit as st
import pandas as pd
import plotly.express as px


st.caption("Created by Ashish | Data Analyst Project")
st.markdown("---")


st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Nassau Candy Sales Dashboard")

# Load Data
pd.read_csv(r"Nassau Candy Distributor.csv")


# Create Profit Margin
df["Profit Margin"] = df["Gross Profit"] / df["Sales"]

st.dataframe(df.head())


#KPI Cards


total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Profit Margin"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg Profit Margin", f"{avg_margin:.2%}")

#Sidebar Filters

st.sidebar.header("Filters")

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

filtered_df = df[df["Division"].isin(division)]


#Best Division Charts 

division_profit = filtered_df.groupby("Division")["Gross Profit"].sum().reset_index()

fig1 = px.bar(
    division_profit,
    x="Division",
    y="Gross Profit",
    title="Profit by Division"
)

st.plotly_chart(fig1, use_container_width=True)

#High Sales vs Low Profit (Scatter Plot)

fig2 = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross Profit",
    color="Division",
    hover_data=["Product Name"],
    title="Sales vs Profit Analysis"
)

st.plotly_chart(fig2, use_container_width=True)


#Worst Margin Products Table

worst_products = (
    filtered_df.groupby("Product Name")["Profit Margin"]
    .mean()
    .sort_values()
    .head(10)
)

st.subheader("⚠️ Lowest Margin Products")
st.dataframe(worst_products)


#Profit Dependency Charts

top_products = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="Product Name",
    y="Gross Profit",
    title="Top Profit Contributing Products"
)

st.plotly_chart(fig3, use_container_width=True)


