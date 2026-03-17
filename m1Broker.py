import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

st.title("Hisse Fiyat Sorgulama")

if "lots" not in st.session_state:
    st.session_state.lots = ["LOGO", "ASELS"]

def goster(ad, veri):
    baslangic = veri["Close"].iloc[0]
    son = veri["Close"].iloc[-1]
    yuzde = round((son - baslangic) / baslangic * 100, 2)
    renk = "🟢" if yuzde >= 0 else "🔴"
    st.write(f"{renk} {ad}: {round(son, 2)} TL  |  %{yuzde}")
    min_fiyat = veri["Close"].min()
    max_fiyat = veri["Close"].max()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=veri.index.astype(str),
        y=veri["Close"].values,
        mode="lines",
        name=ad
    ))
    fig.update_layout(yaxis=dict(range=[min_fiyat-5, max_fiyat+5]))
    st.plotly_chart(fig)

hisse_listesi = []

for lot in st.session_state.lots:
    veri = yf.Ticker(f"{lot}.IS").history(period="5d")
    if not veri.empty:
        baslangic = veri["Close"].iloc[0]
        son = veri["Close"].iloc[-1]
        yuzde = round((son - baslangic) / baslangic * 100, 2)
        hisse_listesi.append({"ad": lot, "yuzde": yuzde, "veri": veri})

hisse_list
