"""Missing: DOCSTRING"""

from django.db import models

class Loan(models.Model):
    """
    Stores the loans entries.
    """
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    term = models.IntegerField(null=False)
    rate = models.DecimalField(max_digits=4, decimal_places=4, null=False)
    date = models.DateTimeField(null=False)

    @property
    def installment(self):
        """
        Derived attribute.
        """
        r = float(self.rate) / 12.0 # pylint: disable=invalid-name
        return (r + r / ((1 + r) ** float(self.term) - 1)) * float(self.amount)

    def __str__(self):
        return f'{self.id}'

class Payment(models.Model):
    """Missing: DOCSTRING"""
    MADE = 'made'
    MISSED = 'missed'
    PAYMENT_CHOICES = (
        (MADE, 'made'),
        (MISSED, 'missed'),
    )
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment = models.CharField(
        max_length=2,
        choices=PAYMENT_CHOICES,
        default=MADE,
    )
    date = models.DateTimeField(auto_now=False, null=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    def __str__(self):
        return f'{self.id}'
