import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💬 Customer & Product Sentiment Lab")
st.markdown("---")

# Use the filtered data from Home.py if available, otherwise load raw
if 'filtered_df' in st.session_state:
    df = st.session_state['filtered_df']
else:
    df = pd.read_csv("data/superstore_cleaned.csv")

try:
    # 1. Automatic Insight Generator
    # We aggregate to find which products are "Friction Points"
    cat_stats = df.groupby('Sub-Category').agg({'Sales':'sum', 'Days_to_Ship':'mean'}).reset_index()
    
    # Logic: High Sales + High Shipping Days = Risk
    risky_cat = cat_stats.sort_values(by=['Sales', 'Days_to_Ship'], ascending=[False, False]).iloc[0]
    
    st.info(f"""
    💡 **AI Insight:** The **'{risky_cat['Sub-Category']}'** category is a top revenue driver but currently 
    averages **{risky_cat['Days_to_Ship']:.1f} days** to ship. This is a primary target for logistics optimization 
    to protect customer sentiment.
    """)

    # 2. Quadrant Analysis
    st.subheader("🎯 Product Sentiment Matrix")
    fig = px.scatter(cat_stats, x='Days_to_Ship', y='Sales', 
                     size='Sales', color='Sub-Category',
                     hover_name='Sub-Category',
                     title="Revenue vs. Shipping Friction (Quadrant View)",
                     labels={'Days_to_Ship': 'Avg Shipping Days (Lower is Better)'},
                     template="plotly_dark", height=500)
    
    # Reference lines for "Average" performance
    fig.add_hline(y=cat_stats['Sales'].mean(), line_dash="dot", line_color="gray", annotation_text="Avg Sales")
    fig.add_vline(x=cat_stats['Days_to_Ship'].mean(), line_dash="dot", line_color="gray", annotation_text="Avg Delay")
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. Market Share & FIXED Ship Mode Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Market Share")
        fig2 = px.pie(df, values='Sales', names='Segment', hole=0.5, 
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
        
    with col2:
        st.subheader("📦 Ship Mode Preference")
        # IMPROVEMENT: Changed to horizontal bar chart for better label readability
        ship_data = df.groupby('Ship Mode')['Sales'].sum().reset_index()
        fig3 = px.bar(ship_data, x='Sales', y='Ship Mode', orientation='h', 
                      template="plotly_dark", color='Sales',
                      color_continuous_scale='Blues')
        st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error: {e}")