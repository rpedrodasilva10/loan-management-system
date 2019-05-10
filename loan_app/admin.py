from django.contrib import admin
from .models import Loan, Payment

class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_id', 'amount', 'term', 'rate', 'date', 'installment')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'payment', 'date', 'amount')


admin.site.register(Loan, LoanAdmin)
admin.site.register(Payment, PaymentAdmin)
