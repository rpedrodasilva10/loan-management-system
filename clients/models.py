from django.db import models

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
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=11)
    cpf = models.CharField("CPF", max_length=11, unique=True)

    def __str__(self):
        return f'{self.client_id} - {self.name} {self.surname}'

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
