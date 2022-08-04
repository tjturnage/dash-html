import os
import pandas as pd
import plotly.graph_objs as go
os.chdir('C:/data/scripts/Forecast_Search_Wizard/')
dts = []
product = []
with open('fsw_output.txt.txt','r') as src:
    for line in src.readlines():
        if line[0] in ('0','1'):
            values = line.split('\t')
            dts.append(values[0])
            product.append(values[1][1:])

#print(dts,product)
dts_pd = pd.to_datetime(dts,infer_datetime_format=True)
data = {'dts':dts_pd, 'product':product}
df_full = pd.DataFrame(data)
df_full.set_index('dts', inplace=True)
df = df_full[df_full['product'] == 'HWOGRR']
monthly = df.resample('M').count()
print(monthly)
#info = df.rolling(window=30).count()
#print(info)
x=df.index
y=monthly['product']
#print(df)
#print(info)
fig = go.Figure(data=go.Scatter(x=x, y=y))
fig.show()