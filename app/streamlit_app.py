import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Churn Intelligence System", layout="wide")

@st.cache_resource
def load_model():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'best_model_v1.pkl')

    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

st.markdown("""
    <div style='background-color:#1F3864; padding:20px; border-radius:8px;'>
        <h1 style='color:white; margin:0;'>Churn Intelligence System</h1>
        <p style='color:#D0DCF5; margin:0;'>Real-time customer churn risk scorer</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

st.sidebar.header("Customer Attributes")
monthly_revenue = st.sidebar.slider("Monthly Revenue ($)", 0.0, 500.0, 55.0)
monthly_minutes = st.sidebar.slider("Monthly Minutes", 0, 3000, 500)
current_equipment_days = st.sidebar.slider("Equipment Age (days)", 0, 2000, 365)
customer_care_calls = st.sidebar.slider("Customer Care Calls", 0, 50, 2)
overage_minutes = st.sidebar.slider("Overage Minutes", 0, 1000, 50)
perc_change_minutes = st.sidebar.slider("Percent Change in Minutes", -100, 100, 0)
months_in_service = st.sidebar.slider("Months in Service", 0, 100, 24)
made_retention_call = st.sidebar.selectbox("Made Retention Call?", ["No", "Yes"])

score_button = st.sidebar.button("Score This Customer", type="primary")

col1, col2 = st.columns([1, 1])

if score_button:
    base_prob = 0.15
    if current_equipment_days > 600:
        base_prob += 0.20
    if perc_change_minutes < -30:
        base_prob += 0.15
    if made_retention_call == "Yes":
        base_prob += 0.20
    if customer_care_calls == 0:
        base_prob += 0.10
    if months_in_service > 24:
        base_prob += 0.10
    churn_prob = min(base_prob, 0.95)

    if churn_prob >= 0.60:
        tier, color = "Critical", "#A32D2D"
    elif churn_prob >= 0.40:
        tier, color = "High", "#854F0B"
    elif churn_prob >= 0.25:
        tier, color = "Watch", "#185FA5"
    else:
        tier, color = "Low", "#3B6D11"

    with col1:
        st.subheader("Churn Risk Score")
        st.markdown(f"""
            <div style='background-color:{color}20; border-left:4px solid {color};
                        padding:20px; border-radius:8px;'>
                <h2 style='color:{color}; margin:0;'>{churn_prob*100:.1f}%</h2>
                <p style='margin:0;'>Churn Probability</p>
                <p style='margin-top:10px; font-weight:bold; color:{color};'>
                    Risk Tier: {tier}
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.subheader("Recommended Action")
        actions = {
            "Critical": "Personal outreach within 48 hours plus retention offer",
            "High": "Automated retention offer within 7 days",
            "Watch": "Loyalty nudge within 14 days",
            "Low": "No action required"
        }
        st.info(actions[tier])

    with col2:
        st.subheader("Why This Score?")
        st.write("Key contributing risk factors:")
        factors = []
        if current_equipment_days > 600:
            factors.append("Equipment age exceeds 600 days, staleness risk")
        if perc_change_minutes < -30:
            factors.append("Usage dropped significantly, engagement decay")
        if made_retention_call == "Yes":
            factors.append("Already contacted retention team, distress signal")
        if customer_care_calls == 0:
            factors.append("Zero complaints, possible silent churner")
        if months_in_service > 24:
            factors.append("Long tenure, equipment contract cliff risk")
        if not factors:
            factors.append("No major risk factors detected")
        for f in factors:
            st.write("- " + f)
else:
    st.info("Adjust customer attributes in the sidebar and click Score This Customer")

st.write("---")
st.caption("Churn Intelligence System | Cell2Cell Dataset | Yash Chavan | VIT Pune 2026")