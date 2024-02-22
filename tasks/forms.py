from django.forms import ModelForm
from django import forms
from .models import task,Productos,Itemcarrito,Clientes,Carrito

class taskform(ModelForm):
    class Meta:
        model = task
        fields = ['title', 'description', 'important']
        

class carriform(ModelForm):
    class Meta:
        model = Itemcarrito
        fields = ['nombre_productos', 'categoria', 'descripcion','precio']        


class producform(ModelForm):
    class Meta:
        model = Productos
        fields = ['codigo_productos', 'nombre_productos', 'precio', 'fecha_ingreso', 'cantidad', 'descripcion', 'categoria']

class ClienteForm(ModelForm):
    class Meta:
        model = Clientes
        fields = ['Id_cedula', 'nombres', 'email', 'direccion', 'telefono']

class carritoform(ModelForm):
    class Meta:
        model = Carrito
        fields = ['nomproducto', 'precio', 'cantidad']

class AgregarAlCarritoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1)

