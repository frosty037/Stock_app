import yfinance as yf
import streamlit as st

sifre = st.text_input("Şifre:", type="password")

if sifre != "samet123":
    st.stop()


st.title("Hisse Fiyat Sorgulama")

stock_name = st.text_input("Hisse adı gir:").strip().upper()

if stock_name:
    stock_name += ".IS"
    share = yf.Ticker(stock_name)
    bilgi = share.info
    price = bilgi.get("currentPrice")

    if price is None:
        st.error("Hisse bulunamadı!")
    else:
        st.success(f"{stock_name}: {price} TL")