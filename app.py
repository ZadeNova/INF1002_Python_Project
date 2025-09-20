import streamlit as st

pg = st.navigation([st.Page("Main.py"), st.Page("Networth Calculator.py")])
pg.run()