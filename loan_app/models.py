from django.db import models


class Loan(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    balance = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    term = models.IntegerField(null=False)
    rate = models.DecimalField(max_digits=4, decimal_places=3, null=False)
    date = models.DateTimeField(auto_now=False, null=False)
    installment = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    paid = models.BooleanField(default=False)


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT)
    made = models.BooleanField(null=False)
    date = models.DateTimeField(auto_now=False, null=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)