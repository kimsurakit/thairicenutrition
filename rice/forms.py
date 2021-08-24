from django import forms
from django.forms import formset_factory


SELECT_FIELD_CHOICES = [
    ('riceVarietiesTH', 'Rice varieties (TH)'),
    ('riceVarietiesEN', 'Rice varieties'),
    ('cropSiteProvince', 'Crop Site - Province'),
    ('yearOfAnalysis', 'Year of analysis'),
    ('siteOfAnalysis', 'Site of analysis'),
    ('dataSource', 'Data source'),
    ('riceCategories', 'Rice categories'),
    ('length', 'Length '),
    ('color', 'Color'),
    ('chalkiness', 'Chalkiness'),
    ('amylose', 'Amylose'),
    ('content2AP', '2AP content '),
    ('carbohydrate', 'Carbohydrate'),
    ('protein', 'Protein'),
    ('totalFat', 'Total fat'),
]

CONDITION_CHOICES = [
    ('eq', 'Equal to'),
    ('gt', 'Greater than'),
    ('lt', 'Less Than'),
    ('ct', 'Contains'),
    ('bw', 'Begins with'),
    ('ew', 'Ends with'),
    ('ne', 'Not Equal to'),
]
OPERATION_CHOICES = [('and','AND'),('or','OR')]

class AdcancedSearchForm(forms.Form):
    select_field = forms.CharField(
        required=True,
        label='select field',
        widget=forms.Select(choices=SELECT_FIELD_CHOICES,attrs={
            'class':'form-select'
        })
    )
    Condition = forms.CharField(
        required=True,
        label='Condition',
        widget=forms.Select(choices=CONDITION_CHOICES,attrs={
            'class':'form-select'
        })
    )
    operation = forms.CharField(
        required=True,
        widget=forms.Select(choices=OPERATION_CHOICES,attrs={
            'class':'form-select'
        })
    )
    Keyword = forms.CharField(max_length=250,
    label='Keyword',
    widget=forms.TextInput(attrs={
            'class':'form-text'
        })
    )
AdcancedSearchFormSet = formset_factory(AdcancedSearchForm, extra=1)
