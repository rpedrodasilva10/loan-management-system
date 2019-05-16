from django.db import models
from pycpfcnpj import cpfcnpj
class Base(models.Model):
    """
    Has the standard base for other classes (fields, methods etc)
    """
    active = models.BooleanField("Ativo: ", default=True)
    updated = models.DateTimeField("Atualizado em: ", auto_now=True)
    created = models.DateTimeField("Criado em: ", auto_now_add=True)

    class Meta:
        abstract = True

class Client(Base):
    """
    Client class abstracts a client in the system
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
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
