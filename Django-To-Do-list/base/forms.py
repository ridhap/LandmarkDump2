from django import forms
from django.contrib.auth.models import User

# Reordering Form and View

class Meta:
        model=User
        feilds=("username","password1","password2")
        
class PositionForm(forms.Form):
    position = forms.CharField()
