from explorer import views
from django.urls import path, include
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
#
# router.register('folders', views.ManageFolderViewset, basename='folders')

urlpatterns = [
    path('list-folder/<pk>/', views.ListFolderAPIView.as_view(), name='list_folder'),
    path('folder/<pk>/', views.ManageFolderAPIView.as_view(), name='manage_folder'),
]