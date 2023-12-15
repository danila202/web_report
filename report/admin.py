from django.contrib import admin

from .models import Customer, Protocol
@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['name', 'type_person', 'address']
    fields = ['name', 'type_person', 'address']


@admin.register(Protocol)
class AdminProtocol(admin.ModelAdmin):
    list_display = ['data', 'performer', 'kind', 'name_file']


