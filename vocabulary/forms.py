from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.


class AddNewForm(forms.Form):
    new_word = forms.CharField(help_text="Enter new english word here")
    translation = forms.CharField(help_text="Enter translation here", required = False)

    def clean_data(self):
        new_word_cl = self.cleaned_data['new_word']
        translation_cl = self.cleaned_data['translation']

        # Помните, что всегда надо возвращать "очищенные" данные.
        return new_word_cl, translation_cl

class ChoseNumberForm(forms.Form):
    number_of_words = forms.IntegerField(help_text="Enter a number of last words here", required = False)

    def clean_data(self):
        number_of_words_cl = self.cleaned_data['number_of_words']
        return number_of_words_cl
