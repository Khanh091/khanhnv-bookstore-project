from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Plaintext theo script DB

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name