import streamlit as st
import streamlit.components.v1 as components

# Set the page to wide mode to match your professional layout
st.set_page_config(layout="wide", page_title="Market Intelligence")

# This reads your exact Claude-designed HTML file
try:
    with open("live_market_dashboard_FRED_4.html", "r") as f:
        html_code = f.read()

    # This displays the HTML exactly as it looks in your file
    components.html(html_code, height=1500, scrolling=True)

except FileNotFoundError:
    st.error("Error: 'live_market_dashboard_FRED_4.html' not found in the repository.")
except Exception as e:
    st.error(f"An error occurred: {e}")
