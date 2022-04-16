from explorer import views
from django.urls import path


urlpatterns = [
    path('list-folder/<pk>/', views.ListFolderAPIView.as_view(),
         name='list_folder'),
    path('folder/<pk>/', views.ManageFolderAPIView.as_view(),
         name='manage_folder'),
    path('folder/', views.CreateFolderAPIView.as_view(),
         name='create_folder'),
]
