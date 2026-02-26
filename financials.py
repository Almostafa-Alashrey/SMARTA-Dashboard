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
st.markdown("**Edge AI Model: Raspberry Pi local inference with private cloud sync.**")

# Metrics Calculation
# Setup Profit: 45,000 - 35,000 = 10,000
# SaaS Profit (30%): 16,250 - 12,500 = 3,750
# Maintenance Profit: 6,000 - 1,200 = 4,800
# Total Year 1 Net Profit = 18,550
# Total Year 1 Revenue = 45,000 + 16,250 + 6,000 = 67,250

col_f1, col_f2, col_f3 = st.columns(3)
col_f1.metric(label="Year 1 Total Revenue", value="67,250 EGP")
col_f2.metric(label="Year 1 Net Profit", value="18,550 EGP")
col_f3.metric(label="Year 1 ROI", value="38.1%", delta="Client-Friendly Pricing")

st.markdown("<br>", unsafe_allow_html=True)

# Data Definition
fin_data = {
    "Category": ["Initial Setup & Hardware", "Annual SaaS", "Annual Maintenance"],
    "Our Cost (EGP)": [35000, 12500, 1200],
    "Client Price (EGP)": [45000, 16250, 6000]
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
    monthly_rev = (16250 / 12) + 500
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
    # Professional blue shades: Dark blue, Medium blue, Sky blue
    pie_data = pd.DataFrame({
        "Expense": ["Hardware Setup (72%)", "SaaS Infrastructure (26%)", "Maintenance (2%)"],
        "Amount (EGP)": [35000, 12500, 1200]
    })
    
    fig = px.pie(pie_data, values="Amount (EGP)", names="Expense", 
                 color_discrete_sequence=["#0D47A1", "#1976D2", "#42A5F5"],
                 hole=0.4)
    
    # Hide plotly toolbar for cleaner look
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