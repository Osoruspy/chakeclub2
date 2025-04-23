from django.db import models
from .choises import estado, adicional, genero
from django.core.validators import MinValueValidator, MaxValueValidator
from .choises import estado, genero, prendas

# Create your models here.

class Clientes(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre Cliente')
    fecha = models.DateField(auto_now=False, auto_now_add=True)
    estado = models.CharField(max_length=1, choices=estado, default='A')
    contacto = models.CharField(max_length=20, verbose_name='Contacto')
    tel_contacto = models.CharField(
        max_length=50, verbose_name="Tel. Contacto")
    obs = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'clientes'

class Confecciones(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=False, auto_now_add=True)
    estado = models.CharField(max_length=1, choices=estado, default='A')
    obs = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return "{}".format(self.cliente.nombre)

    class Meta:
        db_table = 'confecciones'

class Items(models.Model):
    nombre = models.CharField(max_length=20)
    estado = models.CharField(max_length=1, choices=estado, default='A')
    obs = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'items'

class Tamano(models.Model):
    nombre = models.CharField(max_length=20)
    abreviado = models.CharField(max_length=10)
    estado = models.CharField(max_length=1, choices=estado, default='A')
    obs = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return "{} {}".format(self.nombre, self.abreviado)

    class Meta:
        db_table = 'tamano'

class Confecciones_detalles(models.Model):
    confecciones = models.ForeignKey(Confecciones, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, verbose_name=(
        "Item"), on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    tamano = models.ForeignKey(Tamano, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1, choices=genero, default='H')
    item_adicional = models.CharField(max_length=1, default="S")
    numero = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)])
    fecha = models.DateField(auto_now=False, auto_now_add=True)
    estado = models.CharField(max_length=1, choices=estado, default='A')
    obs = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'confecciones_detalles'

class Adicional(models.Model):
    confecciones_detalles = models.ForeignKey(
        Confecciones_detalles, on_delete=models.CASCADE)
    prenda = models.CharField(max_length=1, choices=prendas, default='S')
    estado = models.CharField(max_length=1, choices=estado, default='A')
    obs = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'adicional'

class Pagos(models.Model):
    confecciones = models.ForeignKey(Confecciones, on_delete=models.CASCADE)
    monto = models.IntegerField()
    fecha = models.DateField(auto_now=False, auto_now_add=True)
    estado = models.CharField(max_length=1, choices=estado, default='A')
    obs = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'pagos'


class Pagos_detalles(models.Model):
    pagos = models.ForeignKey(Pagos, on_delete=models.CASCADE)
    monto = models.IntegerField()
    fecha = models.DateField(auto_now=False, auto_now_add=True)
    estado = models.CharField(max_length=1, choices=estado, default='A')
    obs = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'pagos_detalles'


class Auditoria(models.Model):
    tabla = models.CharField(max_length=20)
    datos_anterior = models.CharField(max_length=100)
    datos_cambio = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    obs = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'audtoria'
