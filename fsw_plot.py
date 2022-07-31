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
df = pd.DataFrame(data)
df.set_index('dts', inplace=True)
print(df)

df.plt()