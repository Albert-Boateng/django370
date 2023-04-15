from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('comments_reviews/', views.view_index),
    path('updateProduct/<int:pk>/', views.updateProduct, name='updateProduct'),
    path('deleteProduct/<int:pk>/', views.deleteProduct, name='deleteProduct'),
    path('cart/', views.cart),
    path('thank_you/', views.thank_you),
]