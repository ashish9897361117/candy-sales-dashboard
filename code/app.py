import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Candy Sales Analytics Dashboard",
    page_icon="🍬",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    padding: 25px;
    border-radius: 12px;
    color: white;
    text-align: center;
}
.sub-text {
    font-size: 18px;
    margin-top: 8px;
}
.module-box {
    background-color: #black;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="main-header">
    <h1>🍬 Nassau Candy Sales Performance Dashboard</h1>
    <p class="sub-text">
        Advanced Business Analytics using Streamlit | Profitability • Cost Analysis • Performance Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

colh1, colh2, colh3, colh4 = st.columns(4)

with colh1:
    st.markdown("""
    <div class="module-box">
        <h4>📈 Product Profitability</h4>
        <p>Margin leaderboard & profit contribution analysis</p>
    </div>
    """, unsafe_allow_html=True)

with colh2:
    st.markdown("""
    <div class="module-box">
        <h4>🏢 Division Performance</h4>
        <p>Revenue vs Profit comparison & margin distribution</p>
    </div>
    """, unsafe_allow_html=True)

with colh3:
    st.markdown("""
    <div class="module-box">
        <h4>⚙️ Cost Diagnostics</h4>
        <p>Cost vs Sales insights & margin risk detection</p>
    </div>
    """, unsafe_allow_html=True)

with colh4:
    st.markdown("""
    <div class="module-box">
        <h4>💰 Profit Concentration</h4>
        <p>Pareto analysis & dependency indicators</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()



# ================= DATA LOADING =================
with st.spinner("📊 Loading dashboard data..."):
    df = pd.read_csv("Data/Nassau Candy Distributor.csv")
    df["Profit Margin"] = df["Gross Profit"] / df["Sales"]

# ================= SIDEBAR FILTERS =================
st.sidebar.title("🍬 Candy Analytics")
st.sidebar.caption("Interactive Business Intelligence")
st.sidebar.markdown("---")

division_options = sorted(df["Division"].dropna().unique())
selected_divisions = st.sidebar.multiselect(
    "🏢 Select Division",
    division_options,
    default=division_options
)

filtered_df = df[df["Division"].isin(selected_divisions)].copy()

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing {len(filtered_df):,} rows")

# ================= KPI SECTION =================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
avg_margin = filtered_df["Profit Margin"].mean()
gross_margin = total_profit / total_sales if total_sales != 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Avg Margin", f"{avg_margin:.2%}")
col4.metric("🔥 Gross Margin", f"{gross_margin:.2%}")

# ================= KEY BUSINESS INSIGHTS =================
st.markdown("## 📌 Key Business Insights")

st.info("""
🔎 **Profit Concentration:**  
A small group of products contributes a significant share of total profit, indicating a Pareto-like distribution.

📊 **Margin Imbalance:**  
Some products generate high sales revenue but operate with relatively low profit margins, suggesting pricing or cost optimization opportunities.

🏢 **Division Performance Variation:**  
Profitability differs across divisions, highlighting uneven operational efficiency and potential areas for performance improvement.

⚠️ **Margin Risk Areas:**  
Low-margin products may expose the business to profitability risks if costs increase or pricing pressure occurs.

📈 **Growth Opportunity:**  
Focusing on high-margin and consistently profitable products can improve overall business profitability and resource allocation.
""")

# ================= RISK ALERTS =================
low_margin_products = filtered_df[filtered_df["Profit Margin"] < 0.10]
st.error(f"⚠️ {len(low_margin_products)} products/orders fall into the low-margin risk zone.")

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Product Profitability",
    "🏢 Division Performance",
    "⚙️ Cost vs Margin",
    "💰 Profit Concentration"
])

# ================= MODULE 1 — PRODUCT PROFITABILITY =================
with tab1:
    st.subheader("🏆 Product Margin Leaderboard")

    leaderboard = (
        filtered_df.groupby("Product Name")[["Sales", "Gross Profit", "Profit Margin"]]
        .mean()
        .sort_values("Profit Margin", ascending=False)
        .reset_index()
    )

    st.dataframe(leaderboard.head(10), use_container_width=True)

    st.subheader("💵 Top Profit Contributing Products")

    profit_contribution = (
        filtered_df.groupby("Product Name")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(
        profit_contribution,
        x="Product Name",
        y="Gross Profit",
        title="Top Profit Contributing Products"
    )
    st.plotly_chart(fig1, use_container_width=True)

# ================= MODULE 2 — DIVISION PERFORMANCE =================
with tab2:
    st.subheader("🏢 Revenue vs Profit by Division")

    division_perf = (
        filtered_df.groupby("Division")[["Sales", "Gross Profit"]]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        division_perf,
        x="Division",
        y=["Sales", "Gross Profit"],
        barmode="group",
        title="Revenue vs Profit Comparison by Division"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📦 Margin Distribution by Division")

    fig3 = px.box(
        filtered_df,
        x="Division",
        y="Profit Margin",
        title="Margin Distribution by Division"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ================= MODULE 3 — COST VS MARGIN =================
with tab3:
    st.subheader("⚙️ Cost vs Sales Scatter Plot")

    fig4 = px.scatter(
        filtered_df,
        x="Cost",
        y="Sales",
        color="Division",
        hover_data=["Product Name"],
        title="Cost vs Sales Diagnostics"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("⚠️ Low Margin Risk Products")

    risk_table = (
        filtered_df.groupby("Product Name")[["Sales", "Gross Profit", "Profit Margin"]]
        .mean()
        .sort_values("Profit Margin", ascending=True)
        .reset_index()
    )

    st.dataframe(risk_table.head(10), use_container_width=True)

# ================= MODULE 4 — PROFIT CONCENTRATION =================
with tab4:
    st.subheader("💰 Pareto Analysis")

    pareto = (
        filtered_df.groupby("Product Name")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    pareto["Cumulative Profit %"] = pareto["Gross Profit"].cumsum() / pareto["Gross Profit"].sum()

    fig5 = px.line(
        pareto.head(20),
        x="Product Name",
        y="Cumulative Profit %",
        title="Profit Concentration (Pareto Analysis)"
    )
    st.plotly_chart(fig5, use_container_width=True)

    top3_share = pareto.head(3)["Gross Profit"].sum() / pareto["Gross Profit"].sum()
    st.metric("🎯 Top 3 Products Profit Dependency", f"{top3_share:.2%}")

# ================= RECOMMENDATIONS =================
st.markdown("## 🎯 Business Recommendations")

st.success("""
• Optimize pricing strategy for low-margin, high-sales products.  
• Focus promotions and inventory planning on top profit-contributing products.  
• Monitor divisions with unstable margins for operational improvement.  
• Reduce dependence on a few products by strengthening mid-performing items.  
""")

# ================= ABOUT SECTION =================
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
**Ashish**  
Data Analytics & Business Intelligence Enthusiast

---
*Built as an end-to-end data analytics project — from data cleaning and analysis to dashboard design and cloud deployment.*
""")

st.caption("© 2026 Ashish | Data Analytics Portfolio Project")
