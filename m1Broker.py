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

        min_fiyat = veri["Close"].min() - 5
        max_fiyat = veri["Close"].max() + 5

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=veri.index, y=veri["Close"], mode="lines", name=lot))
        fig.update_layout(yaxis=dict(range=[min_fiyat, max_fiyat]))

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
```

---

**Ne eklendi:**

| Kod | Ne yapıyor |
|-----|-----------|
| `veri["Close"].min() - 5` | En düşük fiyattan 5 çıkar |
| `veri["Close"].max() + 5` | En yüksek fiyata 5 ekle |
| `go.Figure()` | Plotly grafiği oluştur |
| `yaxis=dict(range=[...])` | Y eksenini ayarla |
| `st.plotly_chart(fig)` | Grafiği göster |

---

`requirements.txt` dosyasına `plotly` eklemeyi unutma:
```
streamlit
yfinance
plotly
