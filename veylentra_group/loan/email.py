
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from utils.email_utils import send_resend_email
import logging

logger = logging.getLogger(__name__)


def send_loan_decision_email(loan_application):
    """
    Send email notification when a loan is approved or rejected.
    Uses Resend API.
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
            logger.warning(
                f"Unknown status: {loan_application.status} "
                f"for loan #{loan_application.id}"
            )
            return False

        # Prepare email context
        context = {
            'application': loan_application,
            'username': loan_application.applicant.username,
            'amount': loan_application.amount,
            'purpose': loan_application.purpose,
            'status': loan_application.get_status_display(),
            'duration_months': loan_application.duration_months,
            'employment_status': (
                loan_application.get_employment_status_display()
            ),
            'monthly_income': loan_application.monthly_income,
            'created_at': loan_application.created_at,
            'updated_at': loan_application.updated_at,
            'admin_comment': loan_application.admin_comment,
            'site_url': getattr(
                settings,
                'SITE_URL',
                'https://veylentragroup.com'
            ),
        }

        # Render HTML email
        html_content = render_to_string(template_name, context)

        # Get admin emails
        admin_emails = list(
            User.objects
            .filter(is_staff=True)
            .exclude(email='')
            .values_list('email', flat=True)
        )

        # ---------------------------------------------------------
        # SEND DECISION EMAIL TO APPLICANT VIA RESEND
        # ---------------------------------------------------------
        send_resend_email(
            to=loan_application.applicant.email,
            subject=subject,
            html=html_content
        )

        logger.info(
            f"✅ Decision email sent for loan "
            f"#{loan_application.id} to "
            f"{loan_application.applicant.email} via Resend"
        )

        # ---------------------------------------------------------
        # SEND ADMIN NOTIFICATION VIA RESEND
        # ---------------------------------------------------------
        if admin_emails:
            admin_subject = (
                f"Loan #{loan_application.id} "
                f"Status Update - "
                f"{loan_application.get_status_display()}"
            )

            admin_html = f"""
            <html>
            <body>
                <h2>Loan Application Status Updated</h2>

                <p>
                    <strong>Loan ID:</strong>
                    #{loan_application.id}
                </p>

                <p>
                    <strong>Applicant:</strong>
                    {loan_application.applicant.username}
                </p>

                <p>
                    <strong>Email:</strong>
                    {loan_application.applicant.email}
                </p>

                <p>
                    <strong>Amount:</strong>
                    {loan_application.amount}
                </p>

                <p>
                    <strong>Purpose:</strong>
                    {loan_application.purpose}
                </p>

                <p>
                    <strong>Status:</strong>
                    {loan_application.get_status_display()}
                </p>

                <p>
                    <strong>Duration:</strong>
                    {loan_application.duration_months} months
                </p>

                <p>
                    <strong>Employment Status:</strong>
                    {loan_application.get_employment_status_display()}
                </p>

                <p>
                    <strong>Monthly Income:</strong>
                    {loan_application.monthly_income}
                </p>

                <p>
                    <strong>Admin Comment:</strong>
                    {loan_application.admin_comment or 'None'}
                </p>

                <p>
                    <strong>Updated:</strong>
                    {loan_application.updated_at}
                </p>

                <hr>

                <p>
                    Please review the application in the
                    Veylentra Group administration panel.
                </p>
            </body>
            </html>
            """

            send_resend_email(
                to=admin_emails,
                subject=admin_subject,
                html=admin_html
            )

            logger.info(
                f"✅ Admin decision notification sent for "
                f"loan #{loan_application.id} via Resend"
            )

        return True

    except Exception as e:
        logger.error(
            f"❌ Failed to send decision email for "
            f"loan #{loan_application.id}: {str(e)}",
            exc_info=True
        )
        return False


def send_loan_submission_email(loan_application):
    """
    Send email notification when a loan is submitted.
    Uses Resend API.
    """
    try:
        template_name = 'loan/loan_submitted.html'
        subject = (
            f'📋 Loan Application Submitted - '
            f'#{loan_application.id}'
        )

        # Prepare email context
        context = {
            'application': loan_application,
            'username': loan_application.applicant.username,
            'amount': loan_application.amount,
            'purpose': loan_application.purpose,
            'status': loan_application.get_status_display(),
            'duration_months': loan_application.duration_months,
            'employment_status': (
                loan_application.get_employment_status_display()
            ),
            'monthly_income': loan_application.monthly_income,
            'created_at': loan_application.created_at,
            'updated_at': loan_application.updated_at,
            'admin_comment': loan_application.admin_comment,
            'site_url': getattr(
                settings,
                'SITE_URL',
                'https://veylentragroup.com'
            ),
        }

        # Render HTML email
        html_content = render_to_string(template_name, context)

        # Get admin emails
        admin_emails = list(
            User.objects
            .filter(is_staff=True)
            .exclude(email='')
            .values_list('email', flat=True)
        )

        # ---------------------------------------------------------
        # SEND SUBMISSION EMAIL TO APPLICANT VIA RESEND
        # ---------------------------------------------------------
        send_resend_email(
            to=loan_application.applicant.email,
            subject=subject,
            html=html_content
        )

        logger.info(
            f"✅ Submission email sent for loan "
            f"#{loan_application.id} to "
            f"{loan_application.applicant.email} via Resend"
        )

        # ---------------------------------------------------------
        # SEND ADMIN NOTIFICATION VIA RESEND
        # ---------------------------------------------------------
        if admin_emails:
            admin_subject = (
                f"New Loan Application Submitted "
                f"- #{loan_application.id}"
            )

            admin_html = f"""
            <html>
            <body>
                <h2>New Loan Application</h2>

                <p>
                    <strong>Loan ID:</strong>
                    #{loan_application.id}
                </p>

                <p>
                    <strong>Applicant:</strong>
                    {loan_application.applicant.username}
                </p>

                <p>
                    <strong>Email:</strong>
                    {loan_application.applicant.email}
                </p>

                <p>
                    <strong>Amount:</strong>
                    {loan_application.amount}
                </p>

                <p>
                    <strong>Purpose:</strong>
                    {loan_application.purpose}
                </p>

                <p>
                    <strong>Duration:</strong>
                    {loan_application.duration_months} months
                </p>

                <p>
                    <strong>Employment Status:</strong>
                    {loan_application.get_employment_status_display()}
                </p>

                <p>
                    <strong>Monthly Income:</strong>
                    {loan_application.monthly_income}
                </p>

                <p>
                    <strong>Status:</strong>
                    {loan_application.get_status_display()}
                </p>

                <hr>

                <p>
                    Please review this application in the
                    Veylentra Group administration panel.
                </p>
            </body>
            </html>
            """

            send_resend_email(
                to=admin_emails,
                subject=admin_subject,
                html=admin_html
            )

            logger.info(
                f"✅ Admin submission notification sent for "
                f"loan #{loan_application.id} via Resend"
            )

        return True

    except Exception as e:
        logger.error(
            f"❌ Failed to send submission email for "
            f"loan #{loan_application.id}: {str(e)}",
            exc_info=True
        )
        return False


def test_email():
    """
    Test the Resend email configuration.
    """
    try:
        test_recipient = 'michaelskarsgard07@gmail.com'

        html_content = """
        <html>
        <body>
            <h2>Veylentra Group Email Test</h2>

            <p>
                This is a test email from the Veylentra Group
                loan notification system.
            </p>

            <p>
                If you received this email, the Resend email
                configuration is working correctly.
            </p>
        </body>
        </html>
        """

        send_resend_email(
            to=test_recipient,
            subject='Veylentra Group - Resend Test Email',
            html=html_content
        )

        logger.info(
            f"✅ Test email sent successfully to "
            f"{test_recipient} via Resend"
        )

        return True

    except Exception as e:
        logger.error(
            f"❌ Test email failed: {str(e)}",
            exc_info=True
        )
        return False




# # loan/email.py
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings
# import logging

# logger = logging.getLogger(__name__)


# def send_loan_decision_email(loan_application):
#     """
#     Send email notification when a loan is approved or rejected.
#     """
#     try:
#         # Determine email template and subject based on status
#         if loan_application.status == 'approved':
#             template_name = 'loan/loan_approved.html'
#             subject = f'✅ Loan Application Approved - #{loan_application.id}'
#         elif loan_application.status == 'rejected':
#             template_name = 'loan/loan_rejected.html'
#             subject = f'❌ Loan Application Rejected - #{loan_application.id}'
#         else:
#             logger.warning(f"Unknown status: {loan_application.status} for loan #{loan_application.id}")
#             return False
        
#         # Prepare email context
#         context = {
#             'application': loan_application,
#             'username': loan_application.applicant.username,
#             'amount': loan_application.amount,
#             'purpose': loan_application.purpose,
#             'status': loan_application.get_status_display(),
#             'duration_months': loan_application.duration_months,
#             'employment_status': loan_application.get_employment_status_display(),
#             'monthly_income': loan_application.monthly_income,
#             'created_at': loan_application.created_at,
#             'updated_at': loan_application.updated_at,
#             'admin_comment': loan_application.admin_comment,
#             'site_url': getattr(settings, 'SITE_URL', 'https://veylentragroup.com'),
#         }
        
#         # Render HTML email
#         html_content = render_to_string(template_name, context)
#         text_content = strip_tags(html_content)
        
#         # Get admin emails for BCC
#         from django.contrib.auth.models import User
#         admin_emails = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
        
#         # Send email
#         email = EmailMultiAlternatives(
#             subject=subject,
#             body=text_content,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[loan_application.applicant.email],
#             bcc=admin_emails if admin_emails else None,
#         )
#         email.attach_alternative(html_content, "text/html")
#         email.send(fail_silently=False)
        
#         logger.info(f"✅ Decision email sent for loan #{loan_application.id} to {loan_application.applicant.email}")
#         return True
        
#     except Exception as e:
#         logger.error(f"❌ Failed to send decision email for loan #{loan_application.id}: {str(e)}")
#         import traceback
#         logger.error(traceback.format_exc())
#         return False


# def send_loan_submission_email(loan_application):
#     """
#     Send email notification when a loan is submitted.
#     """
#     try:
#         template_name = 'loan/loan_submitted.html'
#         subject = f'📋 Loan Application Submitted - #{loan_application.id}'
        
#         # Prepare email context
#         context = {
#             'application': loan_application,
#             'username': loan_application.applicant.username,
#             'amount': loan_application.amount,
#             'purpose': loan_application.purpose,
#             'status': loan_application.get_status_display(),
#             'duration_months': loan_application.duration_months,
#             'employment_status': loan_application.get_employment_status_display(),
#             'monthly_income': loan_application.monthly_income,
#             'created_at': loan_application.created_at,
#             'updated_at': loan_application.updated_at,
#             'admin_comment': loan_application.admin_comment,
#             'site_url': getattr(settings, 'SITE_URL', 'https://veylentragroup.com'),
#         }
        
#         # Render HTML email
#         html_content = render_to_string(template_name, context)
#         text_content = strip_tags(html_content)
        
#         # Get admin emails for BCC
#         from django.contrib.auth.models import User
#         admin_emails = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
        
#         # Send email
#         email = EmailMultiAlternatives(
#             subject=subject,
#             body=text_content,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[loan_application.applicant.email],
#             bcc=admin_emails if admin_emails else None,
#         )
#         email.attach_alternative(html_content, "text/html")
#         email.send(fail_silently=False)
        
#         logger.info(f"✅ Submission email sent for loan #{loan_application.id} to {loan_application.applicant.email}")
#         return True
        
#     except Exception as e:
#         logger.error(f"❌ Failed to send submission email for loan #{loan_application.id}: {str(e)}")
#         import traceback
#         logger.error(traceback.format_exc())
#         return False
    



#     # loan/email.py - Add this test function
# def test_email():
#     """Test function to verify email configuration."""
#     try:
#         from django.core.mail import send_mail
#         send_mail(
#             'Test Email',
#             'This is a test email from Veylentra Group.',
#             settings.DEFAULT_FROM_EMAIL,
#             ['michaelskarsgard07@gmail.com'],
#             fail_silently=False,
#         )
#         print("✅ Test email sent successfully!")
#         return True
#     except Exception as e:
#         print(f"❌ Test email failed: {e}")
#         return False