import yfinance as yf
import streamlit as st

st.title("Hisse Fiyat Sorgulama")

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
