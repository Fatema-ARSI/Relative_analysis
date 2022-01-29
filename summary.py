import pandas as pd
import numpy as np
import streamlit as st

from PIL import Image

import yfinance as yf
from yahoofinancials import YahooFinancials
from yahoo_fin import stock_info as si
import pandas_datareader as web

import requests

#add an import to Hydralit
from hydralit import HydraHeadApp


#sidebar section
df=pd.read_csv('company_stats.csv')

#SIDEBAR
df
