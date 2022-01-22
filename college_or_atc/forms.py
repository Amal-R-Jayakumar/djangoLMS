from college_or_atc.choices import INSTITUTES, DISTRICTS
from college_or_atc.models import StudyCenter
from accounts.models import Profile, User
from courses.models import Course,Enrollment
from phonenumber_field.formfields import PhoneNumberField
from django import forms


class StudyCenterForm(forms.ModelForm):
    institute = forms.ChoiceField(choices=INSTITUTES, label='Study Center Type:',
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    name = forms.CharField(label="Name of Institute: ", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Institute Name'}))
    address = forms.CharField(label="Address of Institute: ", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Institute Address','rows': 4}))
    district= forms.ChoiceField(choices=DISTRICTS, label='Select District:',
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    code = forms.CharField(label="Institute Code: ", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Institute Code'}))
    hardware = forms.BooleanField(label="Hardware", widget=forms.CheckboxInput(
        attrs={'class': 'form-check-label'}))
    software = forms.BooleanField(label="Software", widget=forms.CheckboxInput(
        attrs={'class': 'form-check-label'}))
    multimedia = forms.BooleanField(label="Multimedia", widget=forms.CheckboxInput(
        attrs={'class': 'form-check-label'}))

    class Meta:
        model = StudyCenter
        fields = ('institute', 'name', 'code', 'address','district',
                  'hardware', 'software', 'multimedia')

    def __init__(self, *args, **kwargs):
        super(StudyCenterForm, self).__init__(*args, **kwargs)
        self.fields['hardware'].required = False
        self.fields['software'].required = False
        self.fields['multimedia'].required = False


class AddStudentForm(forms.ModelForm):
    name = forms.CharField(label="Name of Student", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    contact_number = forms.CharField(label='Phone Number with Country Code', widget=forms.TextInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))
    gender = forms.CharField(label="Gender", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Gender'}))

    class Meta:
        fields = ['name', 'email', 'contact_number', 'gender']
        model = User


class StudentProfileForm(forms.ModelForm):
    qualification = forms.CharField(label="Course Currently Pursued", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Course Currently Pursued'}))

    class Meta:
        model = Profile
        fields = ['qualification']


class AddATCAdminForm(forms.ModelForm):
    name = forms.CharField(label="Name of ATC Director", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    contact_number = forms.CharField(label='Phone Number', widget=forms.TextInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))

    class Meta:
        fields = ['name', 'email', 'contact_number']
        model = User

class AddStudentAdminForm(forms.ModelForm):
    name = forms.CharField(label="Name of Student", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    contact_number = forms.CharField(label='Phone Number with Country Code', widget=forms.TextInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))

    class Meta:
        fields = ['name', 'email', 'contact_number']
        model = User



class ATCProfileForm(forms.ModelForm):
    address = forms.CharField(label='Address*:', widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'floatingDob', 'placeholder': "Enter Home Address*", 'rows': 4}))

    class Meta:
        model = Profile
        fields = ['address']


from college_or_atc.choices import INSTITUTES,DISTRICTS
from college_or_atc.models import CollegeAddingStudents, StudyCenter
from accounts.models import Profile, User
from courses.models import Course,Enrollment
from phonenumber_field.formfields import PhoneNumberField
from django import forms


class StudyCenterForm(forms.ModelForm):
    institute = forms.ChoiceField(choices=INSTITUTES, label='Study Center Type:',
                                  widget=forms.Select(attrs={'class': 'form-select pt-3 pb-2'}))
    name = forms.CharField(label="Name of Institute: ", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Institute Name'}))
    address = forms.CharField(label="Address of the Institute: ", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Institute Address'}))
    district= forms.ChoiceField(choices=DISTRICTS, label='Select District:',
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    code = forms.CharField(label="Institute Code: ", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Institute Code'}))
    hardware = forms.BooleanField(label="Hardware", widget=forms.CheckboxInput(
        attrs={'class': 'form-check-label'}))
    software = forms.BooleanField(label="Software", widget=forms.CheckboxInput(
        attrs={'class': 'form-check-label'}))
    multimedia = forms.BooleanField(label="Multimedia", widget=forms.CheckboxInput(
        attrs={'class': 'form-check-label'}))

    class Meta:
        model = StudyCenter
        fields = ('institute', 'name', 'code', 'address', 'district',
                  'hardware', 'software', 'multimedia')

    def __init__(self, *args, **kwargs):
        super(StudyCenterForm, self).__init__(*args, **kwargs)
        self.fields['hardware'].required = False
        self.fields['software'].required = False
        self.fields['multimedia'].required = False


class AddStudentForm(forms.ModelForm):
    name = forms.CharField(label="Name of Student", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    contact_number = forms.CharField(label='Phone Number with Country Code', widget=forms.TextInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))
    gender = forms.CharField(label="Gender", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Gender'}))

    class Meta:
        fields = ['name', 'email', 'contact_number', 'gender']
        model = User


class StudentProfileForm(forms.ModelForm):
    qualification = forms.CharField(label="Course Currently Pursued", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Course Currently Pursued'}))

    class Meta:
        model = Profile
        fields = ['qualification']


class AddATCAdminForm(forms.ModelForm):
    name = forms.CharField(label="Name of ATC Director", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    contact_number = forms.CharField(label='Phone Number', widget=forms.TextInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))

    class Meta:
        fields = ['name', 'email', 'contact_number']
        model = User

class AddStudentAdminForm(forms.ModelForm):
    name = forms.CharField(label="Name of Student", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    contact_number = forms.CharField(label='Phone Number', widget=forms.TextInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))

    class Meta:
        fields = ['name', 'email', 'contact_number']
        model = User



class ATCProfileForm(forms.ModelForm):
    address = forms.CharField(label='Address*:', widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'floatingDob', 'placeholder': 'Enter Your Home Address*', 'rows': 4}))

    class Meta:
        model = Profile
        fields = ['address']

class CollegeAddingStudentsForm(forms.ModelForm):
    selected_course=forms.ModelChoiceField(queryset=Course.objects.all(), label='Study Center Type:',widget=forms.Select(attrs={'class': 'form-select pt-3 pb-2'}))
    name = forms.CharField(label="Name of Student", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    contact_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))

    class Meta:
        fields = ['selected_course', 'name', 'email', 'contact_number']
        model = CollegeAddingStudents
