from django import forms
from django.utils.text import slugify
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import RankedElement, RankedList


class NameForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        "name",
        Submit("save", "Save"),
        Button("cancel", "Cancel", data_toggle="collapse", data_target="#name_form"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.public:
            self.fields["name"].help_text = (
                "Changing the name of your ballot will also change the share link to your ballot"
            )

    def save(self):
        obj = super().save(commit=False)
        obj.slug = slugify(obj.name)
        obj.save()
        return obj

    class Meta:
        fields = ["name"]
        model = RankedList


class Delete(Button):
    pass


class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("comment", rows=4, placeholder="This candidate..."),
            FormActions(
                Submit("save", "Save changes"),
                Button("cancel", "Cancel"),
                Delete("delete", "Delete", css_class="btn-warning"),
            ),
        )

    class Meta:
        fields = ["comment"]
        labels = {
            "comment": "",
        }
        model = RankedElement


class OrderedForm(forms.ModelForm):
    class Meta:
        fields = ["ordered"]
        model = RankedList


class VisibilityForm(forms.ModelForm):
    class Meta:
        fields = ["public"]
        model = RankedList
