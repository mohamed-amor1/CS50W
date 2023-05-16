from django import forms
from django.core.validators import MinValueValidator
from .models import Listing, Comment, Bid


class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    description = forms.CharField(
        label="Description", max_length=500, widget=forms.Textarea(attrs={"rows": 4})
    )
    starting_bid = forms.DecimalField(
        label="Starting Bid",
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(
            attrs={"placeholder": "$", "type": "number", "step": "0.01"}
        ),
    )
    image = forms.URLField(
        label="Image URL", required=False, widget=forms.URLInput(attrs={"size": 40})
    )

    category = forms.ChoiceField(label="Category", choices=Listing.CATEGORY_CHOICES)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Your comment",
                    "class": "form-control comment-form",
                }
            ),
        }


class BidForm(forms.ModelForm):
    amount = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Bid",
            }
        )
    )

    class Meta:
        model = Bid
        fields = ("amount",)
