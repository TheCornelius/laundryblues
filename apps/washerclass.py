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
import pickle

apptitle = 'Laundry Customer Profiling'

def app():
    st.markdown('# Predicting Dryer Number using RFC')

    # Importing the model and label encoder
    label_encoders = pickle.load(open('./models/le.pkl', 'rb'))
    load_rfc = pickle.load(open('./models/rfc.pkl', 'rb'))
    keys = label_encoders.keys()
    keys = list(keys)

    # Declaring input fields
    age_group = st.selectbox('Age Group', ('(25, 30]', '(30, 35]', '(50, 55]', '(45, 50]', '(40, 45]', '(35, 40]'))
    basket_colour = st.selectbox('Basket Colour', ('red', 'green', 'blue', 'black', 'white', 'pink', 'purple', 'yellow', 'brown', 'orange', 'grey', 'unknown'))
    day_of_week = st.selectbox('Day of Week', (0, 1, 2, 3, 4, 5, 6))
    kids_category = st.selectbox('Kids Category', ('young', 'no_kids', 'toddler', 'unknown', 'baby'))
    pants_colour = st.selectbox('Pants Colour', ('black', 'blue_jeans', 'yellow', 'white', 'brown', 'grey', 'orange', 'blue', 'green', 'red', 'purple', 'unknown', 'pink'))
    part_of_day = st.selectbox('Part of Day', ('Evening', 'Night', 'Late Night', 'Early Morning', 'Morning', 'Afternoon'))
    race = st.selectbox('Race', ('malay', 'indian', 'unknown', 'chinese', 'foreigner'))
    shirt_colour  = st.selectbox('Shirt Colour', ('blue', 'white', 'red', 'black', 'brown', 'yellow', 'grey', 'orange', 'green', 'purple', 'pink', 'unknown'))
    washer_no = st.selectbox('Washer Number', (3, 6, 4, 5))
    wash_item = st.selectbox('Wash Item', ('clothes', 'unknown', 'blankets'))


    age_group_stuff = {'(25, 30]': 0, '(30, 35]': 1, '(50, 55]': 2, '(45, 50]': 3, '(40, 45]': 4, '(35, 40]': 5}
    age_group_res = age_group_stuff.get(age_group)
    basket_colour_res = label_encoders['BASKET_COLOUR'].transform([basket_colour])[0]
    day_of_week_res = label_encoders['DAY_OF_WEEK'].transform([day_of_week])[0]
    kids_category_res = label_encoders['KIDS_CATEGORY'].transform([kids_category])[0]
    pants_colour_res = label_encoders['PANTS_COLOUR'].transform([pants_colour])[0]
    part_of_day_res = label_encoders['PART_OF_DAY'].transform([part_of_day])[0]
    race_res = label_encoders['RACE'].transform([race])[0]
    shirt_colour_res = label_encoders['SHIRT_COLOUR'].transform([shirt_colour])[0]
    washer_no_res = label_encoders['WASHER_NO'].transform([washer_no])[0]
    wash_item_res = label_encoders['WASH_ITEM'].transform([wash_item])[0]

    predictinputs = [age_group_res, basket_colour_res, day_of_week_res, kids_category_res, pants_colour_res, part_of_day_res, race_res, shirt_colour_res, washer_no_res, wash_item_res]
    prediction = load_rfc.predict([predictinputs])[0]
    prediction_proba = load_rfc.predict_proba([predictinputs])[0]
    prediction = label_encoders['DRYER_NO'].inverse_transform([prediction])[0]

    st.info(f"The predicted dryer is dryer number {prediction}")
    st.success(f"""
        The prediction probability for dryer number 7 is : {prediction_proba[0]}\n
        The prediction probability for dryer number 8 is : {prediction_proba[1]}\n
        The prediction probability for dryer number 9 is : {prediction_proba[2]}\n
        The prediction probability for dryer number 10 is : {prediction_proba[3]}\n
    """)