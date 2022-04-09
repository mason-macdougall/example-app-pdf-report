import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe

st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
st.title("JobComp: Compare the true value of your job offers")

st.write(
    "Have a new job with higher pay but it\'s further away? Now you\'re wondering if it would even be worth it?"
)

st.write(
    "Fear not! We\'ll do the math for you and give you a clear breakdown of the results"
)

left, right = st.columns(2)

right.write("Here's the template we'll be using:")

right.image("template.png", width=300)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")


left.write("Fill in the data:")
form = left.form("template_form")
student = form.text_input("Student name")


st.write(
    student
)

aa = "test string"
st.write(
    aa
)

course = form.selectbox(
    "Choose course",
    ["Report Generation in Streamlit", "Advanced Cryptography"],
    index=0,
)
grade = form.slider("Grade", 1, 100, 60)
submit = form.form_submit_button("Generate Test")

def test_print(i):
    return "This is a test"+i
    
bb = test_print('a')

bb

cc = test_print('b')

st.write(cc)

print("Also a test")

"Here\'s another test"
'And Another'

if submit:
    '''
    html = template.render(
        student=student,
        course=course,
        grade=f"{grade}/100",
        date=date.today().strftime("%B %d, %Y"),
    )

    pdf = pdfkit.from_string(html, False)
    st.balloons()

    right.success("🎉 Your diploma was generated!")
    # st.write(html, unsafe_allow_html=True)
    # st.write("")
    right.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="diploma.pdf",
        mime="application/octet-stream",
    )
    '''
    
    test_print()
    st.write("hello")
