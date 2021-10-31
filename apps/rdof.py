'''Laundry Shop Visitation Day of Week Preference by Race'''
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
    st.markdown('# Laundry Shop Visitation Day of Week Preference by Race')
    st.markdown('## Which day of the week does each race prefer to visit the laundromat?')
    dof = pd.read_csv('./data/dof_race.csv', parse_dates=True)
    dof.describe()
    dof['DATETIME'] = pd.to_datetime(dof['DATETIME'])
    dof['DATE'] = dof['DATETIME'].dt.date

    races = list(dof['RACE'].unique())
    races = [r.title() for r in races if r != 'unknown']

    r = races[0]
    day_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}  # Dictionary to convert between day of week in numeric form to String format

    r_opts = st.selectbox(
        'Race: ',
        races
    )

    r_c1, r_c2 = st.columns([1, 1])

    min_date = date(2015, 10, 19)
    max_date = date(2015, 12, 9)

    s_date = date(2015, 10, 19)
    e_date = date(2015, 12, 9)


    with r_c1:
        r_sd = st.date_input('Start date', value=date(2015, 10, 19))

    with r_c2:
        r_ed = st.date_input('End date', value=date(2015, 12, 9))

    st.info(f'INFO: The date range allowed is from `%s` to `%s`' % (min_date, max_date))

    if r_sd < r_ed and r_sd >= date(2015, 10, 19) and r_ed <= date(2015, 12, 9):
        s_date = r_sd
        e_date = r_ed
        st.success('Successfully chosen dates with\n\nStart date: `%s`\n\nEnd date: `%s`' % (s_date, e_date))
    else:
        st.error('Error: End date must fall after start date, and both dates must be in the range of 2015-10-19 to 2015-12-09')

    pdf = dof[dof['RACE'] == r_opts.lower()].copy()
    pdf = pdf[(pdf['DATE'] >= s_date) & (pdf['DATE'] <= e_date)]
    rdof = pdf['DAY_OF_WEEK'].replace(day_of_week).value_counts().reset_index()
    rdof = rdof.rename(columns = {'DAY_OF_WEEK': 'NUMBER_OF_CUSTOMERS', 'index': 'DAY_OF_WEEK'})

    r_dow = alt.Chart(rdof, width=700, height=430, title=f'Number of {r_opts.title()} Race Customers by Day of Week from {s_date} to {e_date}').mark_bar().encode(
        x=alt.X('NUMBER_OF_CUSTOMERS', title='Number of Customers'),
        y=alt.Y('DAY_OF_WEEK', title='Day of Week', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
        tooltip=[alt.Tooltip('NUMBER_OF_CUSTOMERS', title='Number of customers')]
    )
    st.altair_chart(r_dow)