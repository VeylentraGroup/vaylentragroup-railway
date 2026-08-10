# loan/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import LoanApplication
from .email import send_loan_decision_email, send_loan_submission_email
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=LoanApplication)
def loan_status_changed(sender, instance, **kwargs):
    """
    Send email when loan status changes to approved or rejected.
    """
    # If this is a new instance (no pk), skip
    if not instance.pk:
        return

    try:
        old_loan = LoanApplication.objects.get(pk=instance.pk)
    except LoanApplication.DoesNotExist:
        return

    # Check if status has changed
    if old_loan.status != instance.status:
        logger.info(f"🔄 Loan #{instance.id} status changed from {old_loan.status} to {instance.status}")
        
        # Send email for approved or rejected status
        if instance.status in ["approved", "rejected"]:
            logger.info(f"📧 Sending decision email for loan #{instance.id} - Status: {instance.status}")
            result = send_loan_decision_email(instance)
            
            if result:
                logger.info(f"✅ Decision email sent successfully for loan #{instance.id}")
            else:
                logger.error(f"❌ Failed to send decision email for loan #{instance.id}")


@receiver(post_save, sender=LoanApplication)
def loan_created_notification(sender, instance, created, **kwargs):
    """
    Send email when a new loan application is created.
    """
    if created:
        logger.info(f"🆕 New loan application created - #{instance.id}")
        result = send_loan_submission_email(instance)
        
        if result:
            logger.info(f"✅ Submission email sent for loan #{instance.id}")
        else:
            logger.error(f"❌ Failed to send submission email for loan #{instance.id}")