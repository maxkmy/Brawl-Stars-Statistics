from django import forms 

class PlayerForm(forms.Form):
	playerTag = forms.CharField(label='Player Tag', max_length=20)
