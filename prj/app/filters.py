from django.forms import DateInput
from django_filters import DateFilter
from django_filters import FilterSet, ModelChoiceFilter

from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label="Любая",
    )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'post_text': ['icontains'],
        }

    added_after = DateFilter(
        field_name='post_date',
        lookup_expr='gt',
        label='Дата позже',
        widget=DateInput(attrs={'type': 'date'}))
