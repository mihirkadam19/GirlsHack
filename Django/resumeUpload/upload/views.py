from django.shortcuts import render
from .forms import ResumeUploadForm
from pdfminer.high_level import extract_text
from docx import Document
from io import BytesIO
import os
import google.generativeai as genai


GOOGLE_API_KEY='AIzaSyDCTST_un8AsT6F1mRqsvBVcEa2ih8U7Sw'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")




def extract_text_from_pdf(file):
    # Use BytesIO to handle the in-memory file
    return extract_text(file)

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_file(file):
    _, ext = os.path.splitext(file.name)
    if ext.lower() == '.pdf':
        return extract_text_from_pdf(BytesIO(file.read()))
    elif ext.lower() == '.docx':
        return extract_text_from_docx(BytesIO(file.read()))
    else:
        raise ValueError("Unsupported file format")
    
def get_skills(prompt, text):
    try:
        prompt = prompt + text
        return model.generate_content(prompt)
    except Exception as e:
        print(f'get_skills:{e}')
        return None

def custom_prompt(prompt, skills, job_title, job_description):
    try:
        return prompt + "\n" + "Resume Skills: " + skills + "\n" + "Job Title: " + job_title + "\n" + "Job Description: " + job_description
    except Exception as e:
        print(f'custom_prompt:{e}')
        return None
    
def gemini(text,job_title, job_description):
    try:
        prompt_1 = "From the given text, extract all the skills as a Python list.Return only the list of skills and nothing else. Ensure there are no duplicates."
        skills = get_skills(prompt_1, text)
        #Modify prompt_2 to return the missing skills as a Python list
        prompt_2 = (
        "Given a resume, job title, and job description, extract and compare the required skills from both documents. "
        "First, identify all the skills mentioned in the job description, including technical, soft, and domain-specific skills. "
        "Then, silently compare the skills with the resume. Do not print the resume skills explicitly. "
        "Identify and return a list of  only the top 5 missing or underdeveloped skills in the resume that are crucial for the job described, "
        "along with a brief explanation of why they are necessary for the role."
        )

        prompt = custom_prompt(prompt_2, skills.text, job_title, job_description)

        return model.generate_content(prompt).text.split("\n")
    except Exception as e:
        print(f'gemini:{e}')
        return None

def home(request):
    if request.method == 'POST':
        try:
            fm = ResumeUploadForm(request.POST, request.FILES)
            if fm.is_valid():
                name = fm.cleaned_data['name']
                email = fm.cleaned_data['email']
                designation_job = fm.cleaned_data['designation_job']
                description_job = fm.cleaned_data['description_job']
                resume_file = fm.cleaned_data['resume_file']

                # Process the uploaded file directly from request.FILES
                extracted_text = extract_text_from_file(resume_file)
                print(f"text: {extracted_text[:50]}")
                #skills, review = gemini(extracted_text,designation_job,description_job)
                review = gemini(extracted_text,designation_job,description_job)
                # Print the inputs (for demonstration)
                #print(f'Name: {name}, Email: {email}, Job: {goal_job}, Resume: {extracted_text}')

                return render(request, 'response.html', {
                    #'skills': skills,
                    'review': review
                })
        except Exception as e:
            return render(request, 'index.html', {'msg': str(e)})
    else:
        fm = ResumeUploadForm()

    return render(request, 'index.html', {'fm': fm})
