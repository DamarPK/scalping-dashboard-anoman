import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

Judul Aplikasi

st.set_page_config(page_title="Scalping Dashboard Anoman", layout="wide") st.title("📈 SCALPING DASHBOARD - ANOMAN")

Data Dummy Saham BBCA

Bisa diganti nanti pakai scraping/API

sample_data = { 'Date': pd.date_range(end=datetime.date.today(), periods=10), 'Open': [8900, 8950, 8920, 8960, 8990, 9000, 9050, 9100, 9080, 9110], 'High': [8950, 8970, 8960, 9000, 9020, 9050, 9100, 9150, 9120, 9160], 'Low': [8850, 8900, 8900, 8920, 8950, 8970, 9010, 9050, 9040, 9070], 'Close': [8920, 8960, 8940, 8980, 9000, 9020, 9070, 9110, 9100, 9150], 'Volume': [80_000_000, 85_000_000, 78_000_000, 90_000_000, 100_000_000, 105_000_000, 120_000_000, 125_000_000, 118_000_000, 130_000_000], 'Foreign Buy': [40_000_000, 42_000_000, 38_000_000, 45_000_000, 48_000_000, 50_000_000, 60_000_000, 70_000_000, 68_000_000, 75_000_000], 'Foreign Sell': [30_000_000, 35_000_000, 40_000_000, 42_000_000, 43_000_000, 47_000_000, 50_000_000, 55_000_000, 52_000_000, 60_000_000], 'Dom Buy': [50_000_000, 53_000_000, 48_000_000, 52_000_000, 55_000_000, 57_000_000, 60_000_000, 58_000_000, 59_000_000, 61_000_000], 'Dom Sell': [60_000_000, 63_000_000, 58_000_000, 60_000_000, 62_000_000, 64_000_000, 63_000_000, 60_000_000, 61_000_000, 63_000_000], }

Konversi ke DataFrame

df = pd.DataFrame(sample_data) df['Net Foreign'] = df['Foreign Buy'] - df['Foreign Sell'] df['Net Dom'] = df['Dom Buy'] - df['Dom Sell']

Chart Candlestick

tab1, tab2 = st.tabs(["📊 Chart", "📑 Analisa"])

with tab1: fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Harga')])

fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume', marker_color='lightblue', yaxis='y2'))

fig.update_layout(
    title='Chart Harga & Volume - BBCA',
    xaxis_title='Tanggal',
    yaxis_title='Harga',
    yaxis2=dict(overlaying='y', side='right', showgrid=False),
    xaxis_rangeslider_visible=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

with tab2: st.subheader("📑 Ringkasan Data dan Sinyal") latest = df.iloc[-1] trend_note = "⬆️ POTENSI NAIK" if latest['Net Foreign'] > 0 and latest['Net Dom'] > 0 else "⬇️ HATI-HATI DISTRIBUSI"

st.markdown(f"""
- **Harga Terakhir:** Rp{latest['Close']:,}
- **Volume:** {latest['Volume']:,}
- **Net Foreign:** {latest['Net Foreign']:,} ({'Buy' if latest['Net Foreign'] > 0 else 'Sell'})
- **Net Domestik:** {latest['Net Dom']:,} ({'Buy' if latest['Net Dom'] > 0 else 'Sell'})
- **Sinyal Arah:** **{trend_note}**
- **Support:** Rp{df['Low'].min():,} | **Resistance:** Rp{df['High'].max():,}
""")

st.dataframe(df[['Date', 'Close', 'Volume', 'Net Foreign', 'Net Dom']].sort_values('Date', ascending=False), use_container_width=True)

