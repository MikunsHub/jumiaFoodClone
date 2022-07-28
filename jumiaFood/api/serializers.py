from rest_framework import serializers
from .models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["country_name"]


class Business_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Type
        fields = ["type"]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "meal_name",
            "restaurant",
            "price"
        ]


class OrderItemsRetrieveSerializer(serializers.ModelSerializer):

    Price = serializers.SerializerMethodField('get_price')
    restaurant = serializers.SerializerMethodField('get_restaurant')

    class Meta:
        model = OrderItems
        fields = ["menu", "quantity", "Price","restaurant"]

    def get_price(self, obj):
        price = obj.menu.price
        quantity = obj.quantity
        return price * quantity

    def get_restaurant(self, obj):
        restaurant_id = obj.menu.restaurant.pk
        return restaurant_id


class OrderSerializer(serializers.ModelSerializer):

    item = OrderItemsRetrieveSerializer(
        many=True,
        source='orderitems_set',
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "item",
            "total_amount"
        )

    def create(self, validated_data):

        items_data = validated_data.pop('orderitems_set')
        order = Order.objects.create(**validated_data)

        for item in items_data:
            order.orderitems_set.create(**item)
        print(order.id)
        return order


class OrderRetrieveSerializer(serializers.ModelSerializer):
    quantity = OrderItemsRetrieveSerializer(
        many=True,
        source='orderitems_set'
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "quantity",
            "total_amount",
        ]
        depth = 1


class DeliveryAcceptSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Delivery_driver_match
        fields = [
            "delivery",
            "driver",
            "driver_action",
        ]


class DriverLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = [
            "user",
            "latitude",
            "longitude",
        ]


class DriverStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = [
            "user",
            "is_available",
        ]


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = [
            "id",
            "order",
            "delivery_status",
        ]

class DeliveryDriverMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery_driver_match
        fields = [
            "id",
            "driver",
            "delivery",
        ]

class DeliveryLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery_location
        fields = [
            "customer",
            "address",
        ]
