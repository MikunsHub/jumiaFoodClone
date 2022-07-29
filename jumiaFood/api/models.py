from django.db import models

from django.db import models
from user.models import User

status_choices = (
    ("pending", "pending"),
    ("in_transit", "in_transit"),
    ("delivered", "delivered")
)


# country and business_type can be simple choices
class Country(models.Model):
    country_name = models.CharField(max_length=80)

    def __str__(self):
        return f"<Country: {self.country_name}"


class Business_Type(models.Model):
    type = models.CharField(max_length=25)

    def __str__(self):
        return f"<Business_Type: {self.type}"


class Vendor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    owner_name = models.CharField(max_length=100)
    no_of_establishments = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    business_type = models.ForeignKey(Business_Type, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    # tin_doc = models.FileField()
    # incorporation_cert_doc = models.FileField()
    # owner_id = models.FileField()

    def __str__(self):
        return f"<Name: {self.owner_name} id:{self.pk}>"


class Menu(models.Model):
    meal_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.meal_name}"


class Order(models.Model):
    status = models.CharField(
        max_length=30, choices=status_choices, default=status_choices[0][0])
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Menu, through='OrderItems')
    total_amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


# class Payment(models.Model):
#     pass

class Driver(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20)
    driver_license = models.CharField(max_length=20)  # make file field later
    latitude = models.FloatField(default=7.392130)
    longitude = models.FloatField(default=3.839928)
    is_available = models.BooleanField(default=False)
    is_busy = models.BooleanField(default=False)
    # last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Email:{self.user.email} Id:{self.pk}"


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField()
    # location_ordered

    def __str__(self):
        return f"{self.user.email}"


deliveryOrderChoices = (
    ("pending", "pending"),
    ("delivered", "delivered")
)


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(
        max_length=30, choices=deliveryOrderChoices, default=deliveryOrderChoices[0][0])
    
    def __str__(self):
        return f"Order:{self.order.id} Deliver: {self.pk}" 


driverOrderChoices = (
    ("pending", "pending"),
    ("accepted", "accepted"),
    ("cancelled", "cancelled")
)


class Delivery_accept(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    driver_status = models.CharField(
            max_length=30, 
            choices=driverOrderChoices,
            default=driverOrderChoices[0][0]
        )

    def __str__(self):
        return f"{self.driver.user.email}"


class Delivery_location(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

deliverDriverActionChoices = (
    ("pending", "pending"),
    ("accept", "accept"),
    ("reject", "reject")
)

class Delivery_driver_match(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    driver_action = models.CharField(
            max_length=30, 
            choices=deliverDriverActionChoices,
            default=deliverDriverActionChoices[0][0]
        )
    delivery_status = models.CharField(
        max_length=30, choices=deliveryOrderChoices, default=deliveryOrderChoices[0][0])
    time_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} action:{self.driver_action}:{self.driver.user.email}({self.driver.user.id}) --> {self.delivery.order.customer.email} order:{self.delivery.order.pk}" #customer


