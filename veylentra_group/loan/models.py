from django.db import models
from django.contrib.auth.models import User


class LoanApplication(models.Model):
    """
    Model for storing loan applications submitted by users.
    """
    
    # Status choices for the loan application
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    # Employment status choices
    EMPLOYMENT_CHOICES = [
        ("employed", "Employed"),
        ("self_employed", "Self-employed"),
        ("business_owner", "Business Owner"),
        ("student", "Student"),
        ("unemployed", "Unemployed"),
        ("retired", "Retired"),
    ]
    
    # Applicant - ForeignKey to User model
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="loan_applications",
        help_text="The user who submitted the loan application"
    )
    
    # Loan amount
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="The requested loan amount"
    )
    
    # Purpose of the loan
    purpose = models.TextField(
        help_text="The purpose for which the loan is requested"
    )
    
    # Employment status
    employment_status = models.CharField(
        max_length=30,
        choices=EMPLOYMENT_CHOICES,
        help_text="Current employment status of the applicant"
    )
    
    # Monthly income
    monthly_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Monthly income of the applicant"
    )
    
    # Loan duration in months
    duration_months = models.PositiveIntegerField(
        help_text="Loan duration in months"
    )
    
    # Application status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Current status of the loan application"
    )
    
    # Admin comment (optional)
    admin_comment = models.TextField(
        blank=True,
        null=True,
        help_text="Optional comment from the admin regarding the application"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the application was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the application was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Loan Application"
        verbose_name_plural = "Loan Applications"
    
    def __str__(self):
        return f"{self.applicant.username} - ${self.amount} - {self.get_status_display()}"
    
    def is_pending(self):
        """Check if the application is pending."""
        return self.status == "pending"
    
    def is_approved(self):
        """Check if the application is approved."""
        return self.status == "approved"
    
    def is_rejected(self):
        """Check if the application is rejected."""
        return self.status == "rejected"