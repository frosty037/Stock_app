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

hisse_listesi.sort(key=lambda x: x["yuzde"], reverse=True)

for hisse in hisse_listesi:
    goster(hisse["ad"], hisse["veri"])

st.divider()

stock_name = st.text_input("Hisse adı gir:").strip().upper()

if stock_name:
    stock_name += ".IS"
    share = yf.Ticker(stock_name)
    gecmis = share.history(period="5d")
    if gecmis.empty:
        st.error("Hisse bulunamadı!")
    else:
        goster(stock_name, gecmis)
        if st.button("Listeye Ekle"):
            hisse = stock_name.replace(".IS", "")
            if hisse not in st.session_state.lots:
                st.session_state.lots.append(hisse)
                st.success(f"{hisse} listeye eklendi!")
            else:
                st.warning("Zaten listede var!")
