from django.contrib import admin

from .models import Customer
@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['name', 'type_person', 'address']
    fields = ['name', 'type_person', 'address']


