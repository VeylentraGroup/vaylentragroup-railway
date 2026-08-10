# loan/email.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_loan_decision_email(loan_application):
    """
    Send email notification when a loan is approved or rejected.
    """
    try:
        # Determine email template and subject based on status
        if loan_application.status == 'approved':
            template_name = 'loan/loan_approved.html'
            subject = f'✅ Loan Application Approved - #{loan_application.id}'
        elif loan_application.status == 'rejected':
            template_name = 'loan/loan_rejected.html'
            subject = f'❌ Loan Application Rejected - #{loan_application.id}'
        else:
            logger.warning(f"Unknown status: {loan_application.status} for loan #{loan_application.id}")
            return False
        
        # Prepare email context
        context = {
            'application': loan_application,
            'username': loan_application.applicant.username,
            'amount': loan_application.amount,
            'purpose': loan_application.purpose,
            'status': loan_application.get_status_display(),
            'duration_months': loan_application.duration_months,
            'employment_status': loan_application.get_employment_status_display(),
            'monthly_income': loan_application.monthly_income,
            'created_at': loan_application.created_at,
            'updated_at': loan_application.updated_at,
            'admin_comment': loan_application.admin_comment,
            'site_url': getattr(settings, 'SITE_URL', 'https://veylentragroup.com'),
        }
        
        # Render HTML email
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        
        # Get admin emails for BCC
        from django.contrib.auth.models import User
        admin_emails = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
        
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[loan_application.applicant.email],
            bcc=admin_emails if admin_emails else None,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"✅ Decision email sent for loan #{loan_application.id} to {loan_application.applicant.email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send decision email for loan #{loan_application.id}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def send_loan_submission_email(loan_application):
    """
    Send email notification when a loan is submitted.
    """
    try:
        template_name = 'loan/loan_submitted.html'
        subject = f'📋 Loan Application Submitted - #{loan_application.id}'
        
        # Prepare email context
        context = {
            'application': loan_application,
            'username': loan_application.applicant.username,
            'amount': loan_application.amount,
            'purpose': loan_application.purpose,
            'status': loan_application.get_status_display(),
            'duration_months': loan_application.duration_months,
            'employment_status': loan_application.get_employment_status_display(),
            'monthly_income': loan_application.monthly_income,
            'created_at': loan_application.created_at,
            'updated_at': loan_application.updated_at,
            'admin_comment': loan_application.admin_comment,
            'site_url': getattr(settings, 'SITE_URL', 'https://veylentragroup.com'),
        }
        
        # Render HTML email
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        
        # Get admin emails for BCC
        from django.contrib.auth.models import User
        admin_emails = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
        
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[loan_application.applicant.email],
            bcc=admin_emails if admin_emails else None,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"✅ Submission email sent for loan #{loan_application.id} to {loan_application.applicant.email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send submission email for loan #{loan_application.id}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    



    # loan/email.py - Add this test function
def test_email():
    """Test function to verify email configuration."""
    try:
        from django.core.mail import send_mail
        send_mail(
            'Test Email',
            'This is a test email from Veylentra Group.',
            settings.DEFAULT_FROM_EMAIL,
            ['michaelskarsgard07@gmail.com'],
            fail_silently=False,
        )
        print("✅ Test email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Test email failed: {e}")
        return False