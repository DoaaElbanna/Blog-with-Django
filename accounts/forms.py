from django import forms
from django.contrib.auth import (
     authenticate,
     get_user_model,
     login,
     logout
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # PasswordInput prevent the user from see the paasword

    # validation
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # another way to check if the user is exist
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)  # check the user is exist
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password ")
            if not user.is_active:
                raise forms.ValidationError("This user no longer active")

        return super(UserLoginForm, self).clean(*args, **kwargs)  # return the default


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email address")  # override the default field
    email2 = forms.EmailField(label="Confirm email")
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            "username",
            "email",  # the order of fields is important for clean function
            "email2",
            "password"
        ]

    # To check the email without concern about the order of fields
    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     email2 = self.cleaned_data.get("email2")
    #     if email != email2:
    #         raise forms.ValidationError("Email must match")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("This email has already been registered")
    #
    #     return super(UserRegisterForm, self).clean(*args, **kwargs)
    # To check the email
    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email != email2:
            raise forms.ValidationError("Email must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")

        return email
