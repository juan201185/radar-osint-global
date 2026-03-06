from django.db import models

class Foto(models.Model):
    imagen = models.ImageField(upload_to='fotos/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto {self.id}"