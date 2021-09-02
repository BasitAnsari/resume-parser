from django import forms

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
class FilterForm(forms.Form):
    status = forms.ChoiceField(choices=status_choice)
    date_from = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))

class ExcelForm(forms.Form):
    date_from = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))
    

