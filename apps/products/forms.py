from django import forms

from apps.products.models import NewProductModel, AllMedia


class ProductForm(forms.ModelForm):
    excel_file = forms.FileField(required=False)

    class Meta:
        model = NewProductModel
        fields = '__all__'


class ImageMultipleChoiceField(forms.MultipleChoiceField):
    def clean(self, value):
        # Преобразуйте выбранные значения в список целочисленных идентификаторов
        value = [int(val) for val in value]
        return super().clean(value)


class AllMediaAdminForm(forms.ModelForm):
    images = ImageMultipleChoiceField(required=False)

    class Meta:
        model = AllMedia
        fields = '__all__'
