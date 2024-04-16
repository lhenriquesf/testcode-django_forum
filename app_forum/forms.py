from django import forms
from django.contrib.auth import get_user_model
from .models import Topic, Comment
from django.core.exceptions import ValidationError
from datetime import date

CustomUser = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'date_of_birth', 'password']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

        if age < 14:
            raise ValidationError("Você deve ter pelo menos 14 anos para se registrar.")
        return date_of_birth

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso por outro usuário.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'category', 'content']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso por outro usuário.")
        return email
