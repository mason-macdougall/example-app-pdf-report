import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
from utils import *

st.set_page_config(layout="centered", page_icon="💼", page_title="Diploma Generator")
st.title("JobComp: Compare the true value of your job offers")

st.write(
    "Have a new job with higher pay but it\'s further away? Now you\'re wondering if it would even be worth it?"
)

st.write(
    "Fear not! We\'ll do the math for you and give you a clear breakdown of the results"
)

left, right = st.columns(2)

left.write("Fill in your data for Job #1:")
form = left.form("form1")
pay1 = form.text_input("Hourly pay rate ($/hour)")
dist1 = form.text_input("One-way distance to job (miles)")
travel_time1 = form.text_input("If distance is unknown, enter the one-way travel time (minutes)")
hours1 = form.text_input("Amount of time worked per week (hours)")
days1 = form.text_input("Number of times you go into work per week")
submit1 = form.form_submit_button("Submit Job #1")

right.write("Fill in your data for Job #2:")
form = right.form("form2")
pay2 = form.text_input("Hourly pay rate ($/hour)")
dist2 = form.text_input("One-way distance to job (miles)")
travel_time2 = form.text_input("If distance is unknown, enter the one-way travel time (minutes)")
hours2 = form.text_input("Amount of time worked per week (hours)")
days2 = form.text_input("Number of times you go into work per week")
submit2 = form.form_submit_button("Submit Job #2")

left.write("Fill in your car data:")
form = left.form("form3")
gas = form.text_input("Cost of gas ($/gal)")
mpg = form.text_input("How many miles per gallon does your car get (on average)?")
mph = form.text_input("Average travel speed (miles/hour)")
submit3 = form.form_submit_button("Compare jobs!")

right.write("If you want, we can account for income taxes too:")
form = right.form("form4")
tax_rate = form.text_input("Estimate your income tax rate (as a percentage)")
submit4 = form.form_submit_button("Include tax rate")

inputs = [gas, mpg, mph, pay1, dist1, travel_time1, hours1, days1, pay2, dist2, travel_time2, hours2, days2]

inputs_fin = []
for i in inputs:
    if len(i) == 0:
        inputs_fin.append(np.nan)
    else:
        inputs.append(float(i))
        
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


#course = form.selectbox(
#    "Choose course",
#    ["Report Generation in Streamlit", "Advanced Cryptography"],
#    index=0,
#)
#grade = form.slider("Grade", 1, 100, 60)


if (submit1 and sumbit2 and submit3) and submit4 == False:
    report = get_full_report(job1, job2, car, tax_rate=None)
    for r in report:
        st.write(r)
elif submit1 and sumbit2 and submit3 and submit4:
    if len(tax_rate) == 0:
        tax_rate = None
    else:
        tax_rate = float(tax_rate)/100
    report = get_full_report(job1, job2, car, tax_rate)
    for r in report:
        st.write(r)
