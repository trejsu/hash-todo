from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['user', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}, format='YYYY-MM-DD')
        }

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ''
