from django import forms


class AddSequenceForm(forms.Form):
    sequence = forms.CharField(label='Sequence', max_length=100000, min_length=50)
