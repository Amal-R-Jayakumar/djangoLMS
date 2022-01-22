from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
from accounts.models import User
from django.db import models
from phonenumber_field.formfields import PhoneNumberField
from .models import Contact, Profile
from django.core.files.images import get_image_dimensions


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('Incorrect Email or Password')

            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Email or Password')

        return super(UserLoginForm, self).clean(*args, **kwargs)



class UserSignUpForm(UserCreationForm):
    class Meta:
        fields = ('name', 'contact_number', 'email','gender',
                  'password1', 'password2')
        model = User

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError(
                'This email is already in use. Please Pick another one.')
        return email


class SignupProfileForm(forms.ModelForm):
    dob = forms.DateField(label='Date of Birth*', widget=forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY', 'id': 'inputDate'}), input_formats=settings.DATE_INPUT_FORMATS)
    address = forms.CharField(label='Address*:', widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'floatingDob', 'placeholder': 'Enter Your Home Address*', 'rows': 4}))
    qualification = forms.CharField(label='Course Currently Pursued*:', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id':"floatingQualification", 'placeholder': 'Course(Degree) Currently Pursued*'}))
    class Meta:
        fields = ['dob', 'address', 'qualification']
        model = Profile

class userUpdateForm(forms.ModelForm):
    gender = forms.CharField(
        label='Gender*', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gender*'}))
    class Meta:
        model = User
        fields = ['gender']

class NonStudentUserUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Name*', widget=forms.TextInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Full Name*'}))
    email = forms.EmailField(label='Email*', widget=forms.EmailInput(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Email*'}))
    contact_number = PhoneNumberField(label='Contact Number',
                                      widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))
    class Meta:
        model = User
        fields = ['name', 'email', 'contact_number']


class profileUpdateForm(forms.ModelForm):
    dob = forms.DateField(label='Date of Birth*', widget=forms.DateInput(format='%d/%m/%Y',
        attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY','id':'inputDate'}),input_formats=settings.DATE_INPUT_FORMATS)
    address = forms.CharField(label='Address*:', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Home Address*', 'rows': 3}))
    qualification = forms.CharField(label='Course Currently Pursued*:', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Course(Degree) Currently Pursued*'}))
    profile_pic = forms.ImageField(label="Profile Picture", required=True, widget=forms.FileInput(
        attrs={'class': 'form-control', 'placeholder': 'Upload Your Profile Picture*'}))

    class Meta:
        model = Profile
        fields = ['dob', 'address', 'qualification', 'profile_pic']

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data['profile_pic']

        try:
            w, h = get_image_dimensions(profile_pic)

            # validate dimensions
            # max_width = max_height = 768
            # if w > max_width or h > max_height:
            #     raise forms.ValidationError(
            #         f'Please use an image that is {max_width} x {max_height} pixels or smaller.')

            # validate content type
            main, sub = profile_pic.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # #validate file size
            # if len(profile_pic) > (20 * 1024):
            #     raise forms.ValidationError(
            #         u'profile_pic file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new profile_pic
            """
            pass

        return profile_pic


class ContactForm(forms.ModelForm):
    name=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control rounded-0','placeholder':'Full Name*'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Email*'}))
    contact_number = PhoneNumberField(help_text="Enter phone number with country code +91",label='', widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Phone Number*'}))
    message = forms.CharField(label='', widget=forms.Textarea(
        attrs={'class': 'form-control rounded-0', 'placeholder': 'Message*', 'rows': 5}))
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact_number','message']
