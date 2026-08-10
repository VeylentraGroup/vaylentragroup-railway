# loan/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LoanApplication
from .forms import LoanApplicationForm
import logging

logger = logging.getLogger(__name__)


@login_required
def apply_for_loan(request):
    """View for users to apply for a loan."""
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.applicant = request.user
            loan.save()  # This triggers the post_save signal to send email
            
            messages.success(request, 'Your loan application has been submitted successfully! A confirmation email has been sent to your registered email address.')
            return redirect('loan:loan_status')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoanApplicationForm()
    
    return render(request, 'loan/apply.html', {'form': form})


@login_required
def loan_status(request):
    """View for users to see their loan applications."""
    applications = LoanApplication.objects.filter(applicant=request.user).order_by('-created_at')
    return render(request, 'loan/status.html', {'applications': applications})


@login_required
def loan_detail(request, pk):
    """View for users to see details of a specific loan application."""
    application = get_object_or_404(LoanApplication, pk=pk, applicant=request.user)
    return render(request, 'loan/detail.html', {'application': application})