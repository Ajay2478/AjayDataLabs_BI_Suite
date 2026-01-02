import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.title("📈 Advanced Sales Forecasting")
st.markdown("---")

@st.cache_data
def load_forecast_data():
    df = pd.read_csv("data/superstore_cleaned.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Order Date'])
    return df

try:
    df = load_forecast_data()
    
    # 1. Prepare Time-Series (Index & Resample)
    df_time = df.set_index('Order Date').sort_index()
    monthly_sales = df_time['Sales'].resample('ME').sum().reset_index()
    monthly_sales['Month_Count'] = np.arange(len(monthly_sales))

    # 2. Train OLS Model
    X = monthly_sales['Month_Count'].values.reshape(-1, 1)
    y = monthly_sales['Sales'].values
    model = LinearRegression().fit(X, y)
    
    # Make Predictions for existing data
    monthly_sales['Trendline'] = model.predict(X)

    # 3. Visualization
    fig = px.line(monthly_sales, x='Order Date', y='Sales', 
                  title="Revenue Velocity vs. Market Trend",
                  template="plotly_dark", color_discrete_sequence=['#00d4ff'])
    
    fig.add_scatter(x=monthly_sales['Order Date'], y=monthly_sales['Trendline'], 
                    name="OLS Trendline", line=dict(color='red', dash='dash'))
    
    st.plotly_chart(fig, use_container_width=True)

    # 4. FUTURE FORECAST TABLE (New Feature)
    st.subheader("🔮 6-Month AI Forecast")
    
    # Create future months
    last_month_num = monthly_sales['Month_Count'].max()
    future_months = np.array(range(last_month_num + 1, last_month_num + 7)).reshape(-1, 1)
    future_predictions = model.predict(future_months)
    
    # Display as a clean table
    forecast_df = pd.DataFrame({
        "Month Ahead": [f"Month +{i}" for i in range(1, 7)],
        "Predicted Sales ($)": [f"${x:,.2f}" for x in future_predictions],
        "Growth Status": ["🚀 Positive" if x > monthly_sales['Sales'].mean() else "⚠️ Below Avg" for x in future_predictions]
    })
    
    st.table(forecast_df)

except Exception as e:
    st.error(f"⚠️ Error: {e}")