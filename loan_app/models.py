"""Missing: DOCSTRING"""

import secrets
import string
from django.db import models
from django.db import IntegrityError

from clients.models import Client

class Base(models.Model):
    """
    Has the standard base for other classes (fields, methods etc)
    """
    active = models.BooleanField("Ativo: ", default=True)
    updated = models.DateTimeField("Atualizado em: ", auto_now=True)
    created = models.DateTimeField("Criado em: ", auto_now_add=True)

    class Meta:
        abstract = True

class Loan(Base):
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


class Payment(Base):
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
