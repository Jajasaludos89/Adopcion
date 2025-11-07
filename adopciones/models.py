from django.db import models
from django.core.validators import MinValueValidator

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    def __str__(self): return f"{self.nombre} {self.apellido}"

from django.db import models

class ONG(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    pais = models.CharField(max_length=100, verbose_name="País", null=False, blank=False)
    telefono = models.CharField(max_length=100, verbose_name="Teléfono", null=False, blank=False)
    correo = models.EmailField(max_length=100, verbose_name="Correo", null=False, blank=False)
    representante = models.CharField(max_length=100, verbose_name="Representante", null=False, blank=False)
    sitio_web = models.URLField(max_length=100, verbose_name="Sitio web", null=True, blank=True)
    descripcion = models.TextField(verbose_name="Descripción", null=False, blank=False)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    descripcion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    adoptada = models.BooleanField(default=False)
    ong=models.ForeignKey(ONG, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return f"{self.nombre} ({self.especie})"

class Adopcion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha_adopcion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    def __str__(self): return f"{self.persona} - {self.mascota} - {self.fecha_adopcion}"
