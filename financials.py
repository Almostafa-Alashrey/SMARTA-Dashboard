import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page setup
st.set_page_config(page_title="SMARTA Financials", layout="wide")

# Hide Streamlit UI elements
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
st.markdown("**Edge AI Model: Raspberry Pi local inference with a 30% SaaS profit margin target.**")

# Metrics Calculation
# Setup Profit: 45,000 - 35,000 = 10,000
# SaaS Profit (30% of 17,850): 17,850 - 12,500 = 5,350
# Maintenance Profit: 6,000 - 1,200 = 4,800
# Total Year 1 Net Profit = 20,150
# Total Year 1 Revenue = 45,000 + 17,850 + 6,000 = 68,850

col_f1, col_f2, col_f3 = st.columns(3)
col_f1.metric(label="Year 1 Total Revenue", value="68,850 EGP")
col_f2.metric(label="Year 1 Net Profit", value="20,150 EGP")
col_f3.metric(label="Year 1 ROI", value="41.4%", delta="Target 30% SaaS Margin")

st.markdown("<br>", unsafe_allow_html=True)

# Data Definition
fin_data = {
    "Category": ["Initial Setup & Hardware", "Annual SaaS", "Annual Maintenance"],
    "Our Cost (EGP)": [35000, 12500, 1200],
    "Client Price (EGP)": [45000, 17850, 6000] # Price adjusted for true 30% margin
}
df_fin = pd.DataFrame(fin_data)

# =============================
# 2. MAIN CHARTS (BAR & LINE)
# =============================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Cost vs. Revenue Breakdown")
    bar_data = df_fin.set_index("Category")
    st.bar_chart(bar_data, color=["#1E88E5", "#64B5F6"]) 

with col_chart2:
    st.subheader("12-Month Cumulative Cash Flow")
    months = np.arange(0, 13)
    monthly_rev = (17850 / 12) + 500
    monthly_cost = 1040 + 100 
    
    cum_revenue = [45000 + (m * monthly_rev) for m in months]
    cum_costs = [35000 + (m * monthly_cost) for m in months]
    
    df_cashflow = pd.DataFrame({
        "Month": months,
        "Cumulative Revenue (EGP)": cum_revenue,
        "Cumulative Cost (EGP)": cum_costs
    }).set_index("Month")
    
    st.line_chart(df_cashflow, color=["#1565C0", "#E53935"])

st.markdown("---")

# =============================
# 3. PIE CHART & DATA TABLE
# =============================
col_pie, col_table = st.columns(2)

with col_pie:
    st.subheader("Year 1 Cost Distribution")
    pie_data = pd.DataFrame({
        "Expense": ["Hardware Setup (72%)", "SaaS Infrastructure (26%)", "Maintenance (2%)"],
        "Amount (EGP)": [35000, 12500, 1200]
    })
    
    fig = px.pie(pie_data, values="Amount (EGP)", names="Expense", 
                 color_discrete_sequence=["#0D47A1", "#1976D2", "#42A5F5"],
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_table:
    st.subheader("ROI Detail Table")
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