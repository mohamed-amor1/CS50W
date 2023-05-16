from django import forms
from django.core.validators import MinValueValidator
from .models import Listing, Comment, Bid


class CreateListingForm(forms.Form):
    """
    Form for creating a new listing.
    """

    title = forms.CharField(
        label="Title", max_length=200
    )  # Field for the title of the listing
    description = forms.CharField(
        label="Description", max_length=500, widget=forms.Textarea(attrs={"rows": 4})
    )  # Field for the description of the listing
    starting_bid = forms.DecimalField(
        label="Starting Bid",
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(
            attrs={"placeholder": "$", "type": "number", "step": "0.01"}
        ),
    )  # Field for the starting bid of the listing
    image = forms.URLField(
        label="Image URL", required=False, widget=forms.URLInput(attrs={"size": 40})
    )  # Field for the image URL of the listing

    category = forms.ChoiceField(
        label="Category", choices=Listing.CATEGORY_CHOICES
    )  # Field for selecting the category of the listing


class CommentForm(forms.ModelForm):
    """
    Form for adding a comment to a listing.
    """

    class Meta:
        model = Comment  # Associate the form with the Comment model
        fields = ("text",)  # Include only the 'text' field from the Comment model
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Your comment",
                    "class": "form-control comment-form ",
                }
            ),
        }  # Customize the 'text' field widget appearance


class BidForm(forms.ModelForm):
    """
    Form for placing a bid on a listing.
    """

    amount = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control bid-form",
                "placeholder": "Bid",
            }
        )
    )  # Field for entering the bid amount

    class Meta:
        model = Bid  # Associate the form with the Bid model
        fields = ("amount",)  # Include only the 'amount' field from the Bid model
