import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bonhoeffer Dashboard", layout="wide")
st.title("🌍 Bonhoeffer Master Data Dashboard")

# ✅ CSS Styling
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            height: 100%;
            background: linear-gradient(to bottom right, #004aad, #e0f7fa);
        }
        .block-container {
            padding: 4rem;
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 12px;
            box-shadow: 0 0 12px rgba(0, 0, 0, 0.05);
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(to bottom right, #e0f7fa, #284aad); 
            color: white;
        }
        h1 {
            color: #004aad;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Available Month Tabs
month_tabs = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# ✅ Country and Intern mapping for Leads
country_sheets = {
    "Mexico": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1nALlHhcBTFGqhHEOgxc2vLg6Wq7kr4n7EFeDeC9M3ho/gviz/tq?tqx=out:csv&sheet=Data%20Sheet"
    },
    "India": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1aEsnXfmDTg4XVIPQ4HdGZqjfg1jO-WtyC2nW67qqkuU/gviz/tq?tqx=out:csv&sheet=Data%20Sheet"
    }
}

# ✅ Conversation Sheets: only IDs
conversation_sheets = {
    "Mexico": "1-INGrynbGU7IBLXggsoH9eFvAwgXPjPcFT_OOCPlgJA",
    "India": "1hHZCqXmQP-yd7X-WjJBWKCY2s-YENLj2dYtFXNWjOq4"
}

# ✅ Primary Sales Leads setup
primary_sales_sheet_id = "1LezlwNw1tj2DyRUBHZeTVHagczE_-gJKZ45PLpGvf0w"
primary_sales_sheets = {
    month: f"https://docs.google.com/spreadsheets/d/{primary_sales_sheet_id}/gviz/tq?tqx=out:csv&sheet={month}"
    for month in month_tabs
}

# ✅ Cached loader
@st.cache_data(ttl=3600)
def load_data_from_url(url):
    return pd.read_csv(url)

# 🧭 Sidebar — Mode Toggle
view_mode = st.sidebar.radio("📊 Select View Mode", ["Leads", "Campaign Conversation", "Primary Sales Leads"])

# ----------------------------- LEADS VIEW -----------------------------
if view_mode == "Leads":
    selected_country = st.sidebar.selectbox("🌐 Select Country", list(country_sheets.keys()))
    selected_region = st.sidebar.selectbox("📍 Select Intern/State", list(country_sheets[selected_country].keys()))

    st.subheader(f"📄 Leads Data - {selected_country} → {selected_region}")
    try:
        df_leads = load_data_from_url(country_sheets[selected_country][selected_region])
        st.success(f"✅ Total Entries: {len(df_leads)}")
        st.dataframe(df_leads, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Could not load lead data: {e}")

# ------------------------ CAMPAIGN CONVERSATION VIEW ------------------------
elif view_mode == "Campaign Conversation":
    selected_country = st.sidebar.selectbox("🌐 Select Country", list(conversation_sheets.keys()))
    selected_month = st.sidebar.selectbox("🗓️ Select Month", month_tabs)

    sheet_id = conversation_sheets[selected_country]
    encoded_month = selected_month.replace(" ", "%20")
    convo_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_month}"

    st.subheader(f"📊 Campaign Conversation - {selected_country} ({selected_month})")
    try:
        df_convo = load_data_from_url(convo_url)
        st.success(f"✅ Total Conversations: {len(df_convo)}")
        st.dataframe(df_convo, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Could not load campaign data: {e}")

# ------------------------ PRIMARY SALES LEADS VIEW ------------------------
elif view_mode == "Primary Sales Leads":
    selected_month = st.sidebar.selectbox("🗓️ Select Month", month_tabs)
    sales_url = primary_sales_sheets[selected_month]

    st.subheader(f"📈 Primary Sales Leads - {selected_month}")
    try:
        df_sales = load_data_from_url(sales_url)
        st.success(f"✅ Total Entries: {len(df_sales)}")
        st.dataframe(df_sales, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Could not load sales data: {e}")
