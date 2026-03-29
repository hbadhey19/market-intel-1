import streamlit as st
import streamlit.components.v1 as components
from fredapi import Fred

# 1. Setup FRED with your key
fred = Fred(api_key='2ff3cffffc309fd50e25cc02603af7cf')

def get_fred_data():
    try:
        return {
            "vix": fred.get_series('VIXCLS').iloc[-1],
            "spx": fred.get_series('SP500').iloc[-1],
            "hy":  fred.get_series('BAMLH0A0HYM2').iloc[-1],
            "y10": fred.get_series('DGS10').iloc[-1]
        }
    except:
        return None

# 2. Get the Data
live = get_fred_data()

# 3. Read the HTML file
with open("live_market_dashboard_FRED_4.html", "r") as f:
    html = f.read()

# 4. DATA INJECTION: Force hide the error and insert numbers
if live:
    # This manually hides the banner that is causing your error message
    html = html.replace('class="setup-banner"', 'style="display:none;"')
    html = html.replace('id="err-banner"', 'style="display:none;"')
    
    # This fills in the dashes (—) with the real numbers from FRED
    html = html.replace('id="v-vix">—', f'id="v-vix">{live["vix"]:.2f}')
    html = html.replace('id="v-spx">—', f'id="v-spx">{live["spx"]:,.0f}')
    html = html.replace('id="v-hy">—', f'id="v-hy">{live["hy"]:.2f}%')
    html = html.replace('id="v-y10">—', f'id="v-y10">{live["y10"]:.2f}%')

# 5. Display the cleaned dashboard
components.html(html, height=1200, scrolling=True)
