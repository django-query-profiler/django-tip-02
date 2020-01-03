from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    subcategories = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=120)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Change for newer version of Django

    def __str__(self):
        return self.title
