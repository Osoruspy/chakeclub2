from django.contrib import admin
from .models import Clientes, Confecciones, Confecciones_detalles, Items, Adicional, Pagos, Pagos_detalles, Auditoria, Tamano
# Register your models here.

admin.site.register(Clientes)
admin.site.register(Confecciones)
admin.site.register(Confecciones_detalles)
admin.site.register(Items)
admin.site.register(Adicional)
admin.site.register(Pagos)
admin.site.register(Pagos_detalles)
admin.site.register(Tamano)
