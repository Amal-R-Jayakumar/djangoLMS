from django import forms
from college_or_atc.choices import DISTRICTS
import django_filters
from college_or_atc.models import StudyCenter

class StudyCenterFiltering(django_filters.FilterSet):

    class Meta:
        # district = django_filters.ChoiceFilter(choices=DISTRICTS, label='District:',
        #                               widget=django_filters.Select(attrs={'class': 'form-select pt-3 pb-2'}))
        model = StudyCenter
        fields=['district']
