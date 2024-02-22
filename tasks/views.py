import re
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import task,Productos,Itemcarrito,Clientes,Carrito
from .forms import taskform,producform,ClienteForm,AgregarAlCarritoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from email.message import EmailMessage
import os
import smtplib
import ssl


# Create your views here.
def home(request):
    return render(request, 'home.html')


def is_valid_password(password):
    # La contraseña debe tener al menos 8 caracteres
    # Debe contener al menos una letra mayúscula, una letra minúscula y un carácter especial
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    return bool(regex.match(password))

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 and is_valid_password(password1):
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=password1)
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'El usuario ya existe'})

        return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'La longitud de la contraseña es inválida o las contraseñas no coinciden o no cumplen con los requisitos'})

def email():
    
    load_dotenv()
    email_sender = "tiquejulian727@gmail.com"
    password =  os.getenv("PASSWORD")
    email_reciver = "tiquej432@gmail.com"

    subject = "recuperar contraseña"
    body = f""" Alguien ingreso a tu cuenta...  {email_reciver}"""

    em = EmailMessage()
    em ["From"] = email_sender
    em ["To"] = email_reciver
    em ["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context() 

    with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context  ) as smtp:
        smtp.login(email_sender,password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())  
    return

def recuperar(request):
    if request.method=='GET':
    
        return render(request,'recuperar.html')
    else:
         
        usuario=User.objects.get(email=request.POST['correo']) 
        print(usuario.password) 
        email()
        return render(request,'recuperar.html',{
            'user':usuario.email
        })

@login_required
def tasks(request):
    tasks = task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})



@login_required
def tasks_completed(request):
    tasks = task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})





@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": taskform})
    else:
        try:
            form = taskform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": taskform, "error": "Error creating task."})





@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        Task = get_object_or_404(task, pk=task_id, user=request.user)
        Form = taskform(instance=Task)
        return render(request, 'task_detail.html', {"task": Task, "form": Form})
    else:
        try:
            Task = get_object_or_404(task, pk=task_id, user=request.user)
            form = taskform(request.POST, instance=Task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': Task, 'form': form, 'error': 'Error actualizando task.'})
    
    
    
  
  
  
@login_required  
def complete_task(request, task_id):
    Task = get_object_or_404(task, pk=task_id, user=request.user)
    if request.method == 'POST':
        Task.datecompleted = timezone.now()
        Task.save()
        return redirect('tasks')





@login_required
def delete_task(request, task_id):
    Task = get_object_or_404(task, pk=task_id, user=request.user)
    if request.method == 'POST':
        Task.delete()
        return redirect('tasks')    
    
    
  
    
    
@login_required
def desconectar(request):
    logout(request)
    return redirect('home')


def iniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarSesion.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciarSesion.html', {'form': AuthenticationForm, 'error': 'el usuario o la contraseña  es incorrecto'})
        else:
            login(request, user)
            email()
            return redirect(tasks)
        

@login_required
def lista_productos(request):
    productos = Productos.objects.all()

    query = request.POST.get('q')
    if query:
        productos = productos.filter(nombre_productos__icontains=query)

    return render(request, 'lista_productos.html', {'productos': productos})


def detalle_producto(request, producto_id):
    producto = Productos.objects.get(pk=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

@login_required
def agregar_producto(request):
    if request.method == 'GET':
        return render(request, 'agregar_producto.html', {'form': producform})
    else:
        try:
            form = producform(request.POST)
            new_produc = form.save(commit=False)
            new_produc.save()
            return redirect('lista_productos')
        except ValueError:
            return render(request, 'agregar_producto.html', {"form": producform, "error": "Error creating producto."})

def editar_producto(request, producto_id):
    if request.method == 'GET':
        producto = get_object_or_404(Productos, pk=producto_id)
        Form = producform(instance=producto)
        return render(request, 'editar_producto.html', {'producto': producto, 'form': Form})
    else:
        try:
            producto = get_object_or_404(Productos,pk=producto_id)
            form = producform(request.POST, instance=producto)
            form.save()
            return redirect('lista_productos')
        except ValueError:
            return render(request, 'editar_producto.html', {'producto': producto, 'form': form, 'error': 'Error actualizando task.'})    
    


# views.py
def ver_carrito(request):
    items = Itemcarrito.objects.all()
    total = sum(item.subtotal() for item in items)
    return render(request, 'ver_carrito.html', {'items': items, 'total': total})


def borrar_produc(request, producto_id):
    productos = get_object_or_404(Productos, pk=producto_id)
    productos.delete()
    return redirect('lista_productos') 

def lista_clientes(request):
    clientes = Clientes.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'agregar_cliente.html', {'form': form})

def carrito(request):
    if request.method=='GET':
        productos = Productos.objects.all()
        return render(request,'carrito.html',{'productos':productos})
    else:
        productos = Productos.objects.filter(nombre_productos__icontains=request.POST['nombre'])
        return render(request,'carrito.html',{'productos':productos})

@login_required        
def agregar_al_carrito(request):
    if request.method == 'POST':
        form = AgregarAlCarritoForm(request.POST)
        if form.is_valid():
            producto_id = request.POST['producto_id']
            cantidad = request.POST['cantidad']
    
            producto = Productos.objects.get(pk=producto_id)
            Carrito.objects.create(id_producto=producto,nomproducto=1,precio=2500,cantidad=cantidad)
            return redirect('carrito')
    else:
        productos = Productos.objects.all()
        form = AgregarAlCarritoForm()
    return render(request, 'carrito.html', {'form': form,'productos':productos})



