from django.db import models

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = 'Book'
        ordering = ['id']

    def __str__(self):
        return f"{self.title} by {self.author}"
