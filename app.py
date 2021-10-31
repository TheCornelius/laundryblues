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
from streamlit.elements.legacy_data_frame import add_rows
from multiapp import MultiApp
from apps import rdof, association, dryer_prob, washerclass

st.set_page_config(page_title='Laundry Blues', layout = 'wide', initial_sidebar_state = 'auto')

app = MultiApp()
apptitle = 'Laundry Customer Profiling'
app.add_app('Dryer Probability for Each Washer', dryer_prob.app)
app.add_app('Day of Week Preference by Race', rdof.app)
app.add_app('Attribute Association & Relationships', association.app)
app.add_app('Classifying Dryer Number', washerclass.app)
app.run()