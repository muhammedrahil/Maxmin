from dataclasses import field
from django import forms

from .models import Category



class CategoryForm(forms.ModelForm):
    
    class Meta:
        model=Category
        fields= ['category','parent','description']
        
    def __init__(self,*args,**kwargs):
            super(CategoryForm,self).__init__(*args,**kwargs)
            self.fields['category'].widget.attrs['placeholder'] = 'Enter a  category'
            self.fields['description'].widget.attrs['placeholder'] = 'Enter description'
            for i in self.fields:
                self.fields[i].widget.attrs['class'] = 'form-control'
            # if self.fields['level'] == 0:
            #         self.fields['parent'].widget.attrs['readonly'] = True
            