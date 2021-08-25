
from django import forms

from apps.member_profile.models import UserProfile, SectorCategory, Sector


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'İsminizi Girin'}))
    surname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Soyisminizi Girin'}))
    e_mail = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'E Posta Adresinizi Girin'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Kullanıcı Adınızı Girin'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Şifrenizi Girin'}))
    confirm_password = forms.CharField(max_length=100,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Şifrenizi Onaylayın'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'user', 'image', 'title', 'biography', 'school', 'department', 'hangouts', 'discord', 'twitter',
            'instagram',
            'facebook', 'website', 'achievement', 'sectors')



class SectorApplicationForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['category','content']

    category = forms.ModelChoiceField(queryset=SectorCategory.objects.all(), label='Sektör Kategori')
    content = forms.CharField(label='İçerik')







