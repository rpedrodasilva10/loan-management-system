"""
Models for loan_app application.
"""

import secrets
import string
import decimal
from django.utils import timezone
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from clients.models import Client

class Base(models.Model):
    """
    Abstract base class.
    Stores the dates for creation and last update, and the object's status.
    """
    active = models.BooleanField("Active", default=True)
    updated = models.DateTimeField("Updated", auto_now=True)
    created = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-updated', '-created']

class Loan(Base):
    """
    Abstracts a loan made to a :model:`clients.Client`.
    """
    finished = models.BooleanField("Paid", default=False)
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
        help_text="unique id of a client. ",
        null=False,

    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=False,
        help_text="loan amount in dollars."
    )
    term = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        null=False,
        help_text="number of months that will take until the loan gets paid-off."
    )
    rate = models.DecimalField(
        max_digits=4,
        decimal_places=4,
        null=False,
        help_text="interest rate as decimal."
    )
    date = models.DateTimeField(
        null=False,
        help_text="when the loan was requested (origination date as an ISO 8601 string)."
    )
    instalment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=False,
        blank=True,
        help_text="monthly loan payment.",
    )
    _outstanding = models.DecimalField(
        "outstanding",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=False
    )
    _total_value = models.DecimalField(
        "total value",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=False
    )

    @property
    def outstanding(self):
        """
        Gets the outstanding debt.
        """
        return self._outstanding

    @outstanding.setter
    def outstanding(self, value):
        """
        Sets the outstanding debt.
        """
        if value < 0:
            raise ValueError("Can't set a negative outstanding debt.")
        self._outstanding = value
        if self._outstanding == 0:
            self.finished = True

    def get_balance(self, date):
        """
        Gets the outstanding balance.
        """
        amount_paid = Payment.get_paid_amount(self.loan_id, date)
        return self._total_value - amount_paid

    def __str__(self):
        return f'{self.loan_id}'

    def save(self, *args, **kwargs):# pylint: disable=arguments-differ
        if not self.loan_id:
            self.enforce_business_rules()
            # calculate instalment
            _r = decimal.Decimal(self.rate) / decimal.Decimal(self.term)
            instalment = (_r + _r / ((1 + _r) ** self.term - 1)) * self.amount
            self.instalment = instalment.quantize(
                decimal.Decimal("0.01"),
                decimal.ROUND_DOWN
            )

            # inicialize outstanding
            outstanding = self.instalment * self.term
            self.outstanding = outstanding
            self._total_value = outstanding.quantize(
                decimal.Decimal("0.01"),
                decimal.ROUND_DOWN
            )

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
        else:
            super(Loan, self).save(*args, **kwargs)

    def enforce_business_rules(self):
        """
        Enforces the following business rules:

        1) If a client contracted a loan in the past and paid all without
        missing any payment, you can decrease by 0.02% his tax rate.

        2) If a client contracted a loan in the past and paid all but missed
        until 3 monthly payments, you can increase by 0.04% his tax rate.

        3) If a client contracted a loan in the past and paid all but missed
        more than 3 monthly payments or didn’t pay all the loan, you need to
        deny the new one.
        """
        if not self.client_id.loans.all():
            # client doesn't have loans in the past
            return
        raise_rate = False
        for loan_obj in self.client_id.loans.all():
            if loan_obj.finished:
                missed_payments = 0
                for payment_obj in loan_obj.payments.all():
                    if payment_obj.payment == 'missed':
                        missed_payments += 1
                if missed_payments > 3:
                    raise ValidationError({
                        'loan_id':['Loan denied. Client missed too many payments.']
                    })
                if missed_payments > 0:
                    raise_rate = True
            else:
                raise ValidationError(
                    {'loan_id': ['Client already have an active Loan.']}
                )
        if raise_rate:
            self.rate = float(self.rate) + 0.04
        else:
            self.rate = max(0.0, float(self.rate) - 0.02)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'


class Payment(Base):
    """
    Payment made referencing a :model:`loan_app.Loan`
    and a :model:`clients.Client` in the system.
    """
    payment_id = models.AutoField(primary_key=True)
    MADE = 'made'
    MISSED = 'missed'
    PAYMENT_CHOICES = (
        (MADE, 'made'),
        (MISSED, 'missed'),
    )
    loan_id = models.ForeignKey(
        Loan,
        related_name='payments',
        on_delete=models.CASCADE,
        help_text="unique id of the loan.",
    )
    payment = models.CharField(
        max_length=6,
        choices=PAYMENT_CHOICES,
        default=MADE,
        help_text = "type of payment: made or missed.",
        null=False
    )
    date = models.DateTimeField(
        auto_now=False,
        null=False,
        help_text="payment date."
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=False,
        help_text="amount of the payment made or missed in dollars."
    )

    def __str__(self):
        return f'{self.payment_id}'

    def save(self, *args, **kwargs):# pylint: disable=arguments-differ
        self.enforce_business_rules()
        if self.payment == self.MADE:
            self.loan_id.outstanding -= self.amount
            self.loan_id.save()
        super(Payment, self).save(*args, **kwargs)

    def enforce_business_rules(self):
        """
        Enforces the following business rules:

        1) there must be only one payment per month (made or missed);
        2) the payment amount must be exactly the instalment value;
        3) ensure future payments are not allowed.
        """
        if self.loan_id.payments.filter(
                date__month=self.date.month,
                date__year=self.date.year
            ).count():
            raise ValidationError(
                {'date': 'Payment already registered for this month.'}
            )
        if self.date > timezone.now():
            raise ValidationError(
                {'date': 'Cannot performe future payments.'}
            )
        if self.amount != self.loan_id.instalment:
            raise ValidationError(
                {'amount': f'your instalment amount is {self.loan_id.instalment}!'}
            )

    @staticmethod
    def get_paid_amount(loan_id, date):
        """
        Gets the total amount paid for a specific loan until a specific date.
        """
        payments = Payment.objects.filter(
            loan_id__loan_id=loan_id
        ).filter(
            payment=Payment.MADE
        ).filter(
            date__lte=date
        )
        total_paid = decimal.Decimal(sum([p.amount for p in payments]))
        return total_paid.quantize(
            decimal.Decimal('0.01'),
            decimal.ROUND_DOWN
        )

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
