from user import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpUserView.as_view(), name='signup'),
    path('me/', views.ManageUserView.as_view(), name='profile'),
]
