import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bonhoeffer Dashboard", layout="wide")
st.title("🌍 Bonhoeffer Master Data Dashboard")

# ————— CSS Styling —————
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

# ————— Month Tabs —————
month_tabs = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# ————— Country → Intern/State → sheet‑URL mappings —————
country_sheets = {
    "Mexico": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1nALlHhcBTFGqhHEOgxc2vLg6Wq7kr4n7EFeDeC9M3ho/export?format=csv",
        "Intern 2": "https://docs.google.com/spreadsheets/d/1y9Y8xwtZG891-t6NMAUGY8A6QFuKxltTZTjx325m6Ms/export?format=csv",
        "Intern 3": "https://docs.google.com/spreadsheets/d/1KxDOZKVbOjLnOPmbWkcft0JI-XZVKabTS_Te6HSJKhk/export?format=csv",
        "Intern 4": "https://docs.google.com/spreadsheets/d/1HR9McxwhXRXLBpxiOhTOIUjDCCtl7HcppkRu43Gyub0/export?format=csv",
        "Intern 5": "https://docs.google.com/spreadsheets/d/1C0rqjZymWqHYsCHNy9f-X9jwWx2H8LUsVCHintiDAiU/export?format=csv",
        "Intern 6": "https://docs.google.com/spreadsheets/d/1SuNrDC8XHg_p00nUxNCNvt6pJPC4MfWrWuHUEe4cHSI/export?format=csv",
        "Intern 7": "https://docs.google.com/spreadsheets/d/1BCZk0EM3ZQnL-sY0cPXYpnPhp48Xc4PpRBMafKCo50s/export?format=csv",
        "Intern 8": "https://docs.google.com/spreadsheets/d/1nt5z-pD8Juj7G02UrfljrZ69VLRfyBPdAHW4-3ezljg/export?format=csv",
        "Intern 9": "https://docs.google.com/spreadsheets/d/1InUvZwn3fM0lSuGF0vq22Tm_OzKoFgLb6BUsyeyE1ok/export?format=csv",
        "Intern 10": "https://docs.google.com/spreadsheets/d/1fz6iltA2ZurHxs0S9YPMD-r0la_QPE5rZ4KIZomN_Mk/export?format=csv",
        "Intern 11": "https://docs.google.com/spreadsheets/d/1KMPcyyJb4N8BRf6lul-8umQJKGvFVLWEaNvUKi6aJss/export?format=csv",
        "Intern 12": "https://docs.google.com/spreadsheets/d/1deoAGfUvVz8Ph3ux-8hB55FnayTToEwTa-DTo039eKc/export?format=csv",
        "Intern 13": "https://docs.google.com/spreadsheets/d/16q6MaQSrhhKz-eJpdabahfAOXbuxAESmpR7lq6e6V6E/export?format=csv",
        "Intern 14": "https://docs.google.com/spreadsheets/d/1gqOj3cH6f_I7ijp5SaEfjKFerQ6z8fhqvAI3MliKjyM/export?format=csv",
        "Intern 15": "https://docs.google.com/spreadsheets/d/174vzKnC-41Kuozg2kAj7J26tipMS168r1pzywQ9aOEA/export?format=csv",
        "Intern 16": "https://docs.google.com/spreadsheets/d/1F3nvGSFs9OTpLOxGwUOV2pVCAipc4PQZJ1jdYG9Jm0w/export?format=csv",
        "Intern 17": "https://docs.google.com/spreadsheets/d/16eH2A7O4PUcEZ40qtcfD_OMWIqoELsJuNMLEbjf4yRc/export?format=csv",
        # … your other interns here …
        "All Data": "https://docs.google.com/spreadsheets/d/1LezlwNw1tj2DyRUBHZeTVHagczE_-gJKZ45PLpGvf0w/gviz/tq?tqx=out:csv&sheet=Master_Mexico"
    },
    "India": {
        "Uttar Pradesh": "https://docs.google.com/spreadsheets/d/12k8yG0vDlmr0LJGDBZfswkJEjgEljwWzASIPHC56kik/export?format=csv",
        "Nagaland": "https://docs.google.com/spreadsheets/d/1aEsnXfmDTg4XVIPQ4HdGZqjfg1jO-WtyC2nW67qqkuU/export?format=csv",
        "Rajasthan": "https://docs.google.com/spreadsheets/d/193hrTJMkjuITJ4GLa2NB6SOuasZt2SoqVNxOgNoGreU/export?format=csv",
        "Himachal Pradesh": "https://docs.google.com/spreadsheets/d/1HK5AQFCVAL4Aq_XJ2cXsTGLkc29kPtuZjq7qf-4fOtQ/export?format=csv",
        "Madhya Pradesh 1": "https://docs.google.com/spreadsheets/d/1wDP9SZYjp2IMKC98_K1jGJ8VtMWIwq0vvIQLd0qpDAA/export?format=csv",
        "Punjab": "https://docs.google.com/spreadsheets/d/16rfkmFXUUAFrcDw0hxx3NM5k8nbnjAxkb-bqcNRZbI4/export?format=csv",
        "Bihar": "https://docs.google.com/spreadsheets/d/120n43HwhNyhDDrhedQfMCkrzMvqlF4zArc-UIvIZaOk/export?format=csv",
        "Andhra Pradesh": "https://docs.google.com/spreadsheets/d/1juts6Vw5qP-4oePZk1VnwxBTZ7tbG4oIUlbxTLvrxKQ/export?format=csv",
        "West Bengal": "https://docs.google.com/spreadsheets/d/1CUUzoNYfVQxHZjuwieOgiKfWRR7GDyj0MnopaFgrFvs/export?format=csv",
        "Telangana": "https://docs.google.com/spreadsheets/d/1R6bEhrSIzR-Jg-y52-6L_vI7g2JFt-dximLFrSjk5zM/export?format=csv",
        "Tamil Nadu": "https://docs.google.com/spreadsheets/d/1mcuOaYcKDf77LHHODdP1QPR0TGW7taQkA8b6ylGtZ84/export?format=csv",
        "Jharkhand": "https://docs.google.com/spreadsheets/d/1EInnleZR9VC94mm5sarpMafurgNhr8F-4aTQMEeQJxA/export?format=csv",
        "Gujarat": "https://docs.google.com/spreadsheets/d/1mRuGJUcuTLXWErXQvdkRbVVF0OXdc47sSfU-5wOi87Q/export?format=csv",
        "Haryana": "https://docs.google.com/spreadsheets/d/1GPpw7IT7YmHHNew9WYGKVLROun_VuQTETbHugwxmW48/export?format=csv",
        "Odisha": "https://docs.google.com/spreadsheets/d/1ZOEE9y5PTH7WCJidvl9dTb3lpNPCcx-R9arsKlu1_TY/export?format=csv",
        "Manipur": "https://docs.google.com/spreadsheets/d/1_w4fEiiFGmiaRYwOm6UwtgHt-h2Ywj-IxF0-ibOlbuk/export?format=csv",
        "Madhya Pradesh 2": "https://docs.google.com/spreadsheets/d/1FLEuYTtWX5GEnyFdEE-hkoyDMvQ7TQKPGxTArm9MmYA/export?format=csv",
        "Maharashtra": "https://docs.google.com/spreadsheets/d/1qPkhuVtWRmejNLUNdnSnmxtDYx5O2S7A6oUgeLlTPyw/export?format=csv",
        "Chhattisgarh": "https://docs.google.com/spreadsheets/d/1qucYvy0VO7v2rGT_pMQbtf5saz1HU0pFtt1J1uRpThM/export?format=csv",
        "Uttarakhand": "https://docs.google.com/spreadsheets/d/14RADRb1l9r6oJKsnEHYZJYyHzzmVLE5QGpjHqgBGqP4/export?format=csv",
        "Kerala": "https://docs.google.com/spreadsheets/d/1MnTncZ1khYo3Kd_PKZHvnsokS8yZ3_oEep_uKeTS78I/export?format=csv",
        "Meghalaya": "https://docs.google.com/spreadsheets/d/15mApXjqPzs0T86_93NtUTWJpKJ-0j282frDLirZI04w/export?format=csv",
        # … your other states here …
        "All Data": "https://docs.google.com/spreadsheets/d/1LezlwNw1tj2DyRUBHZeTVHagczE_-gJKZ45PLpGvf0w/gviz/tq?tqx=out:csv&sheet=Master_India"
    },

    "Philippines": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1luQXiR4QnyC_7-svw3-ryXfT2mMdYZYxbNhfm5a-TgY/export?format=csv"
    },
    "Malaysia": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1ZkCcC0gFsWL9eR2x8Ab8BreZWO0XD9RuMCb-WprjAoM/export?format=csv"
    },
    "Thailand": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1S-LkLgSv8Q81DSmJ-Nr5CAbH8DfPNVpI3-bah8_2wik/export?format=csv"
    },
    "Kenya": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1_lZZrMboSS0gFKyKtaup5pffxFRDshDr1L9EW3xZ4jk/export?format=csv",
        "Intern 2": "https://docs.google.com/spreadsheets/d/1SZCjZ0wB1dxieR_OgyPKr8k3b5Yr7lc1Z7PVj1_xGDM/export?format=csv",
        "Intern 3": "https://docs.google.com/spreadsheets/d/1Xt8RkthK5vNmG2kp1nYEa6IskQzcuu0FaYjmbd4OpR0/export?format=csv"
    },
    "Columbia": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1t7kkr1hN5v-FqaC34PmwHlXX3K_UZpBDiT61hLlrkXk/export?format=csv"
    },
    "Saudi Arabia": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1gsa4OfaVO93eA4R8Dlrgud0lP8AaUgFwy_Z0XOtwDXM/export?format=csv",
        "Intern 2": "https://docs.google.com/spreadsheets/d/1ZWwwfwj9DnXq3CqodMmUWa0SyQ_LUPLniTvD6eRYIQw/export?format=csv"
    },
    "Brazil": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1QUrQryUXHDvvruYIdueNI57peA88xOv6afim0I9BPcE/export?format=csv"
    },
    "Uruguay": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1_oVe_GmXea201LtXFiDLkikbrdcgDAhsd6ZDkNh0XQo/export?format=csv"
    },
    "Panama": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1UD36zaYzyal8RxHiFaNRTZH9RuxXZLZ4zFLnNhcK_tQ/export?format=csv",
        "Intern 2": "https://docs.google.com/spreadsheets/d/1W5QUtCVmM2zSm-JKHwgnFyV5OoCwPpD3Nd-KQQCTTb8/export?format=csv"
    },
    "Peru": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1rl5s20mYGIpjXM3Vlggd7QArpsb61tVodsVKRojWG18/export?format=csv",
        "Intern 2": "https://docs.google.com/spreadsheets/d/1t4_FTDunaJqAev5lquroxBgdoBqRr_r2fN5PV4LXxFg/export?format=csv"
    },
    "Honduras": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1rMPBhO6m8AP6efkjpZCZWEamI4a-PABs1pMfN-KcvfM/export?format=csv",
        "Intern 2": "https://docs.google.com/spreadsheets/d/1-Y5d07gZBrUpIFNBSBJ3vDB7PwjDBjlQVRWXrmw8bpE/export?format=csv"
    },
    "Nicaragua": {
        "Intern 1": "https://docs.google.com/spreadsheets/d/1m30-T-oI6__7UyLFVsTKojvsQw5FzfoJTaX6XqnF1_g/export?format=csv",
        "Intern 2": "https://docs.google.com/spreadsheets/d/1l6IYqz3tBOTuYfcpiAEo8svyUnex1nvW3YkKJS9LOf4/export?format=csv"
    }
    # … add other countries as before …
}



# ————— Conversation sheets for “Campaign Conversation” view —————
conversation_sheets = {
    "Mexico": "1-INGrynbGU7IBLXggsoH9eFvAwgXPjPcFT_OOCPlgJA",
    "India": "1hHZCqXmQP-yd7X-WjJBWKCY2s-YENLj2dYtFXNWjOq4"
}

# ————— Primary Sales Leads fixed CSV —————
primary_sales_sheet_id = "1LezlwNw1tj2DyRUBHZeTVHagczE_-gJKZ45PLpGvf0w"
primary_sales_url = (
    f"https://docs.google.com/spreadsheets/d/{primary_sales_sheet_id}"
    f"/gviz/tq?tqx=out:csv&sheet=Primary%20Sales"
)

# ————— Caching loader —————
@st.cache_data(ttl=3600)
def load_csv_from_url(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

# ————— Sidebar: choose view —————
view_mode = st.sidebar.radio(
    "📊 Select View Mode",
    ["Leads", "Campaign Conversation", "Primary Sales Leads"]
)

# ==================== LEADS ====================
if view_mode == "Leads":
    selected_country = st.sidebar.selectbox(
        "🌍 Country", list(country_sheets.keys())
    )
    selected_intern = st.sidebar.selectbox(
        "👤 Intern/State", list(country_sheets[selected_country].keys())
    )

    # for All Data, we already have a full CSV‐export URL pointing at Master_<Country>
    if selected_intern == "All Data":
        url = country_sheets[selected_country][selected_intern]
    else:
        # pull the base URL for that intern, extract its sheet ID, and point at the Data Sheet
        base = country_sheets[selected_country][selected_intern]
        sheet_id = base.split("/d/")[1].split("/")[0]
        url = (
            f"https://docs.google.com/spreadsheets/d/{sheet_id}"
            f"/gviz/tq?tqx=out:csv&sheet=Data%20Sheet"
        )

    st.subheader(f"📄 Leads Data — {selected_country} → {selected_intern}")
    try:
        df = load_csv_from_url(url)
        st.success(f"✅ Loaded {len(df)} entries.")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Could not load data: {e}")

# ==================== CAMPAIGN CONVERSATION ====================
elif view_mode == "Campaign Conversation":
    selected_country = st.sidebar.selectbox(
        "🌍 Country", list(conversation_sheets.keys())
    )
    selected_month = st.sidebar.selectbox("🗓️ Month", month_tabs)

    sheet_id = conversation_sheets[selected_country]
    encoded_month = selected_month.replace(" ", "%20")
    url = (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        f"/gviz/tq?tqx=out:csv&sheet={encoded_month}"
    )

    st.subheader(f"💬 Conversations — {selected_country} ({selected_month})")
    try:
        df = load_csv_from_url(url)
        st.success(f"✅ Loaded {len(df)} conversations.")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Could not load conversation data: {e}")

# ==================== PRIMARY SALES LEADS ====================
else:
    st.subheader("📈 Primary Sales Leads (Fixed Sheet)")
    try:
        df = load_csv_from_url(primary_sales_url)
        st.success(f"✅ Loaded {len(df)} entries.")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Could not load primary sales data: {e}")
