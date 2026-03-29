import streamlit as st
from fredapi import Fred
import os
import ssl
from bs4 import BeautifulSoup

# --- 1. BYPASS SECURITY ERRORS ---
os.environ['CURL_CA_BUNDLE'] = ''
ssl._create_default_https_context = ssl._create_unverified_context

# --- 2. CONNECT TO FRED ---
fred = Fred(api_key='2ff3cffffc309fd50e25cc02603af7cf')

def get_live_data():
    # Fetch the exact data points from your dashboard
    return {
        "vix": fred.get_series('VIXCLS').iloc[-1],
        "spx": fred.get_series('SP500').iloc[-1],
        "hy_oas": fred.get_series('BAMLH0A0HYM2').iloc[-1],
        "yield10": fred.get_series('DGS10').iloc[-1],
        "sahm": fred.get_series('SAHMREALTIME').iloc[-1]
    }

# --- 3. THE EXTRACTION & INJECTION ---
try:
    live = get_live_data()
    
    # Python reads your existing Claude HTML file
    with open("live_market_dashboard_FRED_4.html", "r") as f:
        html_doc = f.read()

    # We use BeautifulSoup to target specific elements by their IDs
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Update the "Signal Board" values in your HTML
    if soup.find(id="v-vix"): soup.find(id="v-vix").string = f"{live['vix']:.2f}"
    if soup.find(id="v-hy"): soup.find(id="v-hy").string = f"{live['hy_oas']:.2f}%"
    if soup.find(id="v-sahm"): soup.find(id="v-sahm").string = f"{live['sahm']:.2f}"

    # --- 4. LAUNCH THE DASHBOARD ---
    st.components.v1.html(str(soup), height=1200, scrolling=True)

except Exception as e:
    st.error(f"Waiting for live market feed... {e}")