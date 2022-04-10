import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
import numpy as np
from utils import *

st.set_page_config(layout="centered", page_icon="💼", page_title="JobComp")
st.title("JobComp: Compare the true value of your job options")

st.write(
    "Have a new job with higher pay but it\'s further away? Now you\'re wondering if it would even be worth it?"
)

st.write(
    "Fear not! We\'ll do the math for you and give you a clear breakdown of the results"
)

left, right = st.columns(2)

left.write("Fill in the data for Job #1, Job #2, and your car:")
form = left.form("form1")
pay1 = form.text_input("Job #1: Hourly pay rate ($/hour)")
hours1 = form.text_input("Job #1: Amount of time worked per week (hours)")
days1 = form.text_input("Job #1: Number of times you go into work per week")
dist1 = form.text_input("Job #1: One-way distance to job (miles)")
travel_time1 = form.text_input("Job #1: If distance is unknown, enter the one-way travel time (minutes)")
#submit1 = form.form_submit_button("Submit Job #1")

#right.write("Fill in your data for Job #2:")
#form = right.form("form2")
pay2 = form.text_input("Job #2: Hourly pay rate ($/hour)")
hours2 = form.text_input("Job #2: Amount of time worked per week (hours)")
days2 = form.text_input("Job #2: Number of times you go into work per week")
dist2 = form.text_input("Job #2: One-way distance to job (miles)")
travel_time2 = form.text_input("Job #2: If distance is unknown, enter the one-way travel time (minutes)")
#submit2 = form.form_submit_button("Submit Job #2")

#left.write("Fill in your car data:")
#form = left.form("form3")
mpg = form.text_input("Car: How many miles per gallon does your car get (on average)?")
mph = form.text_input("Car: Average travel speed (miles/hour)")
gas = form.text_input("Car: Cost of gas ($/gal)")
#submit = form.form_submit_button("Compare jobs!")

#right.write("If you want, we can account for income taxes too:")
#form = right.form("form4")
tax_rate = form.text_input("If you want, we can account for income taxes too. Just input your income tax rate (as a percentage)")
#submit4 = form.form_submit_button("Include tax rate")

submit = form.form_submit_button("Compare jobs!")


#course = form.selectbox(
#    "Choose course",
#    ["Report Generation in Streamlit", "Advanced Cryptography"],
#    index=0,
#)
#grade = form.slider("Grade", 1, 100, 60)


#if submit: #(submit1 and sumbit2 and submit3) and submit4 == False:
#    report = get_full_report(job1, job2, car, tax_rate=None)
#    for r in report:
#        st.write(r)
if submit: #1 and sumbit2 and submit3 and submit4:
    inputs = [gas, mpg, mph, pay1, dist1, travel_time1, hours1, days1, pay2, dist2, travel_time2, hours2, days2]

    inputs_fin = []
    for i in inputs:
        if len(str(i)) == 0:
            inputs_fin.append(np.nan)
        else:
            inputs_fin.append(float(i))

    gas, mpg, mph, pay1, dist1, travel_time1, hours1, days1, pay2, dist2, travel_time2, hours2, days2 = inputs_fin

    car = {'gas': gas, # $/gal
           'mpg': mpg,  # miles/gal
           'mph': mph # miles/hr
          }

    job1 = {'pay': pay1, # $/hr
            'dist': dist1, # miles (one way)
            'travel_time': travel_time1, # travel time in mins (one way)
            'hours': hours1, # hrs of work per week
            'days': days1} # number of days you go into work per week

    job2 = {'pay': pay2, 
            'dist': dist2,
            'travel_time': travel_time2,
            'hours': hours2, 
            'days': days2}

    if len(str(tax_rate)) == 0:
        tax_rate = None
    else:
        tax_rate = float(tax_rate)/100
        
    report = get_full_report(job1, job2, car, tax_rate)
    for r in report:
        st.write(r)

    
