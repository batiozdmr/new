from django import forms
from django.forms import ModelForm, DateInput
from apps.content.models import Event

from django import forms


class PostForm(forms.Form):
    content = forms.CharField(label="Yazı", widget=forms.Textarea(attrs={'placeholder': 'Yazı Yazınız'}),
                              required=False)
    image = forms.ImageField(label=("Resim"), required=False)
    video = forms.ImageField(label=("Video"), required=False)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
