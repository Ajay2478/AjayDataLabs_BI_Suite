import pandas as pd
import pathlib

def run_pipeline():
    print("💎 AjayDataLabs: Starting Data Engineering Pipeline...")
    
    curr_dir = pathlib.Path(__file__).parent.resolve()
    input_path = curr_dir / "data" / "superstore.csv"
    output_path = curr_dir / "data" / "superstore_cleaned.csv"

    df = pd.read_csv(input_path, encoding='ISO-8859-1')
    df.columns = df.columns.str.strip()

    # 1. Temporal Engineering (Fixed)
    print("⏳ Parsing dates...")
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, format='mixed')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, format='mixed')
    df = df.sort_values('Order Date')

    # 2. Engineering New "Elite" Metrics (Since Profit is missing)
    print("🛠️ Engineering New Metrics...")
    
    # Calculate Shipping Delay (Efficiency Metric)
    df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Create Time Ordinals for OLS Forecasting
    start_date = df['Order Date'].min()
    df['Months_Since_Start'] = ((df['Order Date'].dt.year - start_date.year) * 12 + 
                                (df['Order Date'].dt.month - start_date.month))

    # 3. Clean and Export
    df['Postal Code'] = df['Postal Code'].fillna(0).astype(int)
    
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Cleaned data saved to {output_path}")
    print(f"📊 New Features: 'Days_to_Ship' and 'Months_Since_Start'")

if __name__ == "__main__":
    run_pipeline()