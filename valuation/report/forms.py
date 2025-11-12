from django import forms
from .models import Valuation, Property, Owner, Plot
from django.forms import inlineformset_factory


class ValuationForm(forms.ModelForm):
    class Meta:
        model = Valuation
        exclude = ['created_at']  # Exclude auto-generated field
        widgets = {
            'val_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bank_req_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'report_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., VAL-2025-001'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Name'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Branch'}),
            'bank_ref_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Reference Number'}),
            'bank_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Bank Address'}),
            'borrower_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Borrower Full Name'}),
            'borrower_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'borrower_pan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PAN Number'}),
            'borrower_citizenship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citizenship Number'}),
            'borrower_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Borrower Address'}),
        }
    
    def clean_report_number(self):
        report_number = self.cleaned_data.get('report_number')
        if report_number:  # Only check if report_number is provided
            if Valuation.objects.filter(report_number=report_number).exists():
                raise forms.ValidationError("This report number already exists. Please use a unique report number.")
        return report_number
    
    def clean_borrower_contact(self):
        contact = self.cleaned_data.get('borrower_contact')
        if contact:
            if not contact.isdigit():
                raise forms.ValidationError("Contact number should contain only digits.")
            if len(contact) != 10:
                raise forms.ValidationError("Contact number must be 10 digits.")
        return contact
    
    def clean_borrower_pan(self):
        pan = self.cleaned_data.get('borrower_pan')
        if pan and len(pan) != 10:
            raise forms.ValidationError("PAN number must be 10 characters.")
        return pan

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['valuation', 'created_at']  # Exclude valuation and created_at
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Property Address'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
            'municipality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Municipality'}),
            'ward_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ward Number'}),
            'land_type': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make name and address required
        self.fields['name'].required = True
        self.fields['address'].required = True
        self.fields['district'].required = True

        
class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        exclude = ['created_at']  # Exclude auto-generated field
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'citizenship_number': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if contact:
            if not contact.isdigit():
                raise forms.ValidationError("Contact number should contain only digits.")
            if len(contact) != 10:
                raise forms.ValidationError("Contact number must be 10 digits.")
        return contact

class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        exclude = ['created_at', 'area_sqft', 'area_sqmt', 'gov_value', 'market_value', 'fair_market_value']
        widgets = {
            'plot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sheet_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ropani': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
            'ana': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '15', 'step': '1'}),
            'paisa': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '3', 'step': '1'}),
            'dam': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '4', 'step': '0.0001'}),
            'bigha': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
            'kattha': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '19', 'step': '1'}),
            'dhur': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '19', 'step': '1'}),
            'market_rate_per_sqft': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'north_boundary': forms.TextInput(attrs={'class': 'form-control'}),
            'south_boundary': forms.TextInput(attrs={'class': 'form-control'}),
            'east_boundary': forms.TextInput(attrs={'class': 'form-control'}),
            'west_boundary': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate Nepali measurement systems
        ana = cleaned_data.get('ana', 0)
        paisa = cleaned_data.get('paisa', 0)
        dam = cleaned_data.get('dam', 0)
        kattha = cleaned_data.get('kattha', 0)
        dhur = cleaned_data.get('dhur', 0)
        
        if ana < 0 or ana > 15:
            self.add_error('ana', 'Ana must be between 0 and 15')
        
        if paisa < 0 or paisa > 3:
            self.add_error('paisa', 'Paisa must be between 0 and 3')
        
        if dam < 0 or dam > 4:
            self.add_error('dam', 'Dam must be between 0 and 4')
        
        if kattha < 0 or kattha > 19:
            self.add_error('kattha', 'Kattha must be between 0 and 19')
        
        if dhur < 0 or dhur > 19:
            self.add_error('dhur', 'Dhur must be between 0 and 19')
        
        return cleaned_data


OwnerFormSet = inlineformset_factory(
    Property, Owner, form=OwnerForm, 
    extra=1, can_delete=True, fields='__all__'
)

PlotFormSet = inlineformset_factory(
    Property, Plot, form=PlotForm,
    extra=1, can_delete=True, fields='__all__'
)