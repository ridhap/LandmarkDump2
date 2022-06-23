from django.forms import Form, ModelForm
from django import forms
from todo_maker.models import Task
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskCreateForm(ModelForm):
    id = forms.CharField(required=False)
    task_accomplished = forms.ChoiceField(
            widget = forms.Select(attrs={'class': "form-control"}),
            choices=[(0, "Task Pending"), (1, "Task Accomplished")],
        )
    class Meta:
        model = Task
        fields = ("id", "title", "description", "task_accomplished",)
        labels = {
            "title" : mark_safe("Task Title {}".format("<span class='required' >*</span>")),
            "task_accomplished" : mark_safe("Task accomplished {}".format("<span class='required' >*</span>")),
        }
        widgets = {
            "title" : forms.TextInput(attrs={'class' : 'form-control'}),
            "description" : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']



class PositionForm(forms.Form):
    position = forms.CharField()
