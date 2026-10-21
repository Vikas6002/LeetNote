# notes/forms.py
from django import forms
from .models import Note, Tag


class NoteForm(forms.ModelForm):
    # show tags as checkboxes instead of a multi-select box
    tag = forms.ModelMultipleChoiceField(
        queryset  = Tag.objects.all(),
        widget    = forms.CheckboxSelectMultiple,
        required  = False,
        label     = "Tags"
    )

    # extra field — user pastes LeetCode URL and we auto-fill details
    problem_link = forms.URLField(
        required = False,
        label    = "LeetCode Problem URL",
        help_text= "Paste URL to auto-fill title, difficulty and tags"
    )

    class Meta:
        model  = Note
        fields = [
            'problem_number',
            'title',
            'problem_link',
            'difficulty',
            'language',
            'code',
            'explanation',
            'tag',
            'is_public',
        ]
        widgets = {
            'code'       : forms.Textarea(attrs={'rows': 12, 'class': 'code-area'}),
            'explanation': forms.Textarea(attrs={'rows': 5}),
        }