from django import forms


class UserForm(forms.Form):
    login = forms.CharField(max_length=30, label='Логин')
    password1 = forms.CharField(
        max_length=30,
        min_length=6,
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        max_length=30,
        min_length=6,
        label='Повторите пароль',
        widget=forms.PasswordInput
    )
    email = forms.EmailField(widget=forms.EmailInput)
    photo = forms.ImageField(label='Аватарка')

    def clean_password2(self):
        data = self.cleaned_data['password2']
        pass_origin = self.cleaned_data['password1']
        if pass_origin != data:
            raise forms.ValidationError('Пароли должны совпадать')
        return data


class UserProfileForm(forms.Form):
    login = forms.CharField(max_length=50, label='Логин', disabled=True, required=False)
    email = forms.EmailField(widget=forms.EmailInput)
    photo = forms.ImageField(label='Аватарка', required=False)



