from django import forms
from recipebox.models import Author


class AddAuthor(forms.Form):
    name = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class AddRecipe(forms.Form):
    title = forms.CharField(max_length=100)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=100)
    instructions = forms.CharField(widget=forms.Textarea)
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)