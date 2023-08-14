from django import forms
from .models import Account


class SignupForm(forms.ModelForm):
    password2=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':'Type password again'
    }),label="Confirm Password")
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']
        widgets={'first_name':forms.TextInput(attrs={'placeholder':'Enter first name '}),
                 'last_name':forms.TextInput(attrs={'placeholder':'Enter last name '}),
                 'email':forms.EmailInput(attrs={'placeholder':'Enter your email '}),
                 'phone_number':forms.TextInput(attrs={'placeholder':'Enter phone number '}),
                 'password':forms.PasswordInput(attrs={'placeholder':'Enter your password '}),
                 }
        
    def __init__(self,*args,**kwargs):
        super(SignupForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    
    def clean_phone_number(self):
        phone=self.cleaned_data['phone_number']
        if len(str(phone))!=10:
            raise forms.ValidationError("phone number must be 10 digit only")
        return phone 
      
    def clean(self):
        cleaned_data=super(SignupForm,self).clean()
        password=cleaned_data.get('password')
        conf_password=cleaned_data.get('password2')
        if password!=conf_password:
            raise forms.ValidationError("Password does not match!")
        return cleaned_data
    
class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'form-control'}
    ))
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}))
    
    
    def clean_email(self):
        email=self.cleaned_data['email']
        print(email)
        emailids=Account.objects.values_list('email',flat=True)
        print(emailids,type(emailids))
        if email not in emailids:
            raise forms.ValidationError("This email id is not registered !")
        if len(str(email))==0:
            raise forms.ValidationError("please enter email")
        return email