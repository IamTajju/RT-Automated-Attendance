from django import forms
from .models import Ocr


class ImageUpload(forms.ModelForm):
    class Meta:
        model = Ocr
        fields = ['image']


class GradeForm(forms.Form):
    grade = forms.ChoiceField(choices=(
        ("9", "Grade 9"), ("10", "Grade 10"), ("11", "Grade 11"), ("12", "Grade 12")), label="Select Grade")
