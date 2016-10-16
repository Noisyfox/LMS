from django import forms
from django.utils.translation import ugettext_lazy as _

from LMS.models import GENDERS, Course


class DateInput(forms.DateInput):
    input_type = 'date'


class StudentEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, min_length=2, label=_('First Name'), strip=True)
    last_name = forms.CharField(max_length=30, min_length=2, label=_('Last Name'), strip=True)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label=_('Gender'))
    year = forms.IntegerField(label=_('Year'))
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label=_('Course'))
    start_date = forms.DateField(label=_('Start Date'), widget=DateInput())
    password = forms.CharField(label=_('Password'))
