import pandas as pd
import numpy as np
import streamlit as st

from PIL import Image

import yfinance as yf


import requests

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class company_analysis(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):

    #-------------------existing untouched code------------------------------------------







        #sidebar section
        df=pd.read_csv('company_stats.csv')
        drop=np.where(df['Ticker']=="GOOG")
        df.drop((206),inplace=True)


        #SIDEBAR

        sorted_sector_unique=sorted(df['Sector'].unique())
        selected_sector=st.sidebar.selectbox('Sector',sorted_sector_unique,index=7)

        #sidebar section
        industry=df[(df['Sector']==selected_sector)]
        sorted_industry_unique=sorted(industry['Industry'].unique())
        selected_industry=st.sidebar.selectbox('Industry',sorted_industry_unique)
        #sidebar section
        company=df[(df['Industry']==selected_industry)]
        sorted_comp_unique = sorted( company['Company'] )
        selected_comp = st.sidebar.selectbox('Stock', sorted_comp_unique)
        stock=df.loc[df['Company']==selected_comp,'Ticker']
        stock=stock.to_string(header=False,index=False)


        #tickerData=yf.Ticker(stock)
        #string_logo='<img src=%s>' % tickerData.info['logo_url']
        #st.markdown(string_logo,unsafe_allow_html=True)

        string_name=selected_comp
        st.header('*%s*' % string_name)


        #peer group
        api='KwhdgIMbfV_cfyMTVQ_524WpmcVTXStN'

        api_url=f'https://api.polygon.io/v1/meta/symbols/{stock}/company?apiKey={api}'
        data=requests.get(api_url).json()
        peer_co=data ['similar']
        peer_co=peer_co+[stock]


        #under_over value

        def to_value(ratio):
            ratio=float(ratio)
            if ratio<=1.00:
                return '-Under Valued'
            elif ratio==1.00:
                return 'Fair Valued'
            else:
                return 'Over Valued'


        df['Value_label']=df['PEG Ratio'].apply(to_value)

        df["Value_percent"]=abs(df["PEG Ratio"]-1)*100

        # Custom function for rounding values

        def round_value(input_value):
            if input_value.values > 1:
                a = float(round(input_value, 2))
            else:
                a = float(round(input_value, 3))
            return a

        compet=df[ (df['Ticker'].isin(peer_co)) ]
        st.markdown(""" - #### Comparable Companies """)
        st.write("Select a company from the below dropdown list to view if the company is Over Valued or Under Valued ")
        selected_stock = st.selectbox("",compet)



        col1,col2,col3=st.columns(3)

        watchlst=df.loc[df['Company']==selected_stock,'Ticker']
        watchlst=watchlst.to_string(header=False,index=False)

        col_df=df.loc[df['Ticker']==watchlst]
        col_price = f'{float(round_value(col_df.Value_percent))}%'
        col_label=col_df['Value_label']
        col_label=col_label.to_string(header=False,index=False)

        col2.metric(watchlst,col_price,col_label)

        st.write(""" - In the above metrics, I have used PEG Ratio is also known as Price/Earnings to Growth Ratio which allow user to determine the valuation of the stock while considering the growth rate of the company's earnings.""")

        st.write(""" - A good PEG Ratio is 1.0 i.e. if the company has the PEG ratio of 1.0 then the company is traded at its fair value. On the other hand, if the company has the PEG ratio of 1.37 then the company is traded above its fair valued by 37% and vice a versa.""")

        st.write(

        " ###### In this case " + str(selected_stock) + " is " + str(col_label) + " by " + str(col_price)

        )

        st.markdown("""  - #### Statistical Data """)

        #DataFrame


        hide_table_index="""
        <style>
        tbody th {display:none}
        .blank {display:none}
        </style>
        """

        st.markdown(hide_table_index, unsafe_allow_html=True)
        st.write('Data Dimension: ' + str(compet.shape[0]) + ' rows and ' + str(compet.shape[1]) + ' columns.')


        st.table(compet[["Company","Ticker","Current Share Price","52 Weeks High","Equity Value","Enterprise Value","Beta","LTM Sales","Debt/Equity","EV/Sales","P/E","EBITDA","EV/EBITDA","PEG Ratio"]])

        st.write("The data above is collected as of 26/01/2022")

        #Summary
        st.markdown("""  - #### Company Analysis """)


        sector=pd.read_csv('summary_stock.csv')
        st.write(' ###### Opportunities for ' + str(selected_stock)+':')

        opp=sector.loc[sector['Ticker']==watchlst,'Opportunities']
        opp=list(opp)
        
        for i in range(len(opp)):
            st.write(opp[i])

        st.write(' ###### Threats for ' + str(selected_stock)+':')

        threat=sector.loc[sector['Ticker']==watchlst,'Threats']
        threat=list(threat)
        for i in range(len(threat)):
            st.write(threat[i])


        #-------------------existing untouched code------------------------------------------
