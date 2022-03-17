from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Department, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2','bio']

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']
