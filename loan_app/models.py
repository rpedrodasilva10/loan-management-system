"""Missing: DOCSTRING"""

import secrets
import string
import decimal
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ValidationError

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
    Loans class abstracts a loan made to a client
    """
    finished = models.BooleanField("Pago: ", default=False)

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

    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    term = models.DecimalField(max_digits=3, decimal_places=0, null=False)
    rate = models.DecimalField(max_digits=4, decimal_places=4, null=False)
    date = models.DateTimeField(null=False)
    instalment = models.DecimalField(
        "Valor da parcela: ",
        max_digits=12,
        decimal_places=2,
        null=False
    )

    _outstanding = models.DecimalField(
        "Valor em aberto: ",
        max_digits=12,
        decimal_places=2,
        null=False
    )

    @property
    def outstanding(self):
        """
        Gets the outstanding debt
        """
        return self._outstanding

    @outstanding.setter
    def outstanding(self, value):
        """
        Sets the outstanding debt
        """
        if value < 0:
            raise ValueError("Can't set a negative Outstanding debt")
        self._outstanding = value

        if self._outstanding == 0:
            self.finished = True

    def __str__(self):
        return f'{self.loan_id}'


    def __init__(self, *args, **kwargs):

        super(Loan, self).__init__(*args, **kwargs)

        # calculate instalment
        _r = self.rate / self.term
        instalment = (_r + _r / ((1 + _r) ** self.term - 1)) * self.amount
        self.instalment = instalment.quantize(
            decimal.Decimal("0.01"),
            decimal.ROUND_DOWN
        )

        # inicialize outstanding
        outstanding = self.instalment * self.term
        self.outstanding = outstanding

    def save(self, *args, **kwargs):# pylint: disable=arguments-differ

        if not self.loan_id:
            self.enforce_business_rules()

            # Creating loan_id here instead of put it in a function because
            # it uses super().save method to check db integrity.
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
        if not self.client_id.loans.all():
            # client doesn't have loans in the past
            return

        missed_payments = 0
        for loan_obj in self.client_id.loans.all():
            if loan_obj.finished:
                for payment_obj in loan_obj.payments.all():
                    if payment_obj.payment == 'missed':
                        missed_payments += 1
            else:
                raise ValidationError(
                    {'loan_id': ['Client already have an active Loan.']}
                )

        if missed_payments == 0:
            self.rate = max(0.0, float(self.rate) - 0.02)
        elif missed_payments < 4:
            self.rate = float(self.rate) + 0.04
        else:
            raise ValidationError(
                {'loan_id': ['Loan denied. Client missed too many payments.']}
            )

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'


class Payment(Base):
    """
    Payment class abstracts a payment made referencing
    a loan and a client in the system
    """
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

    def save(self, *args, **kwargs):# pylint: disable=arguments-differ

        if self.payment == self.MADE:
            # We need to work with the actual loan object
            # because de FK object doesn't have the method save
            # used to updated the outstanding value
            loan = Loan.objects.get(pk=self.loan_id)

            # Not sure if we need to check here, validate could
            # take care of it
            if  loan.outstanding == 0:
                raise ValueError("Can't make a payment to a loan fully paid")

            # Loan.outstanding will check if it is a negative value, no need to check here.
            loan.outstanding -= self.amount
            loan.save()

        super(Payment, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
