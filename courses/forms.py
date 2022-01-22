from django.db.models.fields.files import FileField
from django.forms import DateInput, TimeInput, DateTimeInput
from django.forms import forms
from django import forms
from django.forms import widgets
from django.forms.widgets import FileInput
from django.shortcuts import get_object_or_404
from django.utils import timezone
from accounts.models import User
from .models import Course, Enrollment, SubmitAssignment, Assignment, Resource, TestQuestion


class EnrollmentForm(forms.ModelForm):
    class Meta:
        fields = ['college']
        model = Enrollment


class GradeAssignmentForm(forms.ModelForm):
    grade = forms.IntegerField(label="Marks", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Marks is 4'}))
    class Meta:
        model = SubmitAssignment
        fields = ['grade']


class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('assignment_name', 'assignment_description', 'course')
        # labels = {
        #     'due_date': 'Due Date (yyyy-mm-dd HH:MM)'
        # }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_object = User.objects.filter(username=user.username)
        new_user_object = get_object_or_404(user_object)
        self.fields['course'].queryset = self.fields['course'].queryset.filter(
            instructor=new_user_object.id)


class SubmitAssignmentForm(forms.Form):

    assignment_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SubmitAssignment
        fields = ('topic', 'description', 'assignment_file',
                  'assignment', 'author')

    def clean_assignment_file(self):
        assignment_file = self.cleaned_data.get('assignment_file')
        # try:
        #     main, sub = assignment_file.content_type.split('/')
        #     # print(f'\n\n{main}\n{sub}\n\n')
        #     format_string = ['document', 'ms-word', 'pdf', 'presentation',
        #                      'sheet', 'ms-excel', 'msaccess', 'octet-stream']
        #     if not any(file_format in sub for file_format in format_string):
        #         raise forms.ValidationError(u'Please upload a in microsoft file format.')
        # except AttributeError:
        #     """
        #     Handles case when we are updating the user profile
        #     and do not supply a new assignment_file
        #     """
        #     pass

        return assignment_file
