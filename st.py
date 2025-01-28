import streamlit as st

# Page configuration
images = st.Page(
    "app_folder/st_app.py", title="Sat Image Change Detector", icon=":material/satellite_alt:", default=True, 
)
about = st.Page(
    "app_folder/About.py", title="About", icon=":material/waving_hand:",
)

pg = st.navigation([images, about])
pg.run()