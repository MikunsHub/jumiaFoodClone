from django.contrib import admin
from .models import *

admin.site.register([
    Country,
    Business_Type,
    Order,
    OrderItems,
    Menu,
    Driver,
    Customer,
    Delivery,
    Delivery_accept,
    Vendor,
    Delivery_location,
    Delivery_driver_match
])
