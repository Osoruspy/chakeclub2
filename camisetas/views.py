from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Clientes, Confecciones, Confecciones_detalles, Items, Adicional, Pagos, Pagos_detalles, Auditoria, Tamano
from .forms import ItemForm
from .choises import *
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy


# Create your views here.

def index(request):
    return render(request, 'index.html')

def chakeclub(request):
    data = {
    'titulo': 'Chake Club',
    }

    return render(request, "chakeclub.html", data)

def get_clientes(request):
    # clientes = list(Clientes.objects.values())
    clientes = list(Clientes.objects.filter(estado='A'))

    if len(clientes) > 0:
        # data = {'message': "Success", 'clientes': clientes}
        data = {'message': "Success",
                'clientes': [
                    {
                        "id": c.id,
                        "nombre": c.nombre,
                        "contacto": c.contacto,
                        "tel_contacto": c.tel_contacto,
                        "obs": c.obs,
                    }
                    for c in clientes
                ]
                }
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

def get_confecciones(request, cliente_id):
    # confecciones = list(Confecciones.objects.filter(cliente_id=cliente_id).values())
    confecciones = list(Confecciones.objects.filter(cliente_id=cliente_id))
    if len(confecciones) > 0:
        # data = {'message': "Success", 'confecciones': confecciones}
        data = {'message': "Success",
                'confecciones': [
                    {
                        "id": c.id,
                        "estado": c.estado,
                        "obs": c.obs,
                        "cliente_id": c.cliente_id,
                        "contacto": c.cliente.contacto,
                        "telcontacto": c.cliente.tel_contacto,
                        "cliestado": c.cliente.estado,
                        "cliobs": c.cliente.obs
                    }
                    for c in confecciones
                ]
                }
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

def get_detalles(request, confecciones_id):
    # detalles = list(Confecciones_detalles.objects.filter(confecciones_id=confecciones_id).values())
    detalles = list(Confecciones_detalles.objects.filter(
        confecciones_id=confecciones_id))

    if len(detalles) > 0:
        # data = {'message': "Success", 'detalles': detalles }
        data = {
            "message": "Success",
            "detalles": [
                {
                    "id": d.id,
                    "item": d.item.nombre,
                    "nombre": d.nombre,
                    "tamano": d.tamano.nombre,
                    "genero": d.genero,
                    "item_adicional": d.item_adicional,
                    "numero": d.numero,
                    "obs": d.obs,
                }
                for d in detalles
            ]
        }
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

def nuevoCliente(request):
    data = {
        'titulo': 'Nuevo Cliente',
    }

    return render(request, "nuevoCliente.html", data)

def registrarCliente(request):
    nombre = request.POST['txtNombre']
    contacto = request.POST['txtContacto']
    telcontacto = request.POST['txtTelContacto']
    obs = request.POST['txtObs']

    cliente = Clientes.objects.create(nombre=nombre,
                                      contacto=contacto,
                                      tel_contacto=telcontacto,
                                      obs=obs)
    
    cliente_id = cliente.id
    confecciones = Confecciones.objects.create(cliente_id=cliente_id)
    
    return redirect("chakeclub")

def nuevaConfeccion(request, cliente_id):
    data = {
        'titulo': 'Nueva Confeccion',
        'cliente_id': cliente_id,
    }

    return render(request, "nuevaConfeccion.html", data)

def registrarConfeccion(request):
    cliente_id = request.POST['id']
    obs = request.POST['obs']

    confecciones = Confecciones.objects.create(cliente_id=cliente_id,
                                               obs=obs)

    return redirect("chakeclub")

def nuevoDetalle(request, confecciones_id):
    items = Items.objects.all().values('id', 'nombre')  # Traer solo lo necesario
    tamanos = Tamano.objects.all().values('id', 'nombre')  # Traer solo lo necesario
    
    data ={
        'titulo': 'Nuevo Detalle',
        'confecciones_id': confecciones_id,
        'items': items,
        'tamanos': tamanos,
        'genero': genero,
        'adicional': adicional,
    }
    
    return render(request, "nuevoDetalle.html", data)

def registrarDetalle(request):
    if request.method == 'POST':
        try:
            # Obtener IDs y convertir a objetos relacionados (FKs)
            confecciones_id = int(request.POST.get('confecciones_id'))
            confeccion = get_object_or_404(Confecciones, pk=confecciones_id)

            item_id = int(request.POST.get('item_id'))
            item = get_object_or_404(Items, pk=item_id)

            tamano_id = int(request.POST.get('tamano_id'))
            tamano = get_object_or_404(Tamano, pk=tamano_id)

            # Obtener campos simples
            nombre = request.POST.get('txtNombre')
            genero = request.POST.get('genero_id')  # 'H', 'M', 'N'
            item_adicional = request.POST.get('item_Adicional_id')  # 'S' o 'N'
            numero = request.POST.get('numNumero')
            obs = request.POST.get('txtObs', '')

            # Crear objeto en base de datos
            Confecciones_detalles.objects.create(
                confecciones=confeccion,
                item=item,
                nombre=nombre,
                tamano=tamano,
                genero=genero,
                item_adicional=item_adicional,
                numero=int(numero) if numero else 0,
                obs=obs
            )
            messages.success(request, "✅ Registro guardado correctamente.")
            # ✅ Detectar qué botón se presionó
            if request.POST.get('action') == 'guardar_nuevo':
                # Volver al mismo formulario vacío (mismo confecciones_id)
                return redirect('nuevoDetalle', confecciones_id=confecciones_id)
            else:
                # Ir a otra página (lista, detalle, etc.)
                return redirect('chakeclub')  # o la que uses

        except (ValueError, Items.DoesNotExist, Tamano.DoesNotExist, Confecciones.DoesNotExist) as e:
            # Mostrar errores si algo no se pudo procesar
            return render(request, 'error.html', {'error': str(e)})

class ItemsCreateView(CreateView):
    model = Items
    form_class = ItemForm
    template_name = 'items_form.html'
    success_url = reverse_lazy('nuevoDetalle')

class ItemsUpdateView(UpdateView):
    model = Items
    form_class = ItemForm
    template_name = 'items_form.html'
    success_url = reverse_lazy('nuevoDetalle')

class RegistroDetailView(DetailView):
    model = Items
    template_name = 'items_detail.html'

