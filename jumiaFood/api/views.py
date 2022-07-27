from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .permissions import CustomerViewOnly
from .utils import create_delivery, update_order_status, order_complete_status


class CountryCreateListApiView(generics.ListCreateAPIView):

    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    # print(queryset)

    def get(self, request):

        countries = Country.objects.all()
        serializer = self.serializer_class(instance=countries, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Business_TypeCreateListApiView(generics.ListCreateAPIView):
    serializer_class = Business_TypeSerializer
    queryset = Business_Type.objects.all()
    # print(queryset)

    def get(self, request):

        business_type = Business_Type.objects.all()
        serializer = self.serializer_class(instance=business_type, many=True)
        return Response(data=serializer.data)


class MenuCreateListApiView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated)
    # permission_classes = [IsAuthenticated,CustomerViewOnly]

    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get(self, request):

        vendor = Menu.objects.all()
        serializer = self.serializer_class(instance=vendor, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderCreateListApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request):
        order = Order.objects.all()
        serializer = self.serializer_class(instance=order, many=True)
        return Response(data=serializer.data)

    def post(self, request):

        data = request.data
        print(type(data))
        print(data)
        total_amount = 0

        for i in data['item']:
            menu_query = Menu.objects.get(pk=i["menu"])
            menu_price = menu_query.price

            Price = i["quantity"] * menu_price
            total_amount += Price

        serializer = self.serializer_class(data=data)

        user = request.user

        if serializer.is_valid():
            serializer.save(customer=user, total_amount=total_amount)
            print(serializer.data)
            create_delivery(
                order_id=serializer.data["id"],
                item=list(serializer.data['item'][1].items())
            )
            return Response(data=serializer.data)

        return Response(data=serializer.errors)


class OrderUpdateApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "order has been updated"})

        else:
            return Response({"message": "order did not update"})


class OrderRetrieveApiView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, CustomerViewOnly]

    queryset = Order.objects.all()
    serializer_class = OrderRetrieveSerializer
    lookup_field = 'pk'


class OrderDeleteApiView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'


class DeliveryLocationCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryLocationSerializer
    queryset = Delivery_location.objects.all()

    def get(self, request):
        location = Delivery_location.objects.all()
        serializer = self.serializer_class(instance=location, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = DeliveryLocationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data
        return Response(serializer.data)


class DeliveryRetrieveView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = DeliverySerializer

    def get(self, request):
        delivery = Delivery.objects.filter(delivery_status="pending")
        serializer = self.serializer_class(instance=delivery, many=True)
        return Response(data=serializer.data)


class DeliveryAcceptCreateView(generics.ListCreateAPIView):
    """
        Driver accepts order
    """
    serializer_class = DeliveryAcceptSerializer
    queryset = Delivery_accept.objects.all()

    def post(self, request):
        serializer = DeliveryAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        data = serializer.data
        update_order_status(data['delivery'])

        return Response(serializer.data)


# another endpoint for the driver to show that they have completed
# the order

class OrderCompleteApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer  # serializer for delivery
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            print(data)
            order_complete_status(data['id'])
            return Response({"message": "delivery has been updated"})

        else:
            return Response({"message": "delivery did not update"})

# update driver's location


class DriverLocationApiView(generics.UpdateAPIView):

    queryset = Driver.objects.all()
    serializer_class = DriverLocationSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data)

        else:
            return Response({"message": "Driver location did not update"})


class DriverAvailabilityApiView(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)

    queryset = Driver.objects.all()
    serializer_class = DriverStatusSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data)

        else:
            return Response({"message": "Driver availability did not update"})
