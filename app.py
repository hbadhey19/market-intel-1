import streamlit as st
import streamlit.components.v1 as components
from fredapi import Fred

# 1. Setup FRED
fred = Fred(api_key='2ff3cffffc309fd50e25cc02603af7cf')

def get_fred_data():
    try:
        # Fetching the exact series from your dashboard
        return {
            "vix": fred.get_series('VIXCLS').iloc[-1],
            "sp500": fred.get_series('SP500').iloc[-1],
            "hy_oas": fred.get_series('BAMLH0A0HYM2').iloc[-1],
            "yield10": fred.get_series('DGS10').iloc[-1]
        }
    except Exception as e:
        st.error(f"FRED Fetch Error: {e}")
        return None

# 2. Get the Data
data = get_fred_data()

# 3. Read your HTML file
with open("live_market_dashboard_FRED_4.html", "r") as f:
    html_content = f.read()

# 4. INJECT the data into the HTML
if data:
    # This hides the "setup-banner" since we already have the data
    html_content = html_content.replace('class="setup-banner"', 'class="setup-banner hidden"')
    
    # This replaces the empty placeholders in your HTML with real numbers
    html_content = html_content.replace('id="v-vix">—', f'id="v-vix">{data["vix"]:.2f}')
    html_content = html_content.replace('id="v-spx">—', f'id="v-spx">{data["sp500"]:,.0f}')
    html_content = html_content.replace('id="v-hy">—', f'id="v-hy">{data["hy_oas"]:.2f}%')
    html_content = html_content.replace('id="v-y10">—', f'id="v-y10">{data["yield10"]:.2f}%')

# 5. Display the Dashboard
components.html(html_content, height=1500, scrolling=True)
