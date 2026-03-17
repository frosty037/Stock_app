import yfinance as yf
import streamlit as st

st.title("Hisse Fiyat Sorgulama")


lots = ["LOGO", "ASELS"]

for lot in lots:
    veri = yf.Ticker(f"{lot}.IS").history(period="1d")
    if not veri.empty:
        veri = yf.Ticker(f"{lot}.IS").history(period="1d", interval="1m")
        fiyat = round(veri["Close"].iloc[-1], 2)

        st.line_chart(veri["Close"])

stock_name = st.text_input("Hisse adı gir:").strip().upper()

if stock_name:
    stock_name += ".IS"
    share = yf.Ticker(stock_name)
    
    gecmis = share.history(period="1d")
    
    if gecmis.empty:
        st.error("Hisse bulunamadı!")
    else:
        price = gecmis["Close"].iloc[-1]
        st.success(f"{stock_name}: {round(price, 2)} TL")
