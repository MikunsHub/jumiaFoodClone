from django.urls import path, include
from .views import (
    CountryCreateListApiView,
    Business_TypeCreateListApiView,
    MenuCreateListApiView,
    OrderCreateListApiView,
    OrderUpdateApiView,
    OrderRetrieveApiView,
    OrderDeleteApiView,
    DeliveryRetrieveView,
    DeliveryAcceptView,
    DeliveryRejectView,
    OrderCompleteApiView,
    DriverLocationApiView,
    DriverAvailabilityApiView,
    DeliveryLocationCreateView
)

urlpatterns = [
    path('countries/', CountryCreateListApiView.as_view()),
    path('business_type/', Business_TypeCreateListApiView.as_view()),
    path('menu/', MenuCreateListApiView.as_view()),
    path('order/', OrderCreateListApiView.as_view()),
    path('<int:pk>/order/', OrderUpdateApiView.as_view()),
    path('order/<int:pk>/', OrderRetrieveApiView.as_view()),
    path('order/<int:pk>/delete/', OrderDeleteApiView.as_view()),
    path('<int:driver>/delivery', DeliveryRetrieveView.as_view()),
    path('delivery/location', DeliveryLocationCreateView.as_view()),
    path('driver/<int:pk>/delivery/accept', DeliveryAcceptView.as_view()),
    path('driver/<int:pk>/delivery/reject', DeliveryRejectView.as_view()),
    path('delivery/<int:pk>/order/', OrderCompleteApiView.as_view()),
    path('delivery/driver/<int:pk>/location/', DriverLocationApiView.as_view()),
    path('delivery/driver/<int:pk>/status/', DriverAvailabilityApiView.as_view()),
    
    
]
