from django.contrib import admin
from .models import Loan, Payment

class LoanAdmin(admin.ModelAdmin):
    list_display = ('created','finished','updated', 'loan_id', 'client_id', 'amount', 'term', 'rate', 'date','_outstanding', 'installment')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'loan', 'payment', 'date', 'amount')


admin.site.register(Loan, LoanAdmin)
admin.site.register(Payment, PaymentAdmin)
