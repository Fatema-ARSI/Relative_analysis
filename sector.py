import pandas as pd
import streamlit as st
import openpyxl

import plotly.graph_objects as go



#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class sector_analysis(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):

        #-------------------existing untouched code------------------------------------------





        #SIDEBAR CODE

        st.sidebar.header('User Input Features')

        df=pd.read_csv('company_stats.csv')

        #sector
        sorted_sector_unique=sorted(df['Sector'].unique())
        selected_sector=st.sidebar.selectbox('Sector',sorted_sector_unique,index=7)

        #industry
        industry=df[(df['Sector']==selected_sector)]
        sorted_industry_unique=sorted(industry['Industry'].unique())
        selected_industry=st.sidebar.multiselect('Industry',sorted_industry_unique,sorted_industry_unique)


        #main page

        def load_data(url):
            html=pd.read_html(url, header=0)
            data=html[0]
            return data


        #graph code
        sect_wght=pd.DataFrame()
        sect_wght=load_data(url='https://siblisresearch.com/data/us-sector-weightings/')
        sect_wght.drop([11],axis=0,inplace=True)
        sect_wght.drop(['12/31/2016'],axis=1,inplace=True)


        sect_wght['12/31/2021']=sect_wght['12/31/2021'].apply(lambda x:str(x).replace('%',''))
        sect_wght['12/31/2021']=sect_wght['12/31/2021'].apply(lambda x:float(x))

        sect_wght['12/31/2020']=sect_wght['12/31/2020'].apply(lambda x:str(x).replace('%',''))
        sect_wght['12/31/2020']=sect_wght['12/31/2020'].apply(lambda x:float(x))

        sect_wght['12/31/2019']=sect_wght['12/31/2019'].apply(lambda x:str(x).replace('%',''))
        sect_wght['12/31/2019']=sect_wght['12/31/2019'].apply(lambda x:float(x))

        sect_wght['12/31/2018']=sect_wght['12/31/2018'].apply(lambda x:str(x).replace('%',''))
        sect_wght['12/31/2018']=sect_wght['12/31/2018'].apply(lambda x:float(x))


        sect_wght['12/31/2017']=sect_wght['12/31/2017'].apply(lambda x:str(x).replace('-','0'))
        sect_wght['12/31/2017']=sect_wght['12/31/2017'].apply(lambda x:str(x).replace('%',''))
        sect_wght['12/31/2017']=sect_wght['12/31/2017'].apply(lambda x:float(x))

        sect_wght['GICS Sector']=sect_wght['GICS Sector'].apply(lambda x:str(x).replace('Communications','Communication Services'))

        #years
        year=sect_wght.columns
        year=year.drop('GICS Sector')

        st.write(""" - Any attempt to diversify the stock portfolio should include some attempt at diversification according to sector and industry. In fact, some investment strategies suggest a perfect balance of sectors, because any asector can be the best-performing group in any given year.""")
        st.write(""" - In recent years, certain secors and industries hav performed better than others, and that is now reflected in the makeup of the S&P 500.""")
        st.write(""" - The weighting of the S&P 500 should be important because the index does not always represent the types of companies performing the best in any given year. """)
        st.markdown("""  ###### In the pie-chart below, we can review the weightage of every sector in S&P 500 over the years: """)



        selected_year=st.selectbox('Select Year',year)

        labels=sect_wght["GICS Sector"]
        values=sect_wght[selected_year]

        pull=[]

        for sector in labels:
            if sector==selected_sector:
                pull.append(0.2)
            else:
                pull.append(0)



        #plot show

        fig=go.Figure(data=[go.Pie(labels=labels,values=values,pull=pull)])
        st.plotly_chart(fig,use_container_width=True)




        #financial data by sector
        st.markdown("""  - #### Statistical Data """)

        sect_data=pd.read_excel(r'pedata.xls')

        # Filtering data
        df_selected_industry = sect_data[ (sect_data['Industry'].isin(selected_industry)) ]

        hide_table_index="""
        <style>
        tbody th {display:none}
        .blank {display:none}
        </style>
        """

        st.markdown(hide_table_index, unsafe_allow_html=True)

        st.write('Data Dimension: ' + str(df_selected_industry.shape[0]) + ' rows and ' + str(df_selected_industry.shape[1]) + ' columns.')
        st.table(df_selected_industry[['Industry Group','Number of firms','Current PE','Trailing PE','Forward PE','Aggregate Mkt Cap/ Net Income (all firms)','Expected growth in EPS - next 5 years','PEG Ratio']])





        #-------------------existing untouched code------------------------------------------
