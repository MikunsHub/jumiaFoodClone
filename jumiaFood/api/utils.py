from django.db import models
from rest_framework.response import Response
from .models import Delivery, Order, Vendor, Driver,Delivery_driver_match
from .serializers import DeliveryDriverMatchSerializer
import googlemaps
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

configure()

gmaps = googlemaps.Client(key=f'{os.getenv("gmaps_api_key")}')


def get_restuarant_address(vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)

    vendor_address = vendor.address
    return vendor_address


def find_drivers():
    drivers_queryset = Driver.objects.filter(is_available=True,is_busy=False)
    drivers_data = []

    for i in drivers_queryset:
        id_pk = i.pk

        latitude = str(i.latitude)
        longitude = str(i.longitude)
        coordinates = f'{latitude},{longitude}'

        data = {
            "id": id_pk,
            "coordinates": coordinates
        }
        drivers_data.append(data)

    return drivers_data


def get_suitable_drivers(vendor_adrrs, driver_loca):
    """
    vendor_adrrs: this is the destination
    driver_local: this is the origin,list of all drivers
    """

    driver_ids = []  # append the id and
    driver_coordinates = []  # append the distance in km

    for i in range(len(driver_loca)):

        driver_ids.append(driver_loca[i]["id"])
        driver_coordinates.append(driver_loca[i]["coordinates"])

    print(driver_coordinates)
    print(driver_ids)

    geocode_result = gmaps.distance_matrix(
        origins=[vendor_adrrs],
        destinations=driver_coordinates
    )
    
    distance = []
    for i in geocode_result["rows"][0]["elements"]:
        distance.append(float(i["distance"]["text"].split()[0]))

    print(distance)

    data_dict = {}
    for i in range(len(driver_ids)):
        data_dict[driver_ids[i]] = distance[i]

    print(data_dict)

    sorted_data_dict = {k: v for k, v in sorted(
        data_dict.items(), key=lambda item: item[1])}
    print(sorted_data_dict)

    data = list(sorted_data_dict.keys())

    return data[:3]


def create_delivery(order_id, item):

    order = Order.objects.get(id=order_id)

    #get vendor id from the order data
    temp = item[3]
    vendor_id = temp[-1]

    # logic to find the best drivers will be here
    address = get_restuarant_address(vendor_id)
    drivers_data = find_drivers()
    recommended_drivers = get_suitable_drivers(address, drivers_data)

    drivers = []
    serializer_dict_data = {}
    serializer_dict_data[0] = []

    for i in range(0, len(recommended_drivers)):
        serializer_dict_data = {"driver": recommended_drivers[i]}
        drivers.insert(i, serializer_dict_data)

    # delivery = DeliverySerializer(data={"order": order_id, "drivers": drivers})
    delivery = Delivery(order = order)
    delivery.save()

    #this logic creates a pool of request for drivers to pick from
    for i in range(len(recommended_drivers)):
        driver_match = DeliveryDriverMatchSerializer(
                data = {
                    "delivery":delivery.id,
                    "driver":recommended_drivers[i]
                }
            )
        driver_match.is_valid(raise_exception=True)
        driver_match.save()
    

    return Response({"message": "successfully created a delivery instance"})


def update_order_status(delivery_id,status):
    delivery = Delivery.objects.get(id=delivery_id)

    order_id = delivery.order.id
    order_instance = Order.objects.get(id=order_id)
    order_instance.status = status
    order_instance.save()


def update_driver_action(delivery,query_key,driver_action):
    
    delivery = Delivery.objects.get(id=delivery)

    pending_deliveries = Delivery_driver_match.objects.filter(delivery=delivery,driver_action=query_key)
    
    for pending_delivery in pending_deliveries:
        instance = Delivery_driver_match.objects.get(pk=pending_delivery.id)
        instance.driver_action = driver_action
        instance.save()


def order_complete_status(delivery_id):
    delivery = Delivery.objects.get(id=delivery_id)

    order_id = delivery.order.id
    order_instance = Order.objects.get(id=order_id)

    delivery.delivery_status = "delivered"
    order_instance.status = "delivered"
    
    delivery.save()
    order_instance.save()
    print("order delivered")


def update_driver_status(driver_id,state):
    driver = Driver.objects.get(pk=driver_id)
    
    driver.is_busy = state
    driver.save()