from django import forms
from .models import Cantact, Comment

class ContactForm(forms.ModelForm):
    class Meta:
        model = Cantact
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']