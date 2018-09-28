# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class LoginFom(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginFom, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином не зарегистрирован в системе!')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')





class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_check',
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Ваш email'
        self.fields['email'].help_text = 'Пожалуйста, указывайте реальный адрес'

    # def clean(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('Пользователь с данным логином уже есть в системе!')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({
                'username': 'Пожалуйста выберите другое имя пользователя, т.к. пользователь с таким логином уже зарегистрирован в системе!'},
                code='user exists')

        if password != password_check:
            raise forms.ValidationError({
                'password': '',
                'password_check': 'Вы ошиблись при вводе паролей, они не совпадают, введите повторно!'},
                code='passwords do not match', )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError({'email': 'Пользователь с таким email уже зарегистрирован!'},
                                        code='email exists')

class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(),choices=([("self", "Самовывоз"), ("delivery", "Доставка")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Контактный телефон'
        self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому можно связаться с Вами'
        self.fields['buying_type'].label = 'Способ получения заказа'
        self.fields['address'].label = 'Адрес доставки'
        self.fields['address'].help_text = '*Обязательно указывайте город!'
        self.fields['comments'].label = 'Комментарии к заказу'
        self.fields['date'].label = 'Дата доставки'
        self.fields['date'].help_text = 'Доставка производится на следующий день после оформления заказа. Менеджер предварительно свяжется с вами.'
