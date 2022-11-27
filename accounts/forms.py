from django import forms

from .models import User,UserAddress



class ReistrationForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter a password','type':'password','pattern':"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",'id':'psw'
    }))
    confrim_password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter a confrim password','type':'password','pattern':"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
    }))
    
    class Meta:
        model=User
        fields=['email','phone_no','first_name','last_name','password']
        
    def __init__(self,*args,**kwargs):
        super(ReistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter a First Name'
        self.fields['last_name'].widget.attrs['placeholder']  = 'Enter a Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['phone_no'].widget.attrs['placeholder'] = 'Enter Your Phone Number'
                
    

    def clean(self):
        clean=super(ReistrationForm,self).clean()
        password = clean.get('password')
        confrim_password =clean.get('confrim_password')
        if password != confrim_password:
            raise forms.ValidationError('password does not match')
        
        
        
class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email','name':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter a password','name':'password'}))
    
    
    
class ResetPasswod(forms.Form):
    password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter a password','type':'password','pattern':"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",'id':'psw'
    }))
    confrim_password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confrim password','type':'password','pattern':"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
    }))
    
    def clean(self):
        clean=super(ResetPasswod,self).clean()
        password = clean.get('password')
        confrim_password =clean.get('confrim_password')
        if password != confrim_password:
            raise forms.ValidationError('password does not match')
        
class UserAddressForm(forms.ModelForm):
    class Meta:
        model=UserAddress
        fields=['name','phone_no','pincode','locality','address','city_district_town','landmark','alt_phone_no']
        
    def __init__(self,*args,**kwargs):
        super(UserAddressForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter a  Name'
        self.fields['phone_no'].widget.attrs['placeholder']  = 'Enter Your Phone Number'
        self.fields['pincode'].widget.attrs['placeholder'] = 'Enter Your piforncode'
        self.fields['locality'].widget.attrs['placeholder'] = 'Enter Yourlocality '
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Your address'
        self.fields['city_district_town'].widget.attrs['placeholder'] = 'city/district/town'
        self.fields['landmark'].widget.attrs['placeholder'] = 'Enter Your landmark'
        self.fields['alt_phone_no'].widget.attrs['placeholder'] = 'Enter Your alt Phone Number (Optional)'
        for i in self.fields:
            self.fields[i].widget.attrs["required"]='required'
        