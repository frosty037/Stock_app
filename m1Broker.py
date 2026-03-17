import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

st.title("Hisse Fiyat Sorgulama")

lots = ["LOGO", "ASELS"]

for lot in lots:
    veri = yf.Ticker(f"{lot}.IS").history(period="1mo")
    if not veri.empty:
        fiyat = round(veri["Close"].iloc[-1], 2)
        st.write(f"{lot}: {fiyat} TL")

        min_fiyat = veri["Close"].min()
        max_fiyat = veri["Close"].max()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=veri.index, y=veri["Close"], mode="lines", name=lot))
        fig.update_layout(yaxis=dict(range=[min_fiyat-5, max_fiyat+5]))

        st.plotly_chart(fig)

st.divider()

stock_name = st.text_input("Hisse adı gir:").strip().upper()

if stock_name:
    stock_name += ".IS"
    share = yf.Ticker(stock_name)
    gecmis = share.history(period="1mo")
    if gecmis.empty:
        st.error("Hisse bulunamadı!")
    else:
        price = round(gecmis["Close"].iloc[-1], 2)
        st.success(f"{stock_name}: {round(price, 2)} TL")
