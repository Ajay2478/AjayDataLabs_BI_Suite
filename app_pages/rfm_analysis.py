import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.title("🎯 RFM Customer Segmentation")
st.markdown("---")

@st.cache_data
def load_rfm_data():
    df = pd.read_csv("data/superstore_cleaned.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

try:
    df = load_rfm_data()
    
    # 1. RFM Calculation
    # Reference date for Recency (Day after last order in dataset)
    ref_date = df['Order Date'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby('Customer Name').agg({
        'Order Date': lambda x: (ref_date - x.max()).days, # Recency
        'Order ID': 'count',                             # Frequency
        'Sales': 'sum'                                   # Monetary
    }).rename(columns={'Order Date': 'Recency', 'Order ID': 'Frequency', 'Sales': 'Monetary'})

    # 2. Simple Segmentation Logic
    # We'll use quantiles to label customers
    rfm['Segment'] = "Regular"
    rfm.loc[(rfm['Recency'] < rfm['Recency'].quantile(0.25)) & (rfm['Monetary'] > rfm['Monetary'].quantile(0.75)), 'Segment'] = "Champions"
    rfm.loc[(rfm['Recency'] > rfm['Recency'].quantile(0.75)), 'Segment'] = "At Risk"
    rfm.loc[(rfm['Frequency'] > rfm['Frequency'].quantile(0.75)), 'Segment'] = "Loyalists"

    # 3. Visualization: Recency vs Monetary
    st.subheader("Customer Value Matrix")
    fig = px.scatter(rfm.reset_index(), x="Recency", y="Monetary", size="Frequency", 
                     color="Segment", hover_name="Customer Name",
                     title="Recency vs. Monetary Value (Bubble Size = Frequency)",
                     template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

    # 4. Actionable Table
    st.subheader("Segment Deep Dive")
    selected_seg = st.selectbox("Select Segment to View", rfm['Segment'].unique())
    st.dataframe(rfm[rfm['Segment'] == selected_seg].sort_values('Monetary', ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"Error generating RFM: {e}")