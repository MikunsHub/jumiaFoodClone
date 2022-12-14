from django.urls import path, include
from .views import (
    CountryCreateListApiView,
    Business_TypeCreateListApiView,
    MenuCreateListApiView,
    OrderCreateListApiView,
    OrderUpdateApiView,
    OrderRetrieveApiView,
    OrderDeleteApiView,
    DeliveryView,
    DeliveryInTransitView,
    DeliveryRetrieveView,
    DeliveryAcceptView,
    DeliveryRejectView,
    DeliveryCompleteApiView,
    DriverLocationApiView,
    DriverAvailabilityApiView,
    DeliveryLocationCreateView,
    DriverCompletedDeliveryHistoryView,
    PaymentApiView,
    VerifyPaymentApiView
)


urlpatterns = [
    path('countries/', CountryCreateListApiView.as_view(),name="country"),
    path('business_type/', Business_TypeCreateListApiView.as_view(),name="business_type"),
    path('menu/', MenuCreateListApiView.as_view()),
    path('order/', OrderCreateListApiView.as_view()),
    path('<int:pk>/order/', OrderUpdateApiView.as_view()),
    path('order/<int:pk>/', OrderRetrieveApiView.as_view()),
    path('order/<int:pk>/delete/', OrderDeleteApiView.as_view()),
    path('payment/<int:order>/', PaymentApiView.as_view()),
    path('payment/<int:order>/verify', VerifyPaymentApiView.as_view()),
    path('delivery', DeliveryView.as_view()),
    path('<int:driver>/delivery', DeliveryRetrieveView.as_view()),
    path('delivery/in_transit', DeliveryInTransitView.as_view()),
    path('delivery/location', DeliveryLocationCreateView.as_view()),
    path('driver/<int:pk>/delivery/accept', DeliveryAcceptView.as_view()),
    path('driver/<int:pk>/delivery/reject', DeliveryRejectView.as_view()),
    path('driver/<int:driver>/delivery/completed', DriverCompletedDeliveryHistoryView.as_view()),
    path('delivery/<int:pk>/order/', DeliveryCompleteApiView.as_view()),
    path('delivery/driver/<int:pk>/location/', DriverLocationApiView.as_view()),
    path('delivery/driver/<int:pk>/status/', DriverAvailabilityApiView.as_view()),
    
    
    
]
