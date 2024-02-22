from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class task (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True , blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '- by ' + self.user.username

class Categorias(models.Model):
    nombre_categoria = models.CharField(max_length=50)
    descripcion_categoria = models.TextField(blank=True)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_categoria 


class Productos (models.Model):
    codigo_productos = models.CharField(max_length=10, unique=True)
    nombre_productos = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    cantidad = models.PositiveIntegerField(null=True)
    descripcion = models.TextField(max_length=50)
    categoria = models.ForeignKey(Categorias,on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo_productos + '- by ' + self.nombre_productos
   

class Clientes(models.Model):
    Id_cedula = models.CharField(max_length=20,unique=True)
    nombres = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.Id_cedula + '- by ' + self.nombres
    


class Itemcarrito (models.Model):
    nombre_productos = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    
    def subtotal(self):
        return self.producto.precio * self.nombre_productos


class Ventas(models.Model):
    valor_neto = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=0)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    Id_cedula = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.Id_cedula) + '- by ' + str(self.valor_total)
    


class Stock(models.Model):
    cantidad_disponible = models.IntegerField()
    cantidad_nueva = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id_producto) + '- by ' + str(self.cantidad_disponible)
    

class Carrito(models.Model):
    nomproducto = models.IntegerField(max_length=100)
    precio = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=100)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)