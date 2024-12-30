from django.db import models

class Root(models.Model):
    name = models.CharField(max_length=255)
    d3_points = models.JSONField()  # Stores the D3 points as JSON

    def __str__(self):
        return self.name

class DentalStructure(models.Model):
    name = models.CharField(max_length=255)
    tooth_type = models.CharField(max_length=50)
    quadrant = models.CharField(max_length=50)
    num_roots = models.PositiveIntegerField()
    d3_points = models.JSONField()  # Stores the outline points as JSON
    roots = models.ManyToManyField(Root)

    def __str__(self):
        return self.name
