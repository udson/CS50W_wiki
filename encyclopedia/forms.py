from django import forms

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class NewEntryForm(EditEntryForm):
    title = forms.CharField(required=True)