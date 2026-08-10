from django.urls import path
from . import views


app_name = "loan"


urlpatterns = [
    path(
        "apply/",
        views.apply_for_loan,
        name="apply",
    ),
    path(
        "status/",
        views.loan_status,
        name="loan_status",
    ),
    # Optional: Add a detail view for specific loan applications
    path(
        "<int:pk>/",
        views.loan_detail,
        name="detail",
    ),
]