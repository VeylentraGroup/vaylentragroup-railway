# loan/admin.py
from django.contrib import admin
from django.contrib import messages
from .models import LoanApplication


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'applicant', 'amount', 'status', 'created_at']
    list_filter = ['status', 'employment_status', 'created_at']
    search_fields = ['applicant__username', 'applicant__email', 'purpose']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('applicant', 'employment_status', 'monthly_income')
        }),
        ('Loan Details', {
            'fields': ('amount', 'purpose', 'duration_months')
        }),
        ('Admin Section', {
            'fields': ('status', 'admin_comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        count = queryset.count()
        queryset.update(status='approved')
        self.message_user(request, f"{count} application(s) approved.")
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        count = queryset.count()
        queryset.update(status='rejected')
        self.message_user(request, f"{count} application(s) rejected.")
    reject_applications.short_description = "Reject selected applications"