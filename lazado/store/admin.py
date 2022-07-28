from django.contrib import admin
from .models import Items,LookupItemType,Review, Address, Customer, Order

# Register your models here.
admin.site.register(Items)
admin.site.register(LookupItemType)
admin.site.register(Review)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Order)