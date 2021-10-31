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
    st.markdown('# Attribute Association & Relationships')
    st.markdown('## Which attributes are strongly associated?')

    # Importing data matrixes
    cramer_mat = pd.read_csv('./data/cramer_matrix.csv', index_col=0)
    p_mat = pd.read_csv('./data/chi_sq_p_val.csv', index_col=0)

    # Getting the values and putting into the same dataframe
    data_matrix = cramer_mat.reset_index().melt('index')
    data_matrix.columns = ['Attribute_1', 'Attribute_2', "Cramers_V"]
    p_matrix = p_mat.reset_index().melt('index')
    p_matrix.columns = ['Attribute_1', 'Attribute_2', 'p_value']
    data_matrix['p_value'] = p_matrix['p_value']  # Final result dataframe

    variables = data_matrix['Attribute_1'].unique()
    variables = sorted(variables)
    cols = data_matrix.columns  # Storing columns in dataframe

    # Setting widths and heights of boxes, and configuration variables
    width_step = 35
    height_step = width_step
    p_exclude_dups = False  # Whether to exclude duplicates

    # Drawing the heatmap
    st.markdown('### Chi Square test p-value heatmap')
    st.markdown('''
    Chi Square test of independence is a statistical test that verifies whether two attributes are independent or associated.\n
    A p-value of < 0.05 indicates both attributes are associated, and a Cramer's V value of > 0.15 indicates both attributes are strongly associated.
    ''')

    # Draw the first heatmap - p-value
    p_chart = alt.Chart(data_matrix, title="Chi Square Test p-value Heatmap").mark_rect().encode(
        x=alt.X('Attribute_1', title='Attribute 1'),
        y=alt.Y('Attribute_2', title='Attribute 2'),
        color=alt.Color('p_value', legend=None),
        tooltip=[alt.Tooltip('p_value', title='p-value '), alt.Tooltip('Cramers_V', title='Cramer\'s V ')]
    ).properties(
        width=alt.Step(width_step),
        height=alt.Step(height_step)
    )

    p_chart += p_chart.mark_text(size=10).encode(
        text=alt.Text('p_value', format=".3f"),
        color=alt.condition(
            "datum.p_value > 0.5",
            alt.value('white'),
            alt.value('black')
        )
    )

    strong_chart = alt.Chart(data_matrix, title="Chi Square Test p-value Heatmap").mark_rect().encode(
        x=alt.X('Attribute_1', title='Attribute 1'),
        y=alt.Y('Attribute_2', title='Attribute 2'),
        color=alt.Color('p_value', legend=None),
        tooltip=[alt.Tooltip('p_value', title='p-value '), alt.Tooltip('Cramers_V', title='Cramer\'s V ')]
    ).properties(
        width=alt.Step(width_step),
        height=alt.Step(height_step)
    )

    strong_chart += strong_chart.mark_text(size=10).encode(
        text=alt.Text('p_value', format=".3f"),
        color=alt.condition(
            "datum.p_value > 0.5",
            alt.value('white'),
            alt.value('black')
        )
    )

    # Layout the attributes for the first p_chart
    p_c1, p_c2 = st.columns([1, 1])
    with p_c1:
        p_exclude_dups = st.checkbox("Hide duplicates")
        
    with p_c2:
        p_exclude_weak = st.checkbox("Show attribute pairs with strong association")

    if not p_exclude_dups:
        # If show full
        
        if p_exclude_weak:
            # If dont show weak
            p_exc_chart = p_chart.transform_filter("datum.p_value < 0.05 & datum.Cramers_V > 0.15")
            st.altair_chart(p_exc_chart)
        else:
            # Show full, and weak altogether
            st.altair_chart(p_chart)
    else:
        # If exclude duplicates
        p_exc_chart = p_chart.transform_filter("datum.Attribute_1 < datum.Attribute_2")

        if p_exclude_weak:
            # If exclude duplicates and show strong only
            exc_strong_chart = p_exc_chart.transform_filter("datum.p_value < 0.05 & datum.Cramers_V > 0.15")
            st.altair_chart(exc_strong_chart)

        else:
            # exclude duplicates full
            st.altair_chart(p_exc_chart)


    st.markdown("### Cramer's V heatmap")
    st.markdown('''
    Cramer's V is based on a nominal variation of Pearson's Chi Square test. 
    The Cramer's V test serves as a post-test for Chi-Square test, and detects the association strength between categorical attributes.
    \n\n

    Cramer's V:
    - output range is [0, 1]: 0 indicates no association, 1 indicates perfect association
    - no negative values or indicating of negative association
    - symmetrical: unlike correlation, insensitive to swapping X and Y values

    A p-value of < 0.05 indicates both attributes are associated, and a Cramer's V value of > 0.15 indicates both attributes are strongly associated.
    ''')

    # Draw the first heatmap - Cramer's V
    c_chart = alt.Chart(data_matrix, title="Cramers' V Heatmap").mark_rect().encode(
        x=alt.X('Attribute_1', title='Attribute 1'),
        y=alt.Y('Attribute_2', title='Attribute 2'),
        color=alt.Color('Cramers_V', legend=None),
        tooltip=[alt.Tooltip('p_value', title='p-value '), alt.Tooltip('Cramers_V', title='Cramer\'s V ')]
    ).properties(
        width=alt.Step(width_step),
        height=alt.Step(height_step)
    )

    c_chart += c_chart.mark_text(size=10).encode(
        text=alt.Text('Cramers_V', format=".3f"),
        color=alt.condition(
            "datum.Cramers_V > 0.5",
            alt.value('white'),
            alt.value('black')
        )
    )

    c_strong_chart = alt.Chart(data_matrix, title="Cramers' V Heatmap").mark_rect().encode(
        x=alt.X('Attribute_1', title='Attribute 1'),
        y=alt.Y('Attribute_2', title='Attribute 2'),
        color=alt.Color('p_value', legend=None),
        tooltip=[alt.Tooltip('Cramers_V', title='Cramer\'s V '), alt.Tooltip('p_value', title='p-value ')]
    ).properties(
        width=alt.Step(width_step),
        height=alt.Step(height_step)
    )

    c_strong_chart += c_strong_chart.mark_text(size=10).encode(
        text=alt.Text('p_value', format=".3f"),
        color=alt.condition(
            "datum.Cramers_V > 0.5",
            alt.value('white'),
            alt.value('black')
        )
    )

    # Layout the attributes for the second p_chart
    c_c1, c_c2 = st.columns([1, 1])
    with c_c1:
        p_exclude_dups_c = st.checkbox("Hide duplicates\t")
        
    with c_c2:
        p_exclude_weak_c = st.checkbox("Show attribute pairs with strong association\t")

    if not p_exclude_dups_c:
        # If show full
        
        if p_exclude_weak_c:
            # If dont show weak
            c_exc_chart = c_chart.transform_filter("datum.p_value < 0.05 & datum.Cramers_V > 0.15")
            st.altair_chart(c_exc_chart)
        else:
            # Show full, and weak altogether
            st.altair_chart(c_chart)
    else:
        # If exclude duplicates
        c_exc_chart = c_chart.transform_filter("datum.Attribute_1 < datum.Attribute_2")


        if p_exclude_weak_c:
            # If exclude duplicates and show strong only
            c_exc_strong_chart = c_exc_chart.transform_filter("datum.p_value < 0.05 & datum.Cramers_V > 0.15")
            st.altair_chart(c_exc_strong_chart)
        else:
            # exclude duplicates full
            st.altair_chart(c_exc_chart)