from django.db import models

# Create your models here.
class MyPet(models.Model):
    name = models.CharField(max_length=20)
    image_url = models.URLField()

    def __str__(self):
        return self.name
