#%%
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
os.chdir('C:/data/scripts/Forecast_Search_Wizard/')
dts = []
product = []
with open('fsw_output.txt','r') as src:
    for line in src.readlines():
        if line[0] in ('0','1'):
            values = line.split('\t')
            dts.append(values[0])
            product.append(values[1][1:])

#print(dts,product)
dts_pd = pd.to_datetime(dts,format='%m-%d-%Y %H:%M', infer_datetime_format=False)
data = {'dts':dts_pd, 'product':product}
df_temp = pd.DataFrame(data)
df_temp.set_index('dts', inplace=True)
df_full = df_temp[(df_temp.index > "2007-12-15") & (df_temp.index < "2018-12-15")]
df_full['count'] = 1

print(df_full)

def make_trace(prod):
    df = df_full[df_full['product'] == prod]
    #monthly = df.resample('M').count()
    df[prod] = df['count'].cumsum()
    x=df.index
    y=df[prod]
    trace = go.Scatter(x=x,y=y,name=prod)
    return trace

test = df_full.groupby(by=['product']).cumsum()
print(test)
trace1 = make_trace('AFDMQT')
trace2 = make_trace('AFDAPX')
trace3 = make_trace('AFDGRR')
trace4 = make_trace('AFDIWX')
#for w in('AFDMQT','AFDAPX','AFDGRR','AFDIWX'):
#    df = df_full[df_full['product'] == w]
#    monthly = df.resample('M').count()
#    #print(monthly)
#    info = df.rolling(window=30, min_periods=0).count()
#    #print(info)
#    x=df.index
#    y=monthly['product']
#    #print(df)
#    #print(info)

#print(trace1)
test.plot()
title = 'Cumulative number of "Lake Breeze" mentions in AFDs'

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(trace1)
fig.add_trace(trace2,secondary_y=False)
fig.add_trace(trace3,secondary_y=False)
fig.add_trace(trace4,secondary_y=False)
fig['layout'].update(height = 600, width = 1000, title = title,xaxis=dict(
      tickangle=-90
    ))
#iplot(fig)
fig.show()


# %%
