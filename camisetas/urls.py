from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path("", views.chakeclub, name="chakeclub"),
    path('clientes/', views.get_clientes, name='get_clientes'),
    path('confecciones/<int:cliente_id>', views.get_confecciones, name='get_confecciones'),
    path('detalles/<int:confecciones_id>', views.get_detalles, name='get_detalles'),
    path('registrarCliente/', views.registrarCliente, name='registrarCliente'),
    path('nuevoCliente/', views.nuevoCliente, name='nuevoCliente'),
    path('registrarConfeccion/', views.registrarConfeccion, name='registrarConfeccion'),
    path('nuevaConfeccion/<int:cliente_id>/', views.nuevaConfeccion, name='nuevaConfeccion'),
    path('registrarDetalle/', views.registrarDetalle, name='registrarDetalle'),
    path('nuevoDetalle/<int:confecciones_id>/', views.nuevoDetalle, name='nuevoDetalle'),
    path('edicionDetalle/<int:detalles_id>/', views.edicionDetalle, name='edicionDetalle'),
    path('test/', lambda request: HttpResponse('Funciona')),
    path('items/agregar/', views.ItemsCreateView.as_view(), name='items_agregar'),
    path('items/editar/<int:pk>/', views.ItemsUpdateView.as_view(), name='teims_editar'),
    path('items/ver/<int:pk>/', views.ItemsDetailView.as_view(), name='items_ver'),
]

