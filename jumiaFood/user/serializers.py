from rest_framework import serializers
from .models import User
from api.models import Driver, Customer, Vendor


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "username",
                  "email", "password", "is_customer"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class DriverUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "username", "email", "password", "is_driver"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "username", "email", "password", "is_vendor"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomerRegisterSerializer(serializers.ModelSerializer):
    user = CustomerUserSerializer(required=True)

    class Meta:
        model = Customer
        fields = [
            'user',
            'dob',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomerUserSerializer.create(
            CustomerUserSerializer(), validated_data=user_data)
        customer, created = Customer.objects.update_or_create(user=user,
                                                              dob=validated_data.pop(
                                                                  'dob'),
                                                              )
        return customer


class DriverRegisterSerializer(serializers.ModelSerializer):
    user = DriverUserSerializer(required=True)

    class Meta:
        model = Driver
        fields = [
            'user',
            'address',
            'vehicle_type',
            'driver_license',

        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = DriverUserSerializer.create(
            DriverUserSerializer(), validated_data=user_data)
        driver, created = Driver.objects.update_or_create(user=user,
                                                          address=validated_data.pop(
                                                              'address'),
                                                          vehicle_type=validated_data.pop(
                                                              'vehicle_type'),
                                                          driver_license=validated_data.pop(
                                                              'driver_license')
                                                          )
        return driver


class VendorRegisterSerializer(serializers.ModelSerializer):
    user = VendorUserSerializer(required=True)

    class Meta:
        model = Vendor
        fields = [
            'user',
            'owner_name',
            'no_of_establishments',
            'country',
            'business_type',
            'address',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = VendorUserSerializer.create(
            VendorUserSerializer(), validated_data=user_data)
        vendor, created = Vendor.objects.update_or_create(user=user,
                                                          owner_name=validated_data.pop(
                                                              'owner_name'),
                                                          no_of_establishments=validated_data.pop(
                                                              'no_of_establishments'),
                                                          country=validated_data.pop(
                                                              'country'),
                                                          business_type=validated_data.pop(
                                                              'business_type'),
                                                          address=validated_data.pop(
                                                              'address'),
                                                          )
        return vendor
