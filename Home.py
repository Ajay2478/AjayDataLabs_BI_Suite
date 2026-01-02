import streamlit as st
import pandas as pd
import pathlib
import plotly.express as px

st.set_page_config(page_title="AjayDataLabs BI Suite", page_icon="💎", layout="wide")

# 1. New Navigation with RFM Page
pages = [
    st.Page("Home.py", title="Dashboard Overview", icon="🏠", default=True),
    st.Page("app_pages/sales_trends.py", title="Sales Forecasting", icon="📈"),
    st.Page("app_pages/geo_analytics.py", title="Regional Intelligence", icon="🌍"),
    st.Page("app_pages/sentiment_lab.py", title="Customer Sentiment", icon="💬"),
    st.Page("app_pages/rfm_analysis.py", title="Customer Segments", icon="🎯"), # NEW
]
pg = st.navigation(pages)

# 2. Sidebar Branding & GLOBAL YEAR FILTER
st.sidebar.markdown("### 💎 AjayDataLabs")
st.sidebar.caption("v3.0 - Customer Intelligence")

# We store the selected year in 'session_state' to use across pages
df_raw = pd.read_csv("data/superstore_cleaned.csv")
df_raw['Order Date'] = pd.to_datetime(df_raw['Order Date'])
years = sorted(df_raw['Order Date'].dt.year.unique())

selected_year = st.sidebar.select_slider("Select Analysis Year", options=years, value=max(years))

# Filter data globally
df = df_raw[df_raw['Order Date'].dt.year == selected_year]

# 3. Sidebar Methodology
with st.sidebar.expander("🛠️ Methodology"):
    st.markdown(f"Currently viewing data for **{selected_year}**")
    st.write("Models: OLS Regression, RFM Clustering")

# 4. Page Content
if pg.title == "Dashboard Overview":
    st.title(f"🚀 {selected_year} Business Intelligence Suite")
    st.markdown("---")
    
    # Executive KPIs based on filtered data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Annual Revenue", f"₹{df['Sales'].sum():,.0f}")
    with col2:
        st.metric("Avg Order", f"₹{df['Sales'].mean():.0f}")
    with col3:
        st.metric("Logistic Friction", f"{df['Days_to_Ship'].mean():.1f} Days")
    with col4:
        st.metric("Orders Processed", f"{len(df):,}")
            
    st.subheader(f"🏆 Top Performers in {selected_year}")
    top_products = df.groupby('Sub-Category')['Sales'].sum().nlargest(5).reset_index()
    fig = px.bar(top_products, x='Sales', y='Sub-Category', orientation='h', 
                 template="plotly_dark", color='Sales', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
else:
    # Pass the filtered dataframe to other pages via session state if needed
    st.session_state['filtered_df'] = df
    pg.run()