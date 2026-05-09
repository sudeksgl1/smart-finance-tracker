import streamlit as st
import pandas as pd
from database import create_table, add_transaction, get_transactions, delete_transaction
from analysis import analyze, get_warnings
from datetime import date

st.set_page_config(page_title="Smart Finance Tracker", layout="wide")


# 🌧️ Duygu yağmuru
def emotion_rain(transaction_type):
    if "Gelir" in transaction_type:
        emojis = ["💰", "✨", "🌟", "😻"]
    else:
        emojis = ["💸", "😭", "☁️", "😿"]

    html = """
    <style>
    .emoji {
        position: fixed;
        top: -60px;
        font-size: 52px;
        animation: fall linear infinite;
        z-index: 9999;
        pointer-events: none;
    }

    @keyframes fall {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
    </style>
    """

    positions = [10, 25, 40, 55, 70, 85]
    durations = [2, 2.3, 2.6, 2.1, 2.8, 2.4]

    for i, pos in enumerate(positions):
        emoji = emojis[i % len(emojis)]
        html += f"""
        <div class="emoji" style="left:{pos}%; animation-duration:{durations[i]}s;">
            {emoji}
        </div>
        """

    st.markdown(html, unsafe_allow_html=True)


# 📊 dict → tablo dönüşümü
def dict_to_df(d):
    df = pd.DataFrame(d.items(), columns=["Kategori", "Tutar"])

    if df.empty:
        return df

    df["Tutar"] = df["Tutar"].apply(lambda x: f"{x:,.0f} TL")
    df.index = range(1, len(df) + 1)
    df.index.name = "No"

    return df


# 🧱 Setup
create_table()


# 🎨 Tema seçimi
theme = st.sidebar.selectbox(
    "Tema seç 🎨",
    ["🌸 Soft Mode", "🌙 Dark Mode", "☀️ Light Mode"]
)

if theme == "🌸 Soft Mode":
    bg = "#fff1f7"
    card = "#ffe4f0"
    text = "#4a2438"
    chart_color = "#ff7eb6"
    second_chart_color = "#c084fc"

elif theme == "🌙 Dark Mode":
    bg = "#0f172a"
    card = "#1e293b"
    text = "#f8fafc"
    chart_color = "#38bdf8"
    second_chart_color = "#a78bfa"

else:
    bg = "#f8fafc"
    card = "#e0f2fe"
    text = "#0f172a"
    chart_color = "#2563eb"
    second_chart_color = "#f59e0b"


st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text};
}}

[data-testid="stSidebar"] {{
    background-color: {card};
}}

div[data-testid="stMetric"] {{
    background-color: {card};
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}

div[data-testid="stDataFrame"] {{
    background-color: {card};
    border-radius: 16px;
}}

h1, h2, h3, p, label, span {{
    color: {text} !important;
}}
</style>
""", unsafe_allow_html=True)


st.markdown("""
# 💰 Smart Finance Tracker
""")


# 📌 Menü
page = st.sidebar.radio(
    "Menü",
    ["Özet", "Gelirler", "Giderler", "Yeni İşlem Ekle", "İşlem Sil"]
)


# 📥 Veri çek
data = get_transactions()
df = pd.DataFrame(data, columns=["Numara", "Tür", "Tutar", "Kategori", "Tarih"])

income, expense, income_categories, expense_categories, fixed_income_categories, fixed_expense_categories = analyze(data)


# ------------------ 📊 ÖZET ------------------
if page == "Özet":
    st.subheader("📊 Finans Özeti")

    col1, col2, col3 = st.columns(3)

    col1.metric("Toplam Gelir", f"{income:,.0f} TL")
    col2.metric("Toplam Gider", f"{expense:,.0f} TL")
    col3.metric("Kalan", f"{income - expense:,.0f} TL")

    st.divider()
    st.subheader("📋 Kayıtlı İşlemler")

    if df.empty:
        st.info("Henüz hiç işlem eklenmemiş.")
    else:
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("📈 Grafikler")

        df["Tutar"] = pd.to_numeric(df["Tutar"], errors="coerce")

        st.write("### Gelir - Gider Grafiği")
        tur_grafigi = df.groupby("Tür")["Tutar"].sum().reset_index()

        st.vega_lite_chart(
            tur_grafigi,
            {
                "mark": {
                    "type": "bar",
                    "cornerRadiusEnd": 8,
                    "color": chart_color
                },
                "encoding": {
                    "x": {"field": "Tür", "type": "nominal"},
                    "y": {"field": "Tutar", "type": "quantitative"}
                }
            },
            use_container_width=True
        )

        st.write("### Kategori Bazlı Gider Grafiği")
        giderler = df[df["Tür"].str.contains("Gider", case=False, na=False)]

        if giderler.empty:
            st.info("Henüz gider işlemi yok.")
        else:
            kategori_grafigi = giderler.groupby("Kategori")["Tutar"].sum().reset_index()

            st.vega_lite_chart(
                kategori_grafigi,
                {
                    "mark": {
                        "type": "bar",
                        "cornerRadiusEnd": 8,
                        "color": second_chart_color
                    },
                    "encoding": {
                        "x": {"field": "Kategori", "type": "nominal"},
                        "y": {"field": "Tutar", "type": "quantitative"}
                    }
                },
                use_container_width=True
            )

    st.divider()
    st.subheader("⚠️ Uyarılar")

    warnings = get_warnings(income, expense, expense_categories)

    if warnings:
        for w in warnings:
            st.warning(w)
    else:
        st.success("Her şey dengede 👍")


# ------------------ 🟢 GELİRLER ------------------
elif page == "Gelirler":
    st.subheader("🟢 Gelirler")

    st.write("### Normal Gelirler")
    st.table(dict_to_df(income_categories))

    st.write("### Sabit Gelirler")
    st.table(dict_to_df(fixed_income_categories))


# ------------------ 🔴 GİDERLER ------------------
elif page == "Giderler":
    st.subheader("🔴 Giderler")

    st.write("### Normal Giderler")
    st.table(dict_to_df(expense_categories))

    st.write("### Sabit Giderler")
    st.table(dict_to_df(fixed_expense_categories))


# ------------------ ➕ EKLE ------------------
elif page == "Yeni İşlem Ekle":
    st.subheader("➕ Yeni İşlem")

    t = st.selectbox("İşlem Türü", ["Gelir", "Gider", "Sabit Gelir", "Sabit Gider"])
    a = st.number_input("Tutar", min_value=0.0)
    c = st.text_input("Kategori")
    d = st.date_input("Tarih", value=date.today())

    if st.button("Ekle"):
        add_transaction(t, a, c, str(d))

        if "Gelir" in t:
            st.success("Gelir eklendi! 💰✨")
        else:
            st.warning("Gider eklendi! 😿💸")

        emotion_rain(t)


# ------------------ 🗑️ SİL ------------------
elif page == "İşlem Sil":
    st.subheader("🗑️ İşlem Sil")

    if not df.empty:
        df_display = df.copy()
        df_display.index = range(1, len(df_display) + 1)
        df_display.index.name = "No"

        st.dataframe(df_display, use_container_width=True)

        selected = st.selectbox("Silmek için Numara seç", df["Numara"])

        if st.button("Sil"):
            delete_transaction(selected)
            st.success("Silindi")
            st.rerun()
    else:
        st.info("Kayıt yok")