from django.contrib import admin
from django import forms
from rangefilter.filters import DateRangeFilter
from .models import Record
from directories.models import Subcategory

class RecordAdminForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Введите комментарий'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        type = cleaned_data.get('type')
        subcategory = cleaned_data.get('subcategory')


        if category and type and category.type != type:
            raise forms.ValidationError("Выбранная категория не соответствует типу.")


        if subcategory and category and subcategory.category != category:
            raise forms.ValidationError("Выбранная подкатегория не соответствует категории.")

        return cleaned_data

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    form = RecordAdminForm
    list_display = ('date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment')
    list_filter = (
        ('date', DateRangeFilter),
        'status',
        'type',
        'category',
        'subcategory',
    )
    search_fields = ('comment',)
    date_hierarchy = 'date'
    list_select_related = ('status', 'type', 'category', 'subcategory')
    ordering = ('-date',)

    class Media:
        js = (
            'admin/js/jquery.init.js',  # Подключаем jQuery из Django Admin
            'admin/js/record_form.js',  # Наш скрипт
        )