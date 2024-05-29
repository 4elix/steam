from django import forms

from pages.models import Review


class ReviewForm(forms.ModelForm):
    content = forms.CharField(label="Комментарий", widget=forms.Textarea(attrs={
        "class": "form-control form-custom",
        "rows": 5
    }))

    class Meta:
        model = Review
        fields = ["content"]
