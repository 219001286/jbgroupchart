from django.forms import ModelForm
from .models import Department


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['host', 'participants']