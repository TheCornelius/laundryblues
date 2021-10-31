'''Attribute Association & Relationships'''
import streamlit as st
import altair as alt
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
from datetime import date
from PIL import Image
from altair import datum

apptitle = 'Laundry Customer Profiling'

def app():
    st.markdown('# Dryer Probability for Each Washer')
    st.markdown('## For each washer, which dryer is most likely to be used?')
    st.markdown('Select a washer to explore the dryer that is most likely to be used together. Hover on the bars to get more information.')
    st.markdown('Use mouse scroll to zoom in/out of the chart.')

    # Importing data matrixes
    washer_prob = pd.read_csv('./data/washer_dryer_prob.csv', index_col = 0)
    df = pd.read_csv('./data/LaundryData.csv')
    df.columns = df.columns.str.upper()  # Convert column names to upper case
    df['DATE'] =  pd.to_datetime(df['DATE'],format='%d/%m/%Y', errors='coerce')
    df['DATE'] = df['DATE'].dt.date

    cols = washer_prob.columns
    washer_ls = washer_prob['WASHER_NO'].unique()
    washer_ls = sorted(list(washer_ls))

    # DEFINE UI
    w_opts = st.selectbox(
        'Washer Number: ',
        washer_ls
    )

    d_c1, d_c2 = st.columns([1, 1])

    min_date = date(2015, 10, 19)
    max_date = date(2015, 12, 9)

    s_date = date(2015, 10, 19)
    e_date = date(2015, 12, 9)


    with d_c1:
        r_sd = st.date_input('Start date', value=min_date)

    with d_c2:
        r_ed = st.date_input('End date', value=max_date)

    st.info(f'INFO: The date range allowed is from `%s` to `%s`' % (min_date, max_date))

    if r_sd < r_ed and r_sd >= min_date and r_ed <= max_date:
        s_date = r_sd
        e_date = r_ed
        st.success('Successfully chosen dates with\n\nStart date: `%s`\n\nEnd date: `%s`' % (s_date, e_date))
    else:
        st.error('Error: End date must fall after start date, and both dates must be in the range of 2015-10-19 to 2015-12-09')


    # Processing dataframe
    pdf = df.copy()
    pdf = pdf[(pdf['DATE'] >= s_date) & (pdf['DATE'] <= e_date)]

    col1 = 'WASHER_NO'
    col2 = 'DRYER_NO'

    wd_pair_counts = pdf.groupby([col1, col2]).size().reset_index(name="COUNTS").copy()  # to count the number of washer/dryer usage pair counts
    wd_pair_probs = wd_pair_counts.groupby(col1).size()
    wd_pair_probs = pd.DataFrame(columns=[col1, col2, 'PROBABILITY'])
    wd_pair_probs = wd_pair_counts.copy()
    wd_pair_probs['SUM'] = 0
    wd_pair_probs['PROBABILITY'] = 0

    wash_q = df['WASHER_NO'].unique()
    wash_q = sorted(list(wash_q))

    for w in wash_q:
        cur_w = wd_pair_probs[wd_pair_probs[col1] == w]  # ['COUNTS']
        w_sum = sum(cur_w['COUNTS'])
        for i, v in wd_pair_probs.iterrows():
            if v[col1] == w:
                wd_pair_probs.loc[i, 'SUM'] = w_sum
    wd_pair_probs['PROBABILITY'] = wd_pair_probs['COUNTS'] / wd_pair_probs['SUM']

    # Displaying resultant data
    wash_prob_display = wd_pair_probs.copy()
    wash_prob_display = wash_prob_display[wash_prob_display['WASHER_NO'] == w_opts]

    prob_bar_chart = alt.Chart(wash_prob_display, width=700, height=430, title=f'Probability of Each Dryer to be Used With Washer #{w_opts} from {s_date} to {e_date}').mark_bar().encode(
        x=alt.X('DRYER_NO:O', title='Dryer Number', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('PROBABILITY:Q', title='Probability', scale=alt.Scale(domain=[0, 0.5])),
        tooltip=[alt.Tooltip('PROBABILITY', title='Probability '), alt.Tooltip('WASHER_NO', title='Washer Number '), alt.Tooltip('DRYER_NO', title='Dryer Number ')]
    ).configure_axis(
        labelFontSize=13,
    ).interactive()

    st.altair_chart(prob_bar_chart)