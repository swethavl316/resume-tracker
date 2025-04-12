from dotenv import load_dotenv

load_dotenv()

import io
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro')

    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


def input_pdf_setup(upload_file):
    if upload_file is None:
        raise FileNotFoundError("No file uploaded")

    ##Convert the pdf to image

    image=pdf2image.convert_from_bytes(upload_file.read())

    first_page=image[0]

    #Convert to bytes

    img_byte_arr=io.BytesIO()
    first_page.save(img_byte_arr,format='JPEG')
    img_byte_arr=img_byte_arr.getvalue()

    pdf_parts=[
        {
            "mime_type":"image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }
    ]
    return pdf_parts

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area(" Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your Resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
   st.write("PDF Uploadeed Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Percentage match")


input_prompt1 = """
You are an experienced HR With Tech Experience in the field of any one job role from Data Science, Full stack Web development, Big Data Engineering, DEVOPS, Data Analyst, your task is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with job description.Highlight the strengths and weaknesses of the applicant in relation to the specified job role
"""

input_prompt2="""
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Data Science, Full stack Web development, Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality,
Your task is to evaluate the resume against the provided job description. give me the percentge match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.""" 


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
      if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
      else:
        st.write("Please upload the resume")



