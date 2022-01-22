from django import forms
from django.forms import fields
from .models import Question,Response
from .choices import *

class AskQuestionForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICE, label='Topic', widget=forms.Select(attrs={'class': 'form-select'}))
    title = forms.CharField(label="Question",max_length = 350,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Type in your question'}))
    body = forms.CharField(label="Question Description", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Briefly describe your question','rows':3}))
    class Meta:
        model = Question
        fields = ['category','title','body']


class NewResponseForm(forms.ModelForm):
    body = forms.CharField(label="Response", widget=forms.Textarea(attrs={
                           'class': "form-control", 'rows': 4, 'placeholder': 'What are your thoughts?', }))
    class Meta:
        model = Response
        fields = ['body']


class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class':"form-control",
                'rows': 2,
                'placeholder': 'What are your thoughts?'
            })
        }
