#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from streamlit_autorefresh import st_autorefresh
from collect_data import *
import plotly.express as px
from pre import pre_process_inflow_data
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd



def update_data():
    # Perform some request to get a dataframe
    get_river_flow_data()
    get_sindh_barage_data()
    print('refreshed data')

def save_data(df1,df2):
     df1.to_excel('flow_Data.xlsx')
     df2.to_excel('barage_data.xlsx')
     print('made backup data')


# st_autorefresh(interval= 86400 * 1000, key="dataframerefresh")
#
# st.dataframe(update_data())
#
# st_autorefresh(interval= 15*86400 * 1000, key="savedfrefresh")
#
# st.savedf(save_data())
st.set_page_config(layout="wide")
st.header('Indus Dashboard')
st.sidebar.title('Select Ploting Options')


# select data
rivers = ['Indus','Jhelum', 'Chenab', 'Kabul']
river_ops = st.sidebar.radio("River Inflow plot", rivers)

lev_rivers = ['Indus','Jhelum']
reservoir_level = st.sidebar.radio("Reservoir level plot", lev_rivers)

barages = ['Guddu','Sukkur','Kotri']
selected_barage = st.sidebar.radio("Barage", barages)

#retrieve inflow data
flow_river = river_ops + '_Inflow'
df = pre_process_inflow_data()
level_river = reservoir_level + '_levels'
file = 'Sindh_barage.xlsx'
dfb = pd.read_excel(file)
barage_df = dfb.loc[dfb['Station'] == selected_barage]

#ploting data

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"colspan": 2}, None],[{}, {}]],
    subplot_titles=('Time series of Inflows of '+ river_ops,
                    "Reservior Levels Time Series",
                    "Barage Flow Time Series"))
# fig.update_xaxes(title_text="xaxis 1 title", row=1, col=1)
# fig.update_xaxes(title_text="xaxis 2 title", range=[10, 50], row=2, col=1)
# fig.update_xaxes(title_text="xaxis 3 title", showgrid=False, row=2, col=2)
fig.update_yaxes(title_text="1000 X cusecs", row=1, col=1)
fig.update_yaxes(title_text="ft", range=[10, 50], row=2, col=1)
fig.update_yaxes(title_text="1000 cusecs", showgrid=False, row=2, col=2)

fig.add_trace(go.Scatter(name ='Inflows',x=df['Time'], y=df[flow_river]),row=1, col=1)
fig.add_trace(go.Scatter(name ='Reservior levels',x=df['Time'], y=df[level_river]),row=2, col=1)
fig.add_trace(go.Scatter(name = 'Today',x=barage_df['Time'], y=barage_df['Today']), row=2, col=2)
fig.add_trace(go.Scatter(name = 'Last Year',x=barage_df['Time'], y=barage_df['Last Year']),row=2, col=2)
fig.update_layout(height=800, width=1000, showlegend=True,
                  title_text="Pakistan Flow Analytics",
                  #legend = dict(yanchor="top",y=0.99, xanchor="right", x=0.01)
                  )
st.write(fig)

# download = st.button('Download Shape File')
# shape_file_dict = {'chenab':'newchenab.shp',
#                    'Kabul':'krbshape.shp',
#                    'Indus':'Indus_complete.shp',
#                    'tarbela':'newtarbela.shp',
#                    'mangla': 'newmangla.shp'}
# if download:
#   print('Download Started!')

