"""Missing: DOCSTRING"""

import secrets
import string
from django.db import models
from django.db import IntegrityError


class Loan(models.Model):
    """
    Stores the loans entries.
    """
    loan_id = models.CharField(
        primary_key=True,
        max_length=18,
        editable=False,
        unique=True,
        blank=True,
    )
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
        return f'{self.loan_id}'

    def save(self, *args, **kwargs):# pylint: disable=arguments-differ
        if not self.loan_id:
            token = ''.join(secrets.choice(string.digits) for _ in range(15))
            mask = '{}{}{}-{}{}{}{}-{}{}{}{}-{}{}{}{}'
            self.loan_id = mask.format(*token)
        success = False
        failures = 0
        while not success:
            try:
                super(Loan, self).save(*args, **kwargs)
            except IntegrityError:
                failures += 1
                if failures > 5:
                    raise
                token = ''.join(secrets.choice(string.digits) for _ in range(15))
                mask = '{}{}{}-{}{}{}{}-{}{}{}{}-{}{}{}{}'
                self.loan_id = mask.format(*token)
            else:
                success = True


class Payment(models.Model):
    """Missing: DOCSTRING"""
    MADE = 'made'
    MISSED = 'missed'
    PAYMENT_CHOICES = (
        (MADE, 'made'),
        (MISSED, 'missed'),
    )
    payment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(
        Loan, related_name='payments', editable=False, on_delete=models.CASCADE
    )
    payment = models.CharField(
        max_length=2,
        choices=PAYMENT_CHOICES,
        default=MADE,
    )
    date = models.DateTimeField(auto_now=False, null=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    def __str__(self):
        return f'{self.id}'
