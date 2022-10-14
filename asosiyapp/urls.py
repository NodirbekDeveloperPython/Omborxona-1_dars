from django.urls import path
from .views import *
urlpatterns = [
    path('', BolimlarView.as_view(), name='bolimlar'),
    path('mahsulotlar/', MahsulotlarView.as_view(), name='mahsulotlar'),
    path('clientlar/', MijozlarView.as_view(), name='mijozlar'),
    path('del_client/<int:son>/', ClientDeleteView.as_view(), name='delete_client'),
    path('client_update/<int:son>/', ClientUpdateView.as_view(), name='client_update'),
    path('product_update/<int:son>/', ProductUpdateView.as_view(), name='product_update'),
    path('pr_delete/<int:pk>/', ProductDeleteView.as_view(), name='pr_delete'),
]