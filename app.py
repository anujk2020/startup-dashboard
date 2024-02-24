import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title='Startup Analysis')

df = pd.read_csv('startup_funding.csv')

df = df.drop(columns=['Remarks'])
df = df.set_index('Sr No')

df = df.rename(columns={'Date dd/mm/yyyy':'date',
                        'Startup Name':'startup',
                        'Industry Vertical':'vertical',
                        'SubVertical':'subvertical',
                        'City  Location':'city',
                        'Investors Name': 'investors',
                        'InvestmentnType':'round',
                        'Amount in USD':'amount'
                        })


df['amount'] = pd.to_numeric(df['amount'].str.replace(",",""), errors='coerce')

df['date'] = pd.to_datetime(df['date'], errors='coerce')

df['amount'] = df['amount'].fillna(0)

df = df.dropna(subset=['date', 'startup', 'vertical', 'city', 'investors', 'round', 'amount'])

def load_investor_details(investor):
    st.title(investor)

    st.subheader('Recent Investments')
    st.dataframe(df[df['investors'].str.contains(investor)].sort_values(by=['date'],ascending=False).head()[['investors','date','startup','vertical','city','round','amount']].reset_index(drop=True))

    st.subheader('Top 5 Investments')
    st.dataframe(df[df['investors'].str.contains(investor)].sort_values(by=['amount'], ascending=False).head()[
        ['investors', 'date', 'startup', 'vertical', 'city', 'round', 'amount']].reset_index(
        drop=True))


    st.subheader('Biggest Investments')

    col1, col2 = st.columns(2)

    # with col1:
    big_series = df[df['investors'].str.contains(investor)].groupby('startup')[
            'amount'].sum().reset_index().sort_values(by=['amount'], ascending=False).head()
    # st.dataframe(big_series)

    with col1:
        fig, ax = plt.subplots()
        ax.bar(big_series['startup'],big_series['amount'])
        st.pyplot(fig)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    fig1, ax1 = plt.subplots()
    ax1.plot(year_series.index, year_series.values)

    st.pyplot(fig1)

def load_overall_analysis():
    st.title('Overall Analysis')
    total_amt_inv = df['amount'].sum()

    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    total_funded_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total Funding', '$'+str(total_amt_inv))
    with col2:
        st.metric('Maximum Funding', '$'+str(max_funding))
    with col3:
        st.metric('Average Funding', '$' + str(avg_funding))
    with col4:
        st.metric('Total Funded Startups', str(total_funded_startups))

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option== 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')

    if btn0:
        load_overall_analysis()


elif option == 'StartUp':
    st.title('StartUp Analysis')
    st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')

else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    # st.title('Investor Analysis')
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        # st.title('Investor Analysis')
        load_investor_details(selected_investor)

