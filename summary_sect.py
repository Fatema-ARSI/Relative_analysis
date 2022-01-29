import pandas as pd

import streamlit as st
import openpyxl

import plotly.graph_objects as go



#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class sector_summary(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):

        #-------------------existing untouched code------------------------------------------
        df=pd.read_excel('Sector_trends.xlsx')
        df.dropna(inplace=True)
        df2=pd.read_excel('Sector_threats.xlsx')

        #SIDEBAR

        st.sidebar.header('User Input Features')
        sorted_industry_unique=df['Industry'].unique()
        selected_industry=st.sidebar.selectbox('Industry Oppotunity',sorted_industry_unique,index=60)
        sorted_industry_unique2=df2['Industry'].unique()
        selected_industry2=st.sidebar.selectbox('Industry Challenges',sorted_industry_unique2,index=26)

        st.write(' ###### Opportunities for ' + str(selected_industry)+':')
        opp=df.loc[df['Industry']==selected_industry,'Trend']
        opp=list(opp)
        st.write('\n'.join(opp))

        st.write('###### Challenges for ' + str(selected_industry2)+':')

        threat=df2.loc[df2['Industry']==selected_industry2,'Challenges']
        threat=list(threat)
        st.write('\n'.join(threat))
