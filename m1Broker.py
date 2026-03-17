import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

st.title("Hisse Fiyat Sorgulama")

if "lots" not in st.session_state:
    st.session_state.lots = ["LOGO", "ASELS"]

# Önce verileri topla
hisse_listesi = []

for lot in st.session_state.lots:
    veri = yf.Ticker(f"{lot}.IS").history(period="1d")
    if not veri.empty:
        baslangic = veri["Close"].iloc[0]
        son = veri["Close"].iloc[-1]
        yuzde = round((son - baslangic) / baslangic * 100, 2)
        hisse_listesi.append({
            "ad": lot,
            "fiyat": round(son, 2),
            "yuzde": yuzde,
            "veri": veri
        })

# Sırala
hisse_listesi.sort(key=lambda x: x["yuzde"], reverse=True)

# Göster
for hisse in hisse_listesi:
    renk = "🟢" if hisse["yuzde"] >= 0 else "🔴"
    st.write(f"{renk} {hisse['ad']}: {hisse['fiyat']} TL  |  %{hisse['yuzde']}")
    min_fiyat = hisse["veri"]["Close"].min()
    max_fiyat = hisse["veri"]["Close"].max()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hisse["veri"].index, y=hisse["veri"]["Close"], mode="lines", name=hisse["ad"]))
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
        baslangic = gecmis["Close"].iloc[0]
        son = gecmis["Close"].iloc[-1]
        yuzde = round((son - baslangic) / baslangic * 100, 2)
        renk = "🟢" if yuzde >= 0 else "🔴"

        st.write(f"{renk} {stock_name}: {round(son, 2)} TL  |  %{yuzde}")

        min_fiyat = gecmis["Close"].min()
        max_fiyat = gecmis["Close"].max()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=gecmis.index, y=gecmis["Close"], mode="lines", name=stock_name))
        fig.update_layout(yaxis=dict(range=[min_fiyat-5, max_fiyat+5]))
        st.plotly_chart(fig)
