from django import forms
from django.forms import Textarea
from django.apps import apps
Resume = apps.get_model('api', 'Resume')
status_choice = (
    ("1", "List Parsed"),
    ("2", "List Not Parsed"),
    ("3", "List All"),
)
class ResForm(forms.ModelForm):
    resume = forms.FileField(required =True)
    class Meta:
        model = Resume
        fields = ('resume',)

class DetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = False    
    class Meta:
        model = Resume
        fields = '__all__'
        exclude = ('resume','text','is_parsed',)
        required = (
            'name',
            'phone',
            'email',
            'skills',
            'designation',
            'degree',
            'college',
            'experience',
        )
        widgets = {
            'phone': Textarea(attrs={'cols': 40, 'rows': 1, 'placeholder':"Not found"}),
            'skills': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder':"Not found"}),
            'designation': Textarea(attrs={'cols': 80, 'rows': 1, 'placeholder':"Not found"}),
            'degree': Textarea(attrs={'cols': 80, 'rows': 1, 'placeholder':"Not found"}),
            'college': Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder':"Not found"}),
            'experience': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder':"Not found"}),
        }

class FilterForm(forms.Form):
    status = forms.ChoiceField(choices=status_choice)
    date_from = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))

class ExcelForm(forms.Form):
    date_from = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))
    

