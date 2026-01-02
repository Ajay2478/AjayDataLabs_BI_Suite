import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.title("🌍 Regional Logistics Intelligence")
st.markdown("---")

# Use the filtered data from Home.py session state
if 'filtered_df' in st.session_state:
    df = st.session_state['filtered_df']
else:
    # Fallback for direct page access
    df = pd.read_csv("data/superstore_cleaned.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])

try:
    # 2. Key Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        top_city = df.groupby('City')['Sales'].sum().idxmax()
        st.metric("Top City by Sales", top_city)
    with col2:
        avg_delay = df['Days_to_Ship'].mean()
        st.metric("Avg. Shipping Delay", f"{avg_delay:.1f} Days")
    with col3:
        fastest_region = df.groupby('Region')['Days_to_Ship'].mean().idxmin()
        st.metric("Fastest Shipping Region", fastest_region)

    # 3. USA Choropleth Map
    st.subheader("📍 National Sales Hotspots")
    
    # Prep State-level data
    state_data = df.groupby('State').agg({'Sales':'sum', 'Days_to_Ship':'mean'}).reset_index()
    map_metric = st.selectbox("Select Map Insight", ["Sales", "Days_to_Ship"])
    
    fig = px.choropleth(state_data, 
                        locations='State', 
                        locationmode="USA-states", 
                        color=map_metric,
                        scope="usa",
                        hover_name="State",
                        title=f"USA Logistics Map: {map_metric}",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        template="plotly_dark")
    
    st.plotly_chart(fig, use_container_width=True)

    # 4. State Leaderboard & Regional Breakdown
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("🏙️ Top States")
        state_leaders = df.groupby('State')['Sales'].sum().nlargest(5)
        st.bar_chart(state_leaders)

    with col_b:
        st.subheader("📊 Regional Performance")
        regional_stats = df.groupby('Region').agg({
            'Sales': 'sum', 
            'Days_to_Ship': 'mean',
            'Order ID': 'count'
        }).rename(columns={'Order ID': 'Total Orders'})
        
        # Professional highlight for top performers
        st.dataframe(regional_stats.style.highlight_max(axis=0, color='#00d4ff'), use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error: {e}")