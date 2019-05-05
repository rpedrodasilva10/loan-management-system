from django.conf import settings
from django.db import models

class Loan(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    term = models.IntegerField(null=False)
    rate = models.DecimalField(max_digits=4, decimal_places=3, null=False)
    date = models.DateTimeField(null=False)
    installment = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    def __str__(self):
        return (
            'ID:' + str(self.pk) 
            + '-Amount:$' + str(self.amount)
        )

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment = models.CharField(max_length=10, null=False)
    date = models.DateTimeField(auto_now=False, null=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    def __str__(self):
        return (
            'ID:' + str(self.pk) 
            + '-Amount:$' + str(self.amount) 
            + '-Status:' + str(self.payment)
        )