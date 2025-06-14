from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)

    def __str__(self):
        return f"product_name - {self.name} | code - {self.code}"


class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()


class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.FloatField()
