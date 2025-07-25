import hydralit as hy
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import plotly.graph_objects as go
#from home import home_page
#from screener import company_analysis
#from sector import sector_analysis
#from summary_sect import sector_summary

#this is the host application, we add children to it and that's it!
app = hy.HydraApp(title='Relative Analysis', hide_streamlit_markers=True)

@app.addapp(is_home=True)
def home_page():

    #-------------------existing untouched code------------------------------------------

    image = Image.open('logo.jpg')
    st.image(image, width = 500)
    st.title('Relative Analysis')
    st.markdown("""
    **This app showcases stock valuation and sector analysis.**

    Please use the navigation bar to explore the following sections:

    * **Company Analysis** – for analyzing comparable companies
    * **Sector Analysis** – for a detailed view of each sector
    * **Sector Opportunities and Challenges** – for insights into sector trends and industry threats in 2022

    **Note:** This app is intended for informational purposes only.

    **Python libraries used**: `Yahoo Finance`, `Pandas`, `Streamlit`, `Plotly`,`Hydralit`
    """)

    #-------------------existing untouched code------------------------------------------

@app.addapp(title= "Company Analysis")
def Company_Analysis():

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
        #string_logo='<img src=%s>' % tickerData.info['symbol']
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
        st.write("Choose a company from the list below to determine if it is overvalued or undervalued." )
        selected_stock = st.selectbox("",compet)



        col1,col2,col3=st.columns(3)

        watchlst=df.loc[df['Company']==selected_stock,'Ticker']
        watchlst=watchlst.to_string(header=False,index=False)

        col_df=df.loc[df['Ticker']==watchlst]
        col_price = f'{float(round_value(col_df.Value_percent))}%'
        col_label=col_df['Value_label']
        col_label=col_label.to_string(header=False,index=False)

        col2.metric(watchlst,col_price,col_label)

        st.write(""" **In the above metrics, I have included the PEG ratio (Price/Earnings to Growth ratio), which helps assess a stock's valuation while accounting for the company's earnings growth rate.** """)

        st.markdown("""

        A **PEG ratio of 1.0** typically indicates that a stock is fairly valued.

        * If a company's PEG ratio is **above 1.0**, it may be **overvalued** relative to its growth.
        * If it's **below 1.0**, it may be **undervalued**.

        For example, a PEG ratio of **1.37** suggests the company is trading at a **37% premium** to its fair value.

        """)

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

@app.addapp(title="Sector Analysis")
def sector_analysis():

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

        #def load_data(url):
            #html=pd.read_html(url, header=0)
            #data=html[0]
            #return data


        #graph code
        sect_wght=pd.read_excel(r'us-sector-weightings-s&p500.xlsx')
        #sect_wght=load_data(url='https://siblisresearch.com/data/us-sector-weightings/')
        #sect_wght.drop([11],axis=0,inplace=True)
        #sect_wght.drop(['12/31/2016'],axis=1,inplace=True)

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

        st.write(""" **Diversifying a stock portfolio should include consideration of both sector and industry diversification.** """)
        st.write(""" Some investment strategies even recommend maintaining a balanced allocation across sectors, as any sector has the potential to outperform in a given year. In recent years, certain sectors and industries have outperformed others, and this is now reflected in the composition of the S&P 500. Understanding the **sector weightings** within the S&P 500 is important, as the index may not always represent the top-performing sectors in any given year.  """)
        st.write("""  """)
        st.write("""  """)
        st.markdown("""  In the pie chart below, you can review the **sector-wise weight distribution of the S&P 500 over the years:** """)



        selected_year=st.selectbox('Select a Year',year)

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



@app.addapp(title= "Sector Opportunities and Challenges")
def sector_summary():

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

        st.write(' ##### Opportunities for ' + str(selected_industry)+':')
        opp=df.loc[df['Industry']==selected_industry,'Trend']
        opp=list(opp)

        for i in range(len(opp)):
            st.write(opp[i])
        st.write("")
        st.write("")

        st.write('##### Challenges for ' + str(selected_industry2)+':')

        threat=df2.loc[df2['Industry']==selected_industry2,'Challenges']
        threat=list(threat)

        for i in range(len(threat)):
            st.write(threat[i])
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        #-------------------existing untouched code------------------------------------------




#Run the whole lot
app.run()

st.info('Coded by 👩🏻‍💻[Fatema ARSIWALA](https://www.linkedin.com/in/fatemaarsi/)')
st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)
