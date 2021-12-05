import pandas as pd
import os
import streamlit as st
import plotly.graph_objects as go


def get_dataframe(broker_list):
    files = os.listdir(os.path.join('data'))
    path = os.path.join('data', files[-1])
    print(path)
    df = pd.read_csv(path)
    df.drop_duplicates()
    df['Quantity'] = df['Quantity'].astype(float)
    df['BuyerBroker'] = df['BuyerBroker'].astype(str)
    if 'All' in broker_list:
        return df
    else:
        filtered = df[df['BuyerBroker'].isin(broker_list)]
        return filtered


def most_traded(df):
    # temp = df.groupby(['StockSymbol']).sum().sort_values(
    #     by=['Quantity'], ascending=False)
    temp = df.groupby(['StockSymbol'])[['Quantity']].sum(
    ).sort_values(by='Quantity', ascending=False)
    temp['StockSymbol'] = temp.index
    return temp


def get_dropdown_options():
    files = os.listdir(os.path.join('data'))
    path = os.path.join('data', files[-1])
    df = pd.read_csv(path)
    df['BuyerBroker'] = df['BuyerBroker'].astype(str)
    return sorted(list(set(df['BuyerBroker'].to_list())))


st.title('NEPSE Floorsheet Analysis Dashboard')


# def plot_top_broker_by_volume(data, upto=10):
#     sns.set(style='darkgrid')
#     sns.set(rc={'figure.figsize': (20, 10)})
#     data['BuyerBroker'] = data['BuyerBroker'].apply(lambda x: str(x))
#     agg_df = data.groupby(['BuyerBroker'])[['Quantity']].sum(
#     ).sort_values(by='Quantity', ascending=False)
#     agg_df['BuyerBroker'] = agg_df.index
#     sns.barplot(x='BuyerBroker', y='Quantity', data=agg_df.iloc[:10])
#     plt.show()
#     return True


def update_graph_4(dropdown_value):
    # print("dropdown_value", dropdown_value)
    print("dropdown_value", dropdown_value)
    df = get_dataframe(dropdown_value)
    print(len(df))
    filtered = most_traded(df)

    # filtered = df.sort_values(by=['Quantity'], ascending=False)
    scripts = filtered['StockSymbol'].to_list()[:15]
    quantity = filtered['Quantity'].to_list()[:15]
    fig = {
        'data': [{
            'x': scripts,
            'y': quantity,
            'type': 'bar'
        }]
    }
    return fig


options = get_dropdown_options()
selected_brokers = st.sidebar.multiselect(
    'Choose the broker',
    ['All']+options, 'All')

st.header("Script traded by quantity")
fig = update_graph_4(selected_brokers)
st.plotly_chart(fig)
