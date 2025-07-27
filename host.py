import hydralit as hy
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import plotly.graph_objects as go
import base64
#from home import home_page
#from screener import company_analysis
#from sector import sector_analysis
#from summary_sect import sector_summary

#this is the host application, we add children to it and that's it!
app = hy.HydraApp(title='Relative Analysis', hide_streamlit_markers=True)

@app.addapp(is_home=True)
def home_page():

    #-------------------existing untouched code------------------------------------------

    st.markdown("""
           <div style="text-align: center;">
           <h1 style="color:#0A1E3F;"> Relative Analysis </h1>
           </div>
           """, unsafe_allow_html=True)
    
    # --- logo ---
    # Read and encode the logo image to base64
    with open("logo.jpg", "rb") as file:
        contents = file.read()
    data_url = base64.b64encode(contents).decode("utf-8")

    # Use HTML with centered div to display the image
    st.markdown(
        f'<div style="text-align:center;"><img src="data:image/jpg;base64,{data_url}" alt="logo" width="500"></div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    ### Overview

    This application provides **comprehensive stock valuation and sector analysis**, designed to assist finance professionals and enthusiasts in making informed decisions.

    Navigate through the app using the menu to explore:

    - **Company Analysis**: Assess valuation metrics and comparable companies.
    - **Sector Analysis**: Gain insights into sector-level financial metrics and trends.
    - **Sector Opportunities & Challenges**: Understand sector-specific growth drivers and risks.

    """)
    
    # --- Disclaimer ---
    st.markdown("""
    ### ⚠️ Disclaimer

    This tool is intended for **informational purposes only** and does not constitute investment advice.
    """)

    # --- Footer ---
    st.markdown("""
    ---
    **🔧 Powered by:**
       `Yahoo Finance` · `Pandas` · `Streamlit` · `Plotly` · `Hydralit` 

    """)
    st.write("")

    #-------------------existing untouched code------------------------------------------

@app.addapp(title= "Company Analysis")
def Company_Analysis():
    
    #-------------------existing untouched code------------------------------------------
    
    #sidebar section
    df=pd.read_csv('company_stats.csv')
    drop=np.where(df['Ticker']=="GOOG")
    df.drop((206),inplace=True)


    #SIDEBAR
    st.sidebar.header(" Select Company Filters")

    # Sector selection
    sorted_sector_unique=sorted(df['Sector'].unique())
    selected_sector=st.sidebar.selectbox('Sector',sorted_sector_unique,index=7)

    #Industry selection filtered by sector
    industry = df[df['Sector'] == selected_sector]
    sorted_industry_unique = sorted(industry['Industry'].unique())
    selected_industry = st.sidebar.selectbox('Industry', sorted_industry_unique)

    # Company selection filtered by industry
    company = df[df['Industry'] == selected_industry]
    sorted_comp_unique = sorted(company['Company'])
    selected_comp = st.sidebar.selectbox('Company', sorted_comp_unique)

    stock = df.loc[df['Company'] == selected_comp, 'Ticker'].values[0]

    # --- MAIN PAGE ---
    string_name=selected_comp
    st.header('*%s*' % string_name)

    # Fetch peer companies from Polygon API
    api_key = 'KwhdgIMbfV_cfyMTVQ_524WpmcVTXStN'
    api_url = f'https://api.polygon.io/v1/meta/symbols/{stock}/company?apiKey={api_key}'
    response = requests.get(api_url).json()
    peer_co = response.get('similar', [])
    peer_co.append(stock)


    # Define valuation helper functions
    def to_value(ratio):
        ratio = float(ratio)
        if ratio < 1.0:
            return 'Under Valued'
        elif ratio == 1.0:
            return 'Fair Valued'
        else:
            return 'Over Valued'
    
    df['Value_label'] = df['PEG Ratio'].apply(to_value)
    df['Value_percent'] = abs(df['PEG Ratio'] - 1) * 100
    
    def round_value(val):
        return round(val, 2) if val > 1 else round(val, 3)
        
    # Prepare comparable companies dataframe
    compet = df[df['Ticker'].isin(peer_co)]
    
    st.markdown("#### Comparable Companies")
    st.write("Choose a company from the list below to determine valuation status.")
    
    selected_stock = st.selectbox("", compet['Company'].tolist())
    watchlst = df.loc[df['Company'] == selected_stock, 'Ticker'].values[0]
    
    col_df = df.loc[df['Ticker'] == watchlst].iloc[0]
    col_price = f"{round_value(col_df['Value_percent'])}%"
    col_label = col_df['Value_label']
    
    col1, col2, col3 = st.columns(3)
    col2.metric(label=watchlst, value=col_price, delta=col_label)
    
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

    
    # Statistical Data Table
    
    st.markdown("#### Statistical Data")

    
    hide_table_index = """
    <style>
    tbody th {display:none}
    .blank {display:none}
    </style>"""
    
    st.markdown(hide_table_index, unsafe_allow_html=True)
    
    st.write(f"Data Dimension: {compet.shape[0]} rows and {compet.shape[1]} columns.")
    
    st.table(compet[[
        "Company", "Ticker", "Current Share Price", "52 Weeks High", "Equity Value",
        "Enterprise Value", "Beta", "LTM Sales", "Debt/Equity", "EV/Sales",
        "P/E", "EBITDA", "EV/EBITDA", "PEG Ratio"]])
    
    st.write("Data is as of 26/01/2022")
    
    # Company Analysis - Opportunities and Threats
    st.markdown("#### Company Analysis")
    sector_summary = pd.read_csv('summary_stock.csv')
    
    st.write(f"###### Opportunities for {selected_stock}:")
    opportunities = sector_summary.loc[sector_summary['Ticker'] == watchlst, 'Opportunities'].tolist()
    for opp in opportunities:
        st.write(f" {opp}")
        
    st.write(f"###### Threats for {selected_stock}:")
    threats = sector_summary.loc[sector_summary['Ticker'] == watchlst, 'Threats'].tolist()
    for threat in threats:
        st.write(f" {threat}")
        

        #-------------------existing untouched code------------------------------------------

@app.addapp(title="Sector Analysis")
def sector_analysis():

    #-------------------existing untouched code------------------------------------------


    #SIDEBAR CODE

        st.sidebar.header("Filter Parameters")

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
    
        st.markdown("#### 🧭 Sector Weighting in the S&P 500")


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

        st.sidebar.header('Select Industry')
        sorted_industry_unique=df['Industry'].unique()
        selected_industry=st.sidebar.selectbox('Industry Oppotunity',sorted_industry_unique,index=60)
        sorted_industry_unique2=df2['Industry'].unique()
        selected_industry2=st.sidebar.selectbox('Industry Challenges',sorted_industry_unique2,index=26)

        ## main page
        st.markdown("#### 🌐 Industry-Specific Trends & Challenges")
        st.markdown(""" Explore **key opportunities** and **emerging challenges** faced by different industries based on qualitative research and expert insights.""")

        st.markdown(f"💡 Opportunities in **{selected_industry}**")

        st.write(' ##### Opportunities for ' + str(selected_industry)+':')
    
        opps=df.loc[df['Industry']==selected_industry,'Trend'].tolist()
    
        for i, item in enumerate(opps, 1):
            st.markdown(f"""
                <div style="background-color:#e8f5e9; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <b>📌 Opportunity {i}:</b> {item}
                </div>
            """, unsafe_allow_html=True)
            
        # Spacer
        st.markdown("---")

        st.markdown(f"⚠️ Challenges in **{selected_industry2}**")

        st.write('##### Challenges for ' + str(selected_industry2)+':')

        threat=df2.loc[df2['Industry']==selected_industry2,'Challenges'].tolist()

        for i, item in enumerate(challenges, 1):
            st.markdown(f"""
                 <div style="background-color:#fff3e0; padding:15px; border-radius:10px; margin-bottom:10px;">
                     <b>🛑 Challenge {i}:</b> {item}
                 </div>
            """, unsafe_allow_html=True)
            
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
