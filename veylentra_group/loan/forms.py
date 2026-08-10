from django import forms
from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'amount',
            'purpose',
            'employment_status',
            'monthly_income',
            'duration_months',
        ]
        widgets = {
            'purpose': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Please describe the purpose of your loan...',
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter loan amount',
                'step': '0.01',
                'min': '0',
                'class': 'form-control'
            }),
            'monthly_income': forms.NumberInput(attrs={
                'placeholder': 'Enter your monthly income',
                'step': '0.01',
                'min': '0',
                'class': 'form-control'
            }),
            'duration_months': forms.NumberInput(attrs={
                'placeholder': 'Enter duration in months',
                'min': '1',
                'class': 'form-control'
            }),
            'employment_status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'amount': 'Loan Amount ($)',
            'purpose': 'Purpose of Loan',
            'employment_status': 'Employment Status',
            'monthly_income': 'Monthly Income ($)',
            'duration_months': 'Duration (months)',
        }
        help_texts = {
            'amount': 'Enter the amount you wish to borrow.',
            'purpose': 'Briefly describe why you need this loan.',
            'duration_months': 'How many months do you need to repay the loan?',
        }