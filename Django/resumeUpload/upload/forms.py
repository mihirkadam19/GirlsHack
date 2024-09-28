from django import forms
from .validators import validate_file_extension

class ResumeUploadForm(forms.Form):
    name = forms.CharField(max_length=50,required=True,label="Full Name")
    email = forms.CharField(max_length=50,required=True,label="Email")
    goal_job = forms.CharField(max_length=50,required=True,label="Goal Job")
    resume_file = forms.FileField(required=False,label="Upload Resume",validators=[validate_file_extension])