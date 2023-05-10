from django import forms


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 50,
                "placeholder": "Write in markdown a new entry",
            }
        ),
    )


class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 50,
                "placeholder": "Edit this entry in markdown",
            }
        ),
    )
