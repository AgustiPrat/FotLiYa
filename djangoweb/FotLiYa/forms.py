from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ProposedQuestion

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProposedQuestionForm(forms.ModelForm):
    class Meta:
        model = ProposedQuestion
        fields = ['text', 'category', 'mechanics']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise forms.ValidationError("La pregunta ha de tenir mínim 10 caràcters.")
        return text