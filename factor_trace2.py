# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 02:41:08 2022

@author: Fabian
"""
from datetime import date
import investpy
import pandas as pd
from datetime import datetime, timedelta
d = datetime.today() - timedelta(days=30)

datam = investpy.get_etf_historical_data(etf='Amundi MSCI Europe Momentum Factor', country='france', from_date='01/01/2010', to_date=date.today().strftime('%d/%m/%Y'))
datam["Return90"]=datam["Close"]/datam["Close"].shift(90)-1
datam["Return15"]=datam["Close"]/datam["Close"].shift(15)-1
datam["ETF"]="MSCI Europe Momentum"
datam=datam[datam.index.strftime('%Y/%m/%d') >d.strftime('%Y/%m/%d')]

datav = investpy.get_etf_historical_data(etf='Amundi ETF MSCI Europe Value UCITS', country='france', from_date='01/01/2010', to_date=date.today().strftime('%d/%m/%Y'))
datav["Return90"]=datav["Close"]/datav["Close"].shift(90)-1
datav["Return15"]=datav["Close"]/datav["Close"].shift(15)-1
datav["ETF"]="MSCI Europe Value"
datav=datav[datav.index.strftime('%Y/%m/%d') >d.strftime('%Y/%m/%d')]

dataq = investpy.get_etf_historical_data(etf='Amundi MSCI Europe Quality Factor', country='france', from_date='01/01/2010', to_date=date.today().strftime('%d/%m/%Y'))
dataq["Return90"]=dataq["Close"]/dataq["Close"].shift(90)-1
dataq["Return15"]=dataq["Close"]/dataq["Close"].shift(15)-1
dataq["ETF"]="MSCI Europe Quality"
dataq=dataq[dataq.index.strftime('%Y/%m/%d') >d.strftime('%Y/%m/%d')]

data = pd.concat([datam, datav,dataq])
data["Date"]=data.index.strftime("%m%d")
df=data

#Dynamic plotly
import plotly.graph_objects as go
# Base plot
fig = go.Figure(
    layout=go.Layout(
        updatemenus=[dict(type="buttons", direction="right", x=0.9, y=1.16), ],
        template='plotly_white',
        xaxis=dict(range=[-0.2, 0.2],
                   autorange=False, tickwidth=2,
                   title_text="90 Days Return"),
        yaxis=dict(range=[-0.2, 0.2],
                   autorange=False,
                   title_text="15 Days Return"),
        title="Equity Factors Momentum",
    ))

# Add traces
init = 1
fig.add_hline(0, line_width=1, line_dash="solid", line_color="grey")
fig.add_vline(0, line_width=1, line_dash="solid", line_color="grey")
fig.add_trace(
    go.Scatter(x=datam['Return90'][:init],
               y=datam['Return15'][:init],
               name="Momentum",
               visible=True,line_shape='spline',
               line=dict(color="#04103b", dash="dash")))

fig.add_trace(
    go.Scatter(x=datav['Return90'][:init],
               y=datav['Return15'][:init],
               name="Value",
               visible=True,line_shape='spline',
               line=dict(color="#dd0400", dash="dash")))

fig.add_trace(
    go.Scatter(x=dataq['Return90'][:init],
               y=dataq['Return15'][:init],
               name="Quality",
               visible=True,line_shape='spline',
               line=dict(color="#3b5171", dash="dash")))

# Animation
fig.update(frames=[
    go.Frame(
        data=[
            go.Scatter(x=datam['Return90'][:k], y=datam['Return15'][:k]),
            go.Scatter(x=datav['Return90'][:k], y=datav['Return15'][:k]),
            go.Scatter(x=dataq['Return90'][:k], y=dataq['Return15'][:k])
            ]
    )
    for k in range(init, len(datam)+1)])

# Extra Formatting
fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=10)
fig.update_yaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=1)
fig.update_layout(yaxis_tickformat=',')
fig.update_layout(legend=dict(x=0, y=1.1), legend_orientation="h")

# Buttons
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="Play",
                        method="animate",
                    args=[None, {"frame": {"duration": 1000}}])
                #dict(label="Momentum",
                #    method="update",
                #    args=[{"visible": [False, True]},
                #          {"showlegend": True}]),
                #dict(label="Value",
                #    method="update",
                #    args=[{"visible": [True, False]},
                #          {"showlegend": True}]),
                #dict(label="Quality",
                #    method="update",
                #    args=[{"visible": [True, False]},
                #          {"showlegend": True}]),
                #dict(label="All",
                #    method="update",
                #    args=[{"visible": [True, True, True]},
                #          {"showlegend": True}]),
            ]))])
fig.layout.xaxis.tickformat = ',.1%'     
fig.layout.yaxis.tickformat = ',.1%'    
fig.show()
fig.write_html("C:/FS/quantamental_platform/Publications/Factor_Performance_Monitoring/index.html")
