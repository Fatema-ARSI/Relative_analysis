import streamlit as st
from PIL import Image
import pandas as pd

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class home_page(HydraHeadApp):


    def run(self):
        #sidebar section
        # Main panel
        image = Image.open('logo.jpg')
        st.image(image, width = 1000)
        st.title('Relative Analysis')
        st.markdown("""
        This app showcase the Stock Valuation and Sector analysis.

        Please select **Company analysis** for comparable companies analysis, **Sector Analysis** for sector analysis and **Sector Opportunity and Challenges** for sector trends and threats for industries in 2022 from the navigation bar.

        --- Note: This is app can be used for information purpose only.
        * Python libraries: `Yahoo Finance`, `Pandas`, `Streamlit`, `Plotly`,`Hydralit`
        """)
