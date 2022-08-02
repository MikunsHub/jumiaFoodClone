from django.contrib import admin
from .models import *

admin.site.register([
    Country,
    Business_Type,
    Order,
    OrderItems,
    Payment,
    Menu,
    Driver,
    Customer,
    Delivery,
    Vendor,
    Delivery_location,
    Delivery_driver_match
])
