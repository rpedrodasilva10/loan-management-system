"""Missing: DOCSTRING"""

import secrets
import string
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from clients.models import Client


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

    client_id = models.ForeignKey(
        Client,
        related_name='loans',
        on_delete=models.PROTECT,
        default=None,
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
        r = float(self.rate) / self.term # pylint: disable=invalid-name
        return (r + r / ((1 + r) ** float(self.term) - 1)) * float(self.amount)

    def __str__(self):
        return f'{self.loan_id}'

    def save(self, *args, **kwargs):# pylint: disable=arguments-differ
        self.enforce_business_rules()

        # Creating loan_id here instead of put it in a function because
        # it uses super().save method to check db integrity.
        if not self.loan_id:
            token = ''.join(secrets.choice(string.digits) for _ in range(15))
            mask = '{}{}{}-{}{}{}{}-{}{}{}{}-{}{}{}{}'
            self.loan_id = mask.format(*token)
        success = False
        while not success:
            try:
                super(Loan, self).save(*args, **kwargs)
            except IntegrityError:
                token = ''.join(secrets.choice(string.digits) for _ in range(15))
                mask = '{}{}{}-{}{}{}{}-{}{}{}{}-{}{}{}{}'
                self.loan_id = mask.format(*token)
            else:
                success = True

    def enforce_business_rules(self):
        '''
        Enforces the following business rules:

        1) If a client contracted a loan in the past and paid all without
        missing any payment, you can decrease by 0.02% his tax rate.

        2) If a client contracted a loan in the past and paid all but missed
        until 3 monthly payments, you can increase by 0.04% his tax rate.

        3) If a client contracted a loan in the past and paid all but missed
        more than 3 monthly payments or didn’t pay all the loan, you need to
        deny the new one.
        '''
        missed_payments = 0
        for loan_obj in self.client_id.loans.all():
            if not loan_obj.active:
                for payment_obj in loan_obj.payments.all():
                    if payment_obj.payment == 'missed':
                        missed_payments += 1
            else:
                raise ValidationError(
                    {'loan_id': ['Client already have an active Loan.']}
                )

        if missed_payments == 0:
            self.rate = max(0.0, self.rate - 0.02)
        elif missed_payments < 4:
            self.rate = self.rate + 0.04
        else:
            raise ValidationError(
                {'loan_id': ['Loan denied. Client missed too many payments.']}
            )


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
        Loan,
        related_name='payments',
        editable=False,
        on_delete=models.CASCADE
    )
    payment = models.CharField(
        max_length=2,
        choices=PAYMENT_CHOICES,
        default=MADE,
    )
    date = models.DateTimeField(auto_now=False, null=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    def __str__(self):
        return f'{self.payment_id}'
