from django import forms
from cr.models import University, Department

class UniversityForm(forms.ModelForm):
    """Form for creating and editing universities"""
    
    class Meta:
        model = University
        fields = ['title', 'type', 'address']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input1',
                'placeholder': 'Enter university name',
                'required': True
            }),
            'type': forms.Select(attrs={
                'class': 'form-input1',
                'required': True
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input1',
                'placeholder': 'Enter university address'
            }),
        }
        labels = {
            'title': 'University Name',
            'type': 'University Type',
            'address': 'Address'
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Check if university with this title already exists (excluding current instance in edit mode)
        qs = University.objects.filter(title__iexact=title)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('A university with this name already exists.')
        return title


class DepartmentForm(forms.ModelForm):
    """Form for creating and editing departments"""
    
    class Meta:
        model = Department
        fields = ['title', 'code']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input1',
                'placeholder': 'Enter department name',
                'required': True
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-input1',
                'placeholder': 'Enter department code (e.g., CSE, EEE)'
            }),
        }
        labels = {
            'title': 'Department Name',
            'code': 'Department Code'
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Check if department with this title already exists (excluding current instance in edit mode)
        qs = Department.objects.filter(title__iexact=title)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('A department with this name already exists.')
        return title
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            # Check if department with this code already exists (excluding current instance in edit mode)
            qs = Department.objects.filter(code__iexact=code)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('A department with this code already exists.')
        return code