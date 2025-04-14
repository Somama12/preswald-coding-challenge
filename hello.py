from preswald import connect, get_df, query, table, text, slider, plotly
import pandas as pd
import plotly.express as px

# Initialize
connect()
try:
    df = get_df("yahoo_stock")
    # Convert Date to string to avoid Timestamp issues
    df["Date"] = df["Date"].astype(str)
    text(f"Loaded {len(df)} rows")
    text(f"Close range: {df['Close'].min():.2f} to {df['Close'].max():.2f}")
except Exception as e:
    text(f"Error loading data: {str(e)}")
    df = pd.DataFrame()

# Title
text("# Stock Market Explorer 📈")

# Sample table
if not df.empty:
    sample_df = df[["Date", "Close", "Volume"]].head(10).reset_index(drop=True)
    text(f"Sample table rows: {len(sample_df)}")
    table(sample_df, title="Sample Stock Data")

# Query table
if not df.empty:
    try:
        sql = "SELECT Date, Close, Volume FROM yahoo_stock WHERE Close > 2000"
        high_close_df = query(sql, "yahoo_stock")
        high_close_df["Date"] = high_close_df["Date"].astype(str)
        high_close_df = high_close_df.reset_index(drop=True)
        text(f"Query returned {len(high_close_df)} rows")
        table(high_close_df.head(50), title="Days with Close > 2000")
    except Exception as e:
        text(f"Query error: {str(e)}")

# Slider table
if not df.empty:
    close_threshold = slider("Closing Price Threshold", min_val=1500, max_val=4000, default=2000)
    filtered_df = df[df["Close"] > close_threshold][["Date", "Close", "Volume"]].reset_index(drop=True)
    text(f"Slider filter returned {len(filtered_df)} rows")
    table(filtered_df.head(50), title=f"Days with Close > {close_threshold}")

# Plot
if not df.empty:
    try:
        fig = px.line(
            df,
            x="Date",
            y="Close",
            title="Stock Closing Price Over Time",
            labels={"Close": "Closing Price ($)", "Date": "Date"}
        )
        fig.update_layout(template="plotly_white")
        plotly(fig)
    except Exception as e:
        text(f"Plot error: {str(e)}")