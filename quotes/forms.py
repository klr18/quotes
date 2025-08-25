from itertools import count

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import *

class QuoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настраиваем поле категории
        self.fields['source'].empty_label = 'Источник не выбран'

    def clean_quote_text(self):
        quote = self.cleaned_data['quote_text']
        existing = Quote.objects.filter(quote_text=quote).exists()
        if existing:
            raise ValidationError('Такая цитата уже существует')

        return quote

    def clean_source(self):
        source = self.cleaned_data['source']
        amount = Quote.objects.filter(source=source).count()
        if amount == 3:
            raise ValidationError('Количество цитат у одного источника не должно превышать 3')

        return source

    class Meta:
        model = Quote
        fields = ('quote_text', 'weight', 'source')
        labels = {'quote_text': 'Текст цитаты', 'weight': 'Вероятность выпадения цитаты', 'source': 'Источник'}

class SourceForm(ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        existing = Source.objects.filter(name=name).exists()
        if existing:
            raise ValidationError('Такой источник уже существует')

        return name

    class Meta:
        model = Source
        fields = ('name',)
        labels = {'name': 'Название источника'}