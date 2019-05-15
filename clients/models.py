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
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=11)
    cpf = models.CharField("CPF", max_length=11, unique=True)

    def __str__(self):
        return f'{self.client_id} - {self.name} {self.surname}'

    def get_client(self):
        """
        Returns the client's information as a string.
        """
        return self.name + ' ' + self.surname \
            + ' e-mail ' + self.email \
            + ' telephone ' + self.telephone \
            + ' CPF ' + self.cpf

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
