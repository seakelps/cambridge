from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import RankedElement, RankedList


class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("comment", rows=4),
            FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
        )

    class Meta:
        fields = ["comment"]
        model = RankedElement


class OrderedForm(forms.ModelForm):
    class Meta:
        fields = ["ordered"]
        model = RankedList


class VisibilityForm(forms.ModelForm):
    class Meta:
        fields = ["public"]
        model = RankedList
