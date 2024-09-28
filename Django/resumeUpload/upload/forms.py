from django import forms


class ResumeUploadForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    goal_job = forms.CharField(max_length=50)
    resume_file = forms.FileField()