import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta

# Title of the app
st.title("Apple Stock Price Dashboard")

# Fetch last 1 year of Apple stock price data
ticker = 'AAPL'
start_date = pd.to_datetime('today') - pd.DateOffset(years=1)
end_date = pd.to_datetime('today')
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate technical indicators
data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
data['MACD'] = ta.trend.MACD(data['Close']).macd()
data['Signal_Line'] = ta.trend.MACD(data['Close']).macd_signal()
data['Stochastic'] = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close']).stoch()

# Define buy/sell signals
data['Signal'] = np.where(data['RSI'] > 70, 'Sell', 
                 np.where(data['RSI'] < 30, 'Buy', 'Hold'))

# Plotting stock prices and indicators
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

# Stock price
ax1.plot(data['Close'], label='Close Price', color='blue')
ax1.set_title('Apple Stock Price')
ax1.set_ylabel('Price (USD)')
ax1.legend()

# RSI
ax2.plot(data['RSI'], label='RSI', color='orange')
ax2.axhline(70, linestyle='--', alpha=0.5, color='red')
ax2.axhline(30, linestyle='--', alpha=0.5, color='green')
ax2.set_title('Relative Strength Index (RSI)')
ax2.set_ylabel('RSI')
ax2.legend()

# MACD
ax3.plot(data['MACD'], label='MACD', color='purple')
ax3.plot(data['Signal_Line'], label='Signal Line', color='red')
ax3.axhline(0, linestyle='--', alpha=0.5, color='black')
ax3.set_title('MACD')
ax3.set_ylabel('MACD')
ax3.legend()

# Stochastic Oscillator
ax4.plot(data['Stochastic'], label='Stochastic', color='green')
ax4.axhline(80, linestyle='--', alpha=0.5, color='red')
ax4.axhline(20, linestyle='--', alpha=0.5, color='blue')
ax4.set_title('Stochastic Oscillator')
ax4.set_ylabel('Stochastic')
ax4.legend()

plt.xlabel('Date')

# Display plots in Streamlit
st.pyplot(fig)

# Display buy/sell signals as a gauge/meter
buy_signal_count = (data['Signal'] == 'Buy').sum()
sell_signal_count = (data['Signal'] == 'Sell').sum()

# Create a gauge/meter
st.write("### Buy/Sell Signal Gauge")

# Use st.metric for a simple representation
st.metric("Buy Signals", buy_signal_count, delta=f"{buy_signal_count}")
st.metric("Sell Signals", sell_signal_count, delta=f"{sell_signal_count}")

# Optional: Add a gauge-like representation using Plotly
import plotly.graph_objects as go

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=buy_signal_count,
    title={'text': "Buy/Sell Signal Count"},
    gauge={
        'axis': {'range': [0, max(buy_signal_count, sell_signal_count) + 10]},
        'bar': {'color': "green"},
        'steps': [
            {'range': [0, sell_signal_count], 'color': "red"},
            {'range': [sell_signal_count, max(buy_signal_count, sell_signal_count) + 10], 'color': "lightgray"}
        ]
    }
))

# Display the gauge using Plotly
st.plotly_chart(fig_gauge)

