from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import *
from .serializers import *
from .permissions import CustomerViewOnly
from .utils import create_delivery, update_order_status, order_complete_status,update_driver_action,update_driver_status


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

            #alert drivers that they have a delivery to make
            #you can put this delivery in a try catch to prevent,
            # untraceable errors
            create_delivery(
                order_id=serializer.data["id"],
                item=list(serializer.data['item'][0].items())
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
        data = request.data
        print(data)
        if Delivery_location.objects.get(order=data['order']):
            return Response({"message": "address for order already exists"},status=status.HTTP_403_FORBIDDEN)
        
        if Order.objects.get(pk=data['order']).customer != data["customer"]:
            return Response({"message": "Invalid customer"},status=status.HTTP_403_FORBIDDEN)

        serializer = DeliveryLocationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data
        return Response(serializer.data)

#TODO: fix this <-- dashboard endpoint
class DeliveryView(generics.ListCreateAPIView):
    #admin level view
    #allow param to do filtering
    serializer_class = DeliveryDriverViewSerializer
    queryset = Delivery.objects.filter(delivery_status="pending")
    # test_query = Delivery_driver_match.objects.filter(delivery__delivery_status__contains="pending")
    # Asset.objects.filter( project__name__contains="Foo" )

    def get(self, request):
        pending_deliveries = Delivery_driver_match.objects.filter(
                delivery__delivery_status__contains="pending",driver_action="pending"
            )
        deliveries_set = set()
        for i in pending_deliveries:
            print(i.delivery.id)
            deliveries_set.add((i.delivery.id))
            
        deliveries = list(deliveries_set)
        print(Delivery.objects.get(pk=6))
        
        return Response(
            {
            "pending_deliveries": deliveries,
            "driver_action": "pending"
            }
        )

class DeliveryInTransitView(generics.ListCreateAPIView):
    #admin level view
    #allow param to do filtering
    serializer_class = DeliveryDriverViewSerializer
    queryset = Delivery.objects.filter(delivery_status="pending")

    def get(self, request):
        pending_deliveries = Delivery_driver_match.objects.filter(
                delivery__delivery_status__contains="pending",driver_action="accept"
            )
        serializer = self.serializer_class(instance=pending_deliveries, many=True)
        
        return Response(serializer.data)


class DeliveryRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'driver'

    
    serializer_class = DeliveryDriverMatchSerializer

    def get(self, request,driver):
        delivery = Delivery_driver_match.objects.filter(driver=driver,driver_action="pending")
        serializer = self.serializer_class(instance=delivery, many=True)
        print(serializer.data)
        return Response(data=serializer.data)


class DeliveryAcceptView(generics.UpdateAPIView):
    """
        Driver accepts order
    """
    serializer_class = DeliveryAcceptSerializer
    queryset = Delivery_driver_match.objects.all()
    lookup_field = 'pk' #driver match id
    
    def update(self, request,pk, *args, **kwargs):
        data = request.data

        if Delivery_driver_match.objects.get(pk=pk).driver.user.id != data["driver"]:
            return Response({"message": "Invalid delivery receipt provided"},status=status.HTTP_403_FORBIDDEN)
        
        if Delivery_driver_match.objects.filter(delivery=data['delivery'],driver_action="accept").exists():
            return Response({"message": "order has been taken"},status=status.HTTP_403_FORBIDDEN)
        else:
            instance = self.get_object()
            
            serializer = self.get_serializer(
                instance, data = request.data, partial=True)
            
            if serializer.is_valid():

                serializer.save()
                data = serializer.data

                #changes order state as driver accepts to take order
                update_order_status(data['delivery'],"in_transit")
                update_driver_action(data['delivery'],"pending","rejected")
                update_driver_status(data['driver'],True)

                return Response({"message": "driver has accepted order"})

            else:
                return Response({"message": "delivery status change failed"})


class DeliveryRejectView(generics.UpdateAPIView):
    """
        Driver rejects order
    """
    serializer_class = DeliveryAcceptSerializer
    queryset = Delivery_driver_match.objects.all()
    lookup_field = 'pk' #driver match id
    
    def update(self, request,pk, *args, **kwargs):
        data = request.data
        
        if Delivery_driver_match.objects.get(pk=pk).driver.user.id != data["driver"]:
            return Response({"message": "Invalid delivery receipt provided"},status=status.HTTP_403_FORBIDDEN)
        
        instance = self.get_object()
        
        serializer = self.get_serializer(
            instance, data = request.data, partial=True)

        
        if serializer.is_valid():

            serializer.save()
            data = serializer.data

            #reverts the order to the state at creation
            update_order_status(data['delivery'],"pending") 
            update_driver_action(data['delivery'],"rejected","pending")
            update_driver_status(data['driver'],False)

            return Response({"message": "driver has rejected order"})

        else:
            return Response({"message": "delivery status change failed"})



class DeliveryCompleteApiView(generics.UpdateAPIView):
    # permission_classes = (IsAuthenticated,)

    queryset = Delivery_driver_match.objects.all()
    serializer_class = DeliveryCompleteSerializer
    lookup_field = 'pk'

    def update(self, request,pk, *args, **kwargs):
        data = request.data

        if Delivery_driver_match.objects.get(pk=pk).driver.user.id != data["driver"]:
            return Response({"message": "Invalid delivery receipt provided"},status=status.HTTP_403_FORBIDDEN)

        if Delivery_driver_match.objects.filter(delivery=data['delivery'],delivery_status="delivered").exists():
            return Response({"message": "incorrect credentials"},status=status.HTTP_403_FORBIDDEN)

        instance = self.get_object()
        
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()
            data = serializer.data
            
            order_complete_status(data['delivery'])
            update_driver_status(data['driver'],False)
            return Response({"message": "delivery has been updated"})
        else:
            return Response({"message": "delivery did not update"})



class DriverLocationApiView(generics.UpdateAPIView):
    # update driver's location

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

class DriverCompletedDeliveryHistoryView(generics.RetrieveAPIView):

    serializer_class = DriverCompleteDeliverySerializer
    lookup_field = 'driver'

    def get(self,request,driver):
        pending_deliveries = Delivery_driver_match.objects.filter(
                driver=driver,delivery_status="delivered"
            )
        serializer = self.serializer_class(instance=pending_deliveries, many=True)
        
        return Response(serializer.data)
