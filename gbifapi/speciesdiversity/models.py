from django.db import models

# Almacenamos aquí los países a elegir
class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Graphs(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    data_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Diversidad y riqueza en {self.country}"
