from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'Customer'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.email})"
