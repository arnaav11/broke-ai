import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
from datetime import datetime, timedelta
import random

def predict_future_spend(daily_spending_data, days_to_forecast=30):
    """
    Feeds historical daily spending into Prophet to predict future cash flow run-rate.
    """
    print("Initializing Prophet AI Engine...\n")
    
    # 1. Load data into Pandas
    df = pd.DataFrame(daily_spending_data)
    
    # 2. Prophet MANDATORY step: Rename columns to 'ds' (date) and 'y' (metric)
    df.rename(columns={'date': 'ds', 'daily_total': 'y'}, inplace=True)
    
    # Ensure the date column is officially a Pandas datetime object
    df['ds'] = pd.to_datetime(df['ds'])
    
    # 3. Instantiate the Prophet model
    # We turn off yearly seasonality since we only have a few months of mock data
    model = Prophet(yearly_seasonality=False, daily_seasonality=False)
    
    # 4. Train the model on your historical data
    model.fit(df)
    
    # 5. Tell Prophet to create an empty calendar for the next 30 days
    future_calendar = model.make_future_dataframe(periods=days_to_forecast)
    
    # 6. Run the prediction!
    forecast = model.predict(future_calendar)
    
    return model, forecast

if __name__ == "__main__":
    # Generate 60 days of simulated historical spending data
    today = datetime.now()
    mock_history = []
    
    for i in range(60, 0, -1):
        simulated_date = today - timedelta(days=i)
        # Simulate spending between $20 and $150 a day
        simulated_spend = round(random.uniform(20.0, 150.0), 2) 
        
        mock_history.append({
            "date": simulated_date.strftime("%Y-%m-%d"),
            "daily_total": simulated_spend
        })
        
    # Run the Forecasting Engine
    model, forecast_df = predict_future_spend(mock_history, days_to_forecast=30)
    
    # Extract just the predicted future dates
    future_predictions = forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
    
    # Calculate projected total spend for the next month
    projected_total = future_predictions['yhat'].sum()
    
    print("--- [30-DAY FORECAST RESULTS] ---")
    print(f"Projected Total Spend for next 30 days: ${projected_total:,.2f}\n")
    
    print("Preview of next 5 days expected run-rate:")
    print(future_predictions.head(5).to_string(index=False))
    print("---------------------------------")
    
   # NEW VISUALLY APPEALING PLOTLY CODE:
    print("Generating interactive forecast visualization...")
    
    # Create the modern interactive chart
    fig = plot_plotly(model, forecast_df)
    
    # Customize the aesthetics
    fig.update_layout(
        title={
            'text': "<b>AI 30-Day Cash Flow Forecast</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)
        },
        yaxis_title="Daily Spend ($)",
        template="plotly_dark",
        hovermode="x unified",
        
        # --- FIX #1: THE VISIBILITY OF THE TOP BUTTONS ---
        xaxis=dict(
            title="Date",
            rangeselector=dict(
                bgcolor='#2A2A2A',         # Dark grey background for resting buttons
                activecolor='#0052cc',     # Deep blue background for the clicked button
                font=dict(color='#FFFFFF') # Crisp white text so you can actually read it
            )
        )
    )
    
    # --- FIX #2: THE VISIBILITY OF THE HISTORICAL DATA POINTS ---
    # We target the 'markers' (dots) and change them to a bright cyan
    fig.update_traces(
        marker=dict(color='#00d2ff', size=6, opacity=0.9), 
        selector=dict(mode='markers')
    )
    
    # Launch the interactive graph in your web browser
    fig.show()