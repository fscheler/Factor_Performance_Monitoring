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
datav["ETF"]="MSCI Europe Valur"
datav=datav[datav.index.strftime('%Y/%m/%d') >d.strftime('%Y/%m/%d')]

data = pd.concat([datam, datav])




#Static plotly
import plotly.express as px

fig = px.line(data, x="Return90", y="Return15", color="ETF",text=data.index.strftime("%b %d"))
fig.update_traces(textposition="bottom right")
fig.show(auto_open=True)
fig.write_html("C:/FS/quantamental_platform/Publications/Factor_Performance_Monitoring/file.html")

import plotly.express as px

fig=px.line(data, x='Return90', y='Return15', color='ETF', symbol="ETF",
            animation_frame="Date", animation_group="ETF")

data["Date"]=data.index.strftime("%m%d")
fig = px.line(data, x="Return90", y="Return15", color="ETF",
  animation_frame="Date", animation_group="ETF",
           hover_name="Return90", color_discrete_sequence=["#04103b"],
           log_x=False,title='Equity Factors Momentum',labels={"time": "","rate": "",},template='plotly_white',
           range_x=[-0.2,0.2], range_y=[-0.2,0.2])
fig.layout.xaxis.tickformat = ',.1%'     
fig.layout.yaxis.tickformat = ',.1%'     
fig.show()
# lineas and markers on first display
fig.for_each_trace(lambda t: t.update(mode = 'lines+markers'))

# lineas and markers on animation frames
for fr in fig.frames:
    for d in fr.data:
        d.update(mode='markers+lines')
        
fig.show()

fig.write_html("C:/FS/quantamental_platform/Publications/Factor_Performance_Monitoring/filea.html")


#Dynamic plotly
import plotly.graph_objects as go

fig=go.Scatter(x=data.groupby('ETF').head(1)["Return90"], y=data.groupby('ETF').head(1)["Return15"])

fig = go.Figure(
    data=[go.Scatter(x=data.groupby('ETF').head(1)["Return90"], y=data.groupby('ETF').head(1)["Return15"],
                     line_shape='spline',mode='markers+lines',line=dict(width=2, color="#04103b")
                     )],
    layout=go.Layout(
        xaxis=dict(range=[-0.2, 0.2], autorange=False),
        yaxis=dict(range=[-0.2, 0.2], autorange=False),
        template='plotly_white',
        title="Equity Factors Momentum",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
    ),
    frames=[go.Frame(data=[go.Scatter(x=data.groupby('ETF').head(2)["Return90"], y=data.groupby('ETF').head(2)["Return15"])]),
            go.Frame(data=[go.Scatter(x=data.groupby('ETF').head(3)["Return90"], y=data.groupby('ETF').head(3)["Return15"])]),
            go.Frame(data=[go.Scatter(x=data.groupby('ETF').head(4)["Return90"], y=data.groupby('ETF').head(4)["Return15"])],
                     layout=go.Layout(title_text="Equity Factors Momentum"))]
)
fig.update_yaxes( # the y-axis is in dollars
    tickcolor='red'
)
    
fig.layout.xaxis.tickformat = ',.1%'     
fig.layout.yaxis.tickformat = ',.1%'     
fig.show()
fig.write_html("C:/FS/quantamental_platform/Publications/Factor_Performance_Monitoring/fileb.html")



import plotly.express as px
df = px.data.gapminder()
df['pop']=1000
df=data
df['pop']=1
fig = px.scatter(df, x="Return90", y="Return15", animation_frame="Date", animation_group="ETF",
           size="pop", color="ETF", hover_name="ETF",
           log_x=False, size_max=1, range_x=[-0.2,0.2], range_y=[-0.2,0.2],
           # mode = 'markers+lines'
           height = 600, width = 1000
          )

# lineas and markers on first display
fig.for_each_trace(lambda t: t.update(mode = 'lines+markers'))

# lineas and markers on animation frames
for fr in fig.frames:
    for d in fr.data:
        d.update(mode='markers+lines')
        
fig.show()
fig.write_html("C:/FS/quantamental_platform/Publications/Factor_Performance_Monitoring/filec.html")
