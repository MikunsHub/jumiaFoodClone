from rest_framework import generics
from rest_framework.response import Response


from .serializers import DriverRegisterSerializer, CustomerRegisterSerializer, VendorRegisterSerializer


class CustomerRegisterView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated)

    serializer_class = CustomerRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = serializer.save()
        CustomerRegisterSerializer(
            driver, context=self.get_serializer_context()).data
        return Response(serializer.data)


class DriverRegisterView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated)

    serializer_class = DriverRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = serializer.save()
        print(driver)
        driver_data = DriverRegisterSerializer(
            driver, context=self.get_serializer_context()).data
        print(driver_data)
        print(serializer.data)
        return Response(serializer.data)


class VendorRegisterView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated)

    serializer_class = VendorRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.save()
        print(vendor)
        vendor_data = VendorRegisterSerializer(
            vendor, context=self.get_serializer_context()).data
        print(vendor_data)
        print(serializer.data)
        return Response(serializer.data)
