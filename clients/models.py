"""
Models for clients application.
"""

from django.db import models

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


class Client(Base):
    """
    Abstracts a client in the system.
    """
    client_id = models.AutoField(primary_key=True, help_text="unique id of a client.")
    name = models.CharField(max_length=100, help_text="the client name.")
    surname = models.CharField(max_length=100, help_text="the client surname.")
    email = models.EmailField(help_text="the client email.")
    telephone = models.CharField(max_length=11, help_text="the client telephone.")
    cpf = models.CharField("CPF", max_length=11, unique=True, help_text="the client identification.")

    def __str__(self):
        return f'{self.client_id} - {self.name} {self.surname}'


    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
