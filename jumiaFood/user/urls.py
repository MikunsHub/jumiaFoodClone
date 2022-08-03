from django.urls import path
from .views import (
    DriverRegisterView,
    CustomerRegisterView,
    VendorRegisterView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path(
        'register/driver',
        DriverRegisterView.as_view()
    ),
    path(
        'register/customer',
        CustomerRegisterView.as_view()
    ),
    path(
        'register/vendor',
        VendorRegisterView.as_view()
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
        ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
        ),
]
