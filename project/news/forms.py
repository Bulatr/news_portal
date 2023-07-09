from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class SearchForm(forms.Form):
    q = forms.CharField(label='Поиск', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите текст...'}))

class SortForm(forms.Form):
    sort_by = forms.ChoiceField(
        choices=(
            ('name', 'Default sorting'),
            ('popularity', 'Sort by popularity'),
            ('rating', 'Sort by average rating'),
            ('date', 'Sort by newness'),
            ('price', 'Sort by price: low to high'),
            ('price-desc', 'Sort by price: high to low'),
        ),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id' : 'sort_by',
            'onchange': 'handleSortChange(this)',  # Добавляем onchange
        })
    )

class PriceForm(forms.Form):
    price_range = forms.ChoiceField(
        choices=(
            ('0-500', '0 - 500'),
            ('501-900', '501 - 900'),
            ('901-5000', '901 - 5000'),
            ('5001-10000', '5001 - 10000'),
        ),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'price_range',
            'onchange': 'handlePriceChange(this)',  # Добавляем onchange
        })
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'author','typepost', 'category')

    # валидация имени
    def clean_name(self):
        name = self.cleaned_data['title']
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        # Дополнительные проверки и манипуляции с данными
        return name
    # валидация контента
    def clean_content(self):
        content = self.cleaned_data["content"]
        if len(content) < 10:
            raise ValidationError('Описание должно содержать не менее 10 символов.')
        name = self.cleaned_data['title']
        if name == content:
            raise ValidationError("Описание не должно совпадать с именем")
        return content