"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home ,name='home'),
    path('signup/', views.signup,name='signup' ),
    path('tasks/', views.tasks,name='tasks' ),
    path('tasks_completed/', views.tasks_completed,name='tasks_completed' ),
    path('task/create/', views.create_task,name='create_task' ),
    path('task/<int:task_id>/', views.task_detail,name='task_detail' ),
    path('task/<int:task_id>/complete/', views.complete_task,name='complete_task' ),
    path('task/<int:task_id>/delete/', views.delete_task,name='delete_task' ),
    path('logout/', views.desconectar,name='logout' ),
    path('iniciarSesion/', views.iniciarSesion,name='iniciarSesion' ),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complet.html"), name='password_reset_complete'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('productoB/<int:producto_id>/', views.borrar_produc,name='borrar_produc' ),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_carrito/', views.agregar_al_carrito, name='agregar_carrito'),
]
