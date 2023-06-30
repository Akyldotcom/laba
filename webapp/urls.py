from django.urls import path

from webapp.views import product_list_view, product_create_view, product_view, category_create_view

urlpatterns = [
    path('', product_list_view, name="index"),
    path('product/create', product_create_view, name="create_product"),
    path('product/<int:pk>/', product_view, name="product_view"),
    path('categories/', category_create_view, name="categories_create_view")
]
