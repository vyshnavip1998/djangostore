from django import forms

from .models import Person, Course
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data
MATERIAL_CHOICES = (
    ('Note Book', 'Note Book'),
    ('Pen', 'Pen'),
)
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class PersonForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    material = forms.MultipleChoiceField(choices=MATERIAL_CHOICES, widget=forms.CheckboxSelectMultiple)
     #datefield
    birthdate=forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class':'form-control' ,
                'type' :"date" ,
            }
        )
    )
    

    class Meta:
        model = Person
        fields = (
            'name', 'birthdate', 'age','gender',  'phone_number', 'email_id', 'address', 'department', 'course',
            'purpose',
            'material')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['course'].queryset = Course.objects.filter(department_id=department_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.department.course_set.order_by('name')





class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

   
