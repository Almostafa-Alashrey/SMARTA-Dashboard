import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page setup
st.set_page_config(page_title="SMARTA Financials", layout="wide")

# Hide Streamlit UI elements for a professional look
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# =============================
# 1. BRANDING & METRICS
# =============================
st.markdown("<h1 style='color: #2196F3 !important;'>🧊 SMARTA Enterprise Analytics</h1>", unsafe_allow_html=True)
st.header("📈 Financial Projections (Per 100m² Unit)")
st.markdown("**Unit Economics for a standard 100-square-meter cold storage facility (One Client / First 12 Months).**")

# Top-level metrics calculation
# Initial Setup Profit: 60,000 - 45,000 = 15,000
# SaaS Profit: 25,000 - 12,500 = 12,500
# Maintenance Profit: 6,000 - 1,200 = 4,800
# Total Year 1 Net Profit = 32,300
# Total Year 1 Revenue = 60,000 + 25,000 + 6,000 = 91,000

col_f1, col_f2, col_f3 = st.columns(3)
col_f1.metric(label="Year 1 Total Revenue", value="91,000 EGP")
col_f2.metric(label="Year 1 Net Profit", value="32,300 EGP")
col_f3.metric(label="Year 1 ROI", value="55.0%", delta="Sustainable Growth")

st.markdown("<br>", unsafe_allow_html=True)

# Data Definition
fin_data = {
    "Category": ["Initial Setup & Hardware", "Annual SaaS", "Annual Maintenance"],
    "Our Cost (EGP)": [45000, 12500, 1200],
    "Client Price (EGP)": [60000, 25000, 6000]
}
df_fin = pd.DataFrame(fin_data)

# =============================
# 2. MAIN CHARTS (BAR & LINE)
# =============================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Cost vs. Revenue Breakdown")
    bar_data = df_fin.set_index("Category")
    st.bar_chart(bar_data, color=["#ff4b4b", "#2196F3"]) 

with col_chart2:
    st.subheader("12-Month Cumulative Cash Flow")
    months = np.arange(0, 13)
    monthly_rev = (25000 / 12) + 500  # Updated SaaS + Maintenance
    monthly_cost = 1040 + 100        # Server/SIM + Maintenance Cost
    
    cum_revenue = [60000 + (m * monthly_rev) for m in months]
    cum_costs = [45000 + (m * monthly_cost) for m in months]
    
    df_cashflow = pd.DataFrame({
        "Month": months,
        "Cumulative Revenue (EGP)": cum_revenue,
        "Cumulative Cost (EGP)": cum_costs
    }).set_index("Month")
    
    st.line_chart(df_cashflow, color=["#2196F3", "#ff4b4b"])

st.markdown("---")

# =============================
# 3. PIE CHART & DATA TABLE
# =============================
col_pie, col_table = st.columns(2)

with col_pie:
    st.subheader("Year 1 Investment Breakdown")
    # New Percentages: 45000/58700 = 76.6%, 12500/58700 = 21.3%, 1200/58700 = 2.1%
    pie_data = pd.DataFrame({
        "Expense": ["Initial Setup (77%)", "Server/SaaS (21%)", "Maintenance (2%)"],
        "Amount (EGP)": [45000, 12500, 1200]
    })
    
    fig = px.pie(pie_data, values="Amount (EGP)", names="Expense", 
                 color_discrete_sequence=["#ff4b4b", "#FF9800", "#FFC107"],
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.subheader("Detailed ROI Table")
    df_fin["Net Profit (EGP)"] = df_fin["Client Price (EGP)"] - df_fin["Our Cost (EGP)"]
    df_fin["Profit Margin (%)"] = round((df_fin["Net Profit (EGP)"] / df_fin["Client Price (EGP)"]) * 100, 1)
    
    total_cost = df_fin["Our Cost (EGP)"].sum()
    total_price = df_fin["Client Price (EGP)"].sum()
    total_profit = df_fin["Net Profit (EGP)"].sum()
    total_margin = round((total_profit / total_price) * 100, 1)
    
    total_row = pd.DataFrame([{
        "Category": "TOTAL (Year 1)",
        "Our Cost (EGP)": total_cost,
        "Client Price (EGP)": total_price,
        "Net Profit (EGP)": total_profit,
        "Profit Margin (%)": total_margin
    }])
    
    df_fin_with_total = pd.concat([df_fin, total_row], ignore_index=True)
    df_fin_with_total.index += 1
    st.dataframe(df_fin_with_total, use_container_width=True)