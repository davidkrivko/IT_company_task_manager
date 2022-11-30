from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator

from manager.models import Worker, Task


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position")


class DescriptionUpdateForm(forms.ModelForm):
    description = forms.CharField(
        required=True,
        validators=[MinLengthValidator(limit_value=100, message="Input some more")],
    )

    class Meta:
        model: Task
        fields = ("description",)


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )
