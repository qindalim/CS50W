from django import forms

class Createlistingform(forms.Form):
    name = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'step':'0.01', 'min':'0'}))
    image = forms.CharField(widget=forms.URLInput())