from django.shortcuts import render
from django.http import HttpResponse
from .forms import ResumeUploadForm
import os
from pdfminer.high_level import extract_text
from docx import Document

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext.lower() == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")
    
# Create your views here.
def home(request):
    if request.method == 'POST':
        try:
            fm = ResumeUploadForm(request.POST,request.FILES)
            if fm.is_valid():
                name = fm.cleaned_data['name']
                email = fm.cleaned_data['email']
                goal_job = fm.cleaned_data['goal_job']
                resume = fm.cleaned_data['resume_file']
                # Print the inputs (for demonstration)
                #print(f'Name: {name}, Email: {email} job: {goal_job}, resume: {resume}')

                extracted_text = extract_text_from_file(resume)
                print(extracted_text)

                return render(request, 'index.html', {'fm':ResumeUploadForm(), 'msg':'Resume Received'})
        except Exception as e:
            #fm = ResumeUploadForm()
            return render(request, 'index.html',{'msg':e})
    else:
        fm = ResumeUploadForm()

    return render(request, 'index.html', {'fm': fm})