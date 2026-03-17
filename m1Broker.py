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

    periyot = st.selectbox("Periyot seç:", ["1d", "5d", "1mo", "3mo", "1y"])

    gecmis = share.history(period=periyot)

    if gecmis.empty:
        st.error("Hisse bulunamadı!")
    else:
        price = gecmis["Close"].iloc[-1]
        st.success(f"{stock_name}: {round(price, 2)} TL")

        st.line_chart(gecmis["Close"])
