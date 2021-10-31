# UNUSED
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

    # Reading in datasets for Cramer's and Chi Square P value
    cramer_mat = pd.read_csv('./data/cramer_matrix.csv')
    p_mat = pd.read_csv('./data/chi_sq_p_val.csv')

    # st.markdown('## Hello')
    # ldf = pd.read_csv('../data/LaundryData.csv')

    st.markdown('# Attribute Association & Relationships')
    st.markdown('## Which attributes are associated or related?')



    # Compute x^2 + y^2 across a 2D grid
    # x, y = np.meshgrid(range(-5, 5), range(-5, 5))
    # x, y = np.meshgrid(range(-10, 10), range(-10, 10))
    # z = x ** 2 + y ** 2

    # # Convert this grid to columnar data expected by Altair
    # source = pd.DataFrame({'x': x.ravel(),
    #                     'y': y.ravel(),
    #                     'z': z.ravel()})

    # heatmap = alt.Chart(cramer_mat).mark_rect().encode(
    #     x='x:O',
    #     y='y:O',
    #     color='z:Q'
    # )

    # heatmap + heatmap.mark_text().transform_calculate(label = '"" + datum.x + datum.y').encode(
    #     text='label:N',
    #     color=alt.value('black'))

    # source = data.cars()
    source = cramer_mat.copy()

    # Configure common options
    base = alt.Chart(source).transform_aggregate(
        num_cars='count()',
        groupby=['Origin', 'Cylinders']
    ).encode(
        alt.X('Cylinders:O', scale=alt.Scale(paddingInner=0)),
        alt.Y('Origin:O', scale=alt.Scale(paddingInner=0)),
    )

    # Configure heatmap
    heatmap = base.mark_rect().encode(
        color=alt.Color('num_cars:Q',
            scale=alt.Scale(scheme='viridis'),
            legend=alt.Legend(direction='horizontal')
        )
    )

    # Configure text
    text = base.mark_text(baseline='middle').encode(
        text='num_cars:Q',
        color=alt.condition(
            alt.datum.num_cars > 100,
            alt.value('black'),
            alt.value('white')
        )
    )

    # Draw the chart
    heatmap + text


    st.altair_chart(heatmap)