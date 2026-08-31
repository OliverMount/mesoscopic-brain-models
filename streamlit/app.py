# Streamlit app making

import streamlit as st

from tabs.introduction import introduction_tab
from tabs.parameters import parameters_tab
from tabs.run import run_tab
from tabs.reproduce import run_reproduce

st.set_page_config(
    page_title="Jansen-Rit Simulator",
    layout="wide"
)

tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Introduction",
    "⚙️ Parameters",
    "▶️ Run Simulation",
    "🔬 Reproducibility"
])

with tab1:
    introduction_tab()

with tab2:
    parameters_tab()
    
with tab3:
    run_tab()

with tab4:
    run_reproduce()
