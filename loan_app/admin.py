"""
Admin class for loan_app application.
"""

from django.contrib import admin
from .models import Loan, Payment

class LoanAdmin(admin.ModelAdmin):
    """
    Helper class for admin.
    Defines which Loan fields are shown in the interface.
    """
    list_display = (
        'created', 'finished', 'updated', 'loan_id', 'client_id',
        'amount', 'term', 'rate', 'date', '_outstanding', 'instalment'
    )

class PaymentAdmin(admin.ModelAdmin):
    """
    Helper class for admin.
    Defines which Payment fields are shown in the interface.
    """
    list_display = ('payment_id', 'loan_id', 'payment', 'date', 'amount')


admin.site.register(Loan, LoanAdmin)
admin.site.register(Payment, PaymentAdmin)
