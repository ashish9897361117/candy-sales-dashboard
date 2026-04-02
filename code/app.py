import streamlit as st
import pandas as pd
import plotly.express as px
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    transition: 0.3s;
}
.kpi-card:hover {
    transform: scale(1.05);
}
.kpi-title {
    font-size: 16px;
    opacity: 0.8;
}
.kpi-value {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🍬 Nassau Candy Sales Performance Dashboard")
st.caption("Interactive Business Intelligence & Profitability Analysis")


st.set_page_config(page_title="Sales Dashboard", layout="wide")



st.markdown("## 📌 Executive Insights")

st.info("""
✅ Top products generate majority of total profit.

✅ Some high-sales products have low profit margins,
indicating pricing or cost inefficiencies.

✅ Division performance shows uneven profitability distribution.

✅ Business profit depends heavily on a few key products (Pareto effect).
    
""")


# Load Data
import time
import streamlit as st
import pandas as pd

with st.spinner("📊 Loading dashboard data..."):
    time.sleep(3)   # 👈 test delay
    df = pd.read_csv(r"Data/Nassau Candy Distributor.csv")

st.success("Loaded!")



# Create Profit Margin
df["Profit Margin"] = df["Gross Profit"] / df["Sales"]

st.dataframe(df.head())


#KPI Cards
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Profit Margin"].mean()
gross_margin = total_profit / total_sales

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg Margin", f"{avg_margin:.2%}")
col4.metric("Gross Margin", f"{gross_margin:.2%}")


st.markdown("## 📌 Key Business Insights")

st.markdown("""
### 1️⃣ Revenue Growth Trend
Business revenue shows noticeable variation across different time periods,
indicating seasonal demand patterns and peak sales opportunities.

### 2️⃣ Top Performing Products
A small group of products contributes the majority of total revenue and profit.
Focusing marketing and inventory on these products can maximize returns.

### 3️⃣ Profitability Analysis
High sales volume does not always mean high profit. Some products generate
lower margins, suggesting pricing or cost optimization opportunities.

### 4️⃣ Customer Purchase Behavior
Customers show repeat buying patterns in certain categories, indicating
strong preferences and potential for loyalty programs.

### 5️⃣ Regional / Segment Performance
Sales performance varies across regions and customer segments, highlighting
areas for targeted marketing strategies.

### 6️⃣ Margin Volatility
Profit margins fluctuate due to discounts, operational costs, and product mix.
Regular monitoring helps maintain stable profitability.

### 7️⃣ Business Optimization Opportunity
Shifting focus toward high-margin products and reducing low-profit dependency
can improve overall business efficiency.
""")


#MODULE 1 — Product Profitability Overview
# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Product Profitability",
    "🏢 Division Performance",
    "⚙️ Cost vs Margin",
    "💰 Profit Concentration"
])

# ---------------- MODULE 1 ----------------

with tab1:

    st.subheader("🏆 Product Margin Leaderboard")

    leaderboard = (
        df.groupby("Product Name")[["Sales","Gross Profit","Profit Margin"]]
        .mean()
        .sort_values("Profit Margin", ascending=False)
        .reset_index()
    )

    st.dataframe(leaderboard.head(10))

import plotly.express as px

profit_contribution = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    profit_contribution,
    x="Product Name",
    y="Gross Profit",
    title="Top Profit Contributing Products"
)

st.plotly_chart(fig, use_container_width=True, key ="charts1")

#MODULE 2 — Division Performance Dashboard
with tab2:

    st.subheader("Revenue vs Profit by Division")

    division_perf = (
        df.groupby("Division")[["Sales","Gross Profit"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        division_perf,
        x="Division",
        y=["Sales","Gross Profit"],
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True, key ="charts2" )

#Margin Distribution
fig2 = px.box(
    df,
    x="Division",
    y="Profit Margin",
    title="Margin Distribution by Division"
)

st.plotly_chart(fig2, use_container_width=True , key ="charts3")

#MODULE 3 — Cost vs Margin Diagnostics

with tab3:

    st.subheader("Cost vs Sales Diagnostics")

    fig3 = px.scatter(
        df,
        x="Sales",
        y="Gross Profit",
        color="Division",
        hover_data=["Product Name"]
    )

    st.plotly_chart(fig3, use_container_width=True, key ="charts4")
#Margin risk Flags

risk_products = df[df["Profit Margin"] < 0.1]

st.warning("⚠️ Low Margin Risk Products")
st.dataframe(risk_products[["Product Name","Profit Margin"]])


#MODULE 4 — Profit Concentration Analysis

with tab4:

    pareto = (
        df.groupby("Product Name")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

pareto["Cumulative Profit %"] = (
    pareto["Gross Profit"].cumsum()
    / pareto["Gross Profit"].sum()
)
with tab4:

    pareto = (
        df.groupby("Product Name")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

pareto["Cumulative Profit %"] = (
    pareto["Gross Profit"].cumsum()
    / pareto["Gross Profit"].sum()
)


st.markdown("## 🎯 Business Recommendations")

st.success("""
• Optimize pricing for low-margin products
• Focus on top profit contributors
• Reduce cost-heavy inventory
""")



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

st.plotly_chart(fig1, use_container_width=True, key ="charts5")

#High Sales vs Low Profit (Scatter Plot)

fig2 = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross Profit",
    color="Division",
    hover_data=["Product Name"],
    title="Sales vs Profit Analysis"
)

st.plotly_chart(fig2, use_container_width=True, key ="charts6")


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

st.plotly_chart(fig3, use_container_width=True, key ="charts7")


#About Section

st.markdown("---")

st.markdown("""
## 📘 About This Dashboard

The **Nassau Candy Sales Analytics Dashboard** is an interactive business intelligence application 
designed to analyze sales performance, profitability trends, and operational efficiency across 
products and divisions.

This dashboard transforms raw transactional data into actionable insights by combining 
data analysis with intuitive visualizations. It helps identify high-performing products, 
margin risks, and profit concentration patterns to support data-driven business decisions.

### 🔍 Key Capabilities
- Product-level profitability analysis
- Division performance comparison
- Cost vs margin diagnostics
- Profit concentration (Pareto) analysis
- Interactive filtering and visualization

### 🛠️ Technology Stack
**Python • Pandas • Plotly • Streamlit**

### 👨‍💻 Developed By
**Ashish Kushwah**  
Data Analytics & Business Intelligence Enthusiast

---
*Built as an end-to-end data analytics project — from data cleaning and analysis to dashboard design and cloud deployment.*
""")

