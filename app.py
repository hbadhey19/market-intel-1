import streamlit as st
import streamlit.components.v1 as components
from fredapi import Fred

# 1. Connect to FRED
fred = Fred(api_key='2ff3cffffc309fd50e25cc02603af7cf')

def get_data():
    try:
        return {
            "vix": fred.get_series('VIXCLS').iloc[-1],
            "spx": fred.get_series('SP500').iloc[-1],
            "hy":  fred.get_series('BAMLH0A0HYM2').iloc[-1],
            "y10": fred.get_series('DGS10').iloc[-1]
        }
    except:
        return None

# 2. Fetch the numbers
live = get_data()

# 3. Read your HTML file
with open("live_market_dashboard_FRED_4.html", "r") as f:
    html = f.read()

# 4. DATA INJECTION: Replace the dashes with real numbers
if live:
    # Hide the error and setup banners forever
    html = html.replace('class="setup-banner"', 'style="display:none;"')
    html = html.replace('id="err-banner"', 'style="display:none;"')
    
    # Fill in the stats
    html = html.replace('id="v-vix">—', f'id="v-vix">{live["vix"]:.2f}')
    html = html.replace('id="v-spx">—', f'id="v-spx">{live["spx"]:,.0f}')
    html = html.replace('id="v-hy">—', f'id="v-hy">{live["hy"]:.2f}%')
    html = html.replace('id="v-y10">—', f'id="v-y10">{live["y10"]:.2f}%')

# 5. Launch
components.html(html, height=1200, scrolling=True)
